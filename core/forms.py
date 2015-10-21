import smtplib
from django import forms
from django.core.mail import send_mail
from django.utils.html import strip_tags

from core.models.users import AgripoUser, CustomerData
from core.models.shop import Product, Command, CommandProduct, Delivery


class CheckoutForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, label="Prénom")
    last_name = forms.CharField(max_length=128, label="Nom")
    phone = forms.CharField(max_length=128, label="Téléphone")

    class Meta:
        model = Command
        fields = ('first_name', 'last_name', 'phone', 'delivery', 'message')
        widgets = {
            'delivery': forms.fields.Select(attrs={'class': 'form-control input-lg', }),
            'message': forms.Textarea(attrs={'class': 'form-control input-lg textarea-3-lines', })}

    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
        self.fields['message'].required = False
        qs = Delivery.objects.available()
        valid_ids = qs.values_list('pk', flat=True)[:10]
        self.fields['delivery'].queryset = Delivery.objects.filter(pk__in=valid_ids)
        customer = AgripoUser.objects.get(pk=self.customer.pk)
        self.fields['first_name'].initial = customer.first_name
        self.fields['last_name'].initial = customer.last_name
        try:
            self.fields['phone'].initial = customer.customerdata.phone
        except CustomerData.DoesNotExist:
            pass


    def save(self, **kwargs):
        kwargs['commit'] = False
        command = super().save(**kwargs)

        customer = AgripoUser.objects.get(pk=self.customer.pk)
        customer.first_name = self.cleaned_data["first_name"]
        customer.last_name = self.cleaned_data["last_name"]
        customer.save()

        try:
            customer.customerdata.phone
        except CustomerData.DoesNotExist:
            CustomerData.objects.create(customer=customer)

        customer.customerdata.phone = self.cleaned_data["phone"]
        customer.customerdata.save()

        command.customer = AgripoUser.objects.get(pk=self.customer.pk)
        command.save()
        cart_products = Product.static_get_cart_products(self.customer)
        command.total = 0
        command_content = ''
        for product in cart_products:
            the_product = Product.objects.get(id=product['id'])
            quantity = product['quantity']
            command.total += quantity * the_product.price
            command_product = CommandProduct(command=command, product=the_product, quantity=quantity)
            command_product.save()
            the_product.buy(quantity)
            command_content += "<strong>{}</strong> x <strong>{} ({} FCFA)</strong><br />".format(
                quantity, the_product.name, quantity * the_product.price)

        command_content += "Total : <strong>{} FCFA</strong><br />".format(command.total)
        command.save()
        Product.static_clear_cart(self.customer)

        title = 'Agripo - Commande validée'
        html_content = 'Bonjour,<br />Votre commande a été validée avec succès.<br /><br />'
        html_content += 'Elle sera disponible au point de rendez-vous suivant : {}<br /><br />'.format(
            self.cleaned_data['delivery'])
        html_content += "Contenu de votre commande : <br />{}<br /><br />".format(command_content)
        html_content += "Nous vous remercions pour votre confiance.<br /><br />L'équipe d'Agripo"
        content = strip_tags(html_content.replace("<br />", "\n"))
        mail_from = 'briceparent@free.fr'
        mail_to = ['brice@websailors.fr']
        try:
            send_mail(title, content, mail_from, mail_to, fail_silently=False, html_message=html_content)
        except smtplib.SMTPException:
            # @todo log this!!!
            pass

        return command
