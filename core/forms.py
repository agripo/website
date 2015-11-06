import smtplib
from django import forms
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings

from core.models.users import AgripoUser, CustomerData
from core.models.shop import Product, Command, CommandProduct, Delivery
from core.models.general import SiteConfiguration


class ReservationForm(forms.Form):
    CHOICES = (('maison_hote', 'Maison d\'hôtes'), ('ecolodge', 'Écolodge'))
    type = forms.ChoiceField(choices=CHOICES, label="Hébergement")
    CHOICES = (
        ('classe_verte', 'Classe verte'),
        ('agroutourisme', 'Agrotourisme'),
        ('speleologie', 'Spéléologie'))
    activity = forms.ChoiceField(choices=CHOICES, label="Activité")

    arrival = forms.DateField(label="Date d'arrivée prévue",
                              widget=forms.TextInput(attrs={'class': 'datepicker'}))
    departure = forms.DateField(label="Date de départ prévue",
                                widget=forms.TextInput(attrs={'class': 'datepicker'}))

    first_name = forms.CharField(max_length=128, label="Votre prénom")
    last_name = forms.CharField(max_length=128, label="Votre nom")
    phone = forms.CharField(max_length=128, label="Votre numéro de téléphone", help_text="Utiliser le format international")
    email = forms.EmailField(label="Votre adresse email")

    message = forms.CharField(widget=forms.Textarea(), label="Message", help_text="Champ facultatif")

    def send_email(self, **kwargs):
        mail_title = "Agripo - Nouvelle réservation depuis le site"
        html_content = "Bonjour,<br />"
        html_content += "Une réservation vient d'être validée sur le site. Voici les données de l'utilisateur :<br /><br />"
        html_content += "<b>Nom</b> : {} {}<br />".format(self.cleaned_data["first_name"], self.cleaned_data["last_name"])
        html_content += "<b>Télephone</b> : {}<br />".format(self.cleaned_data["phone"])
        html_content += "<b>E-mail</b> : {}<br /><br />".format(self.cleaned_data["email"])
        html_content += "<b>Hébergement</b> : {}<br />".format(self.cleaned_data["type"])
        html_content += "<b>Activité</b> : {}<br />".format(self.cleaned_data["activity"])
        html_content += "<b>Date d'arrivée prévue</b> : {}<br />".format(
            self.cleaned_data["arrival"].strftime('%d/%m/%Y'))
        html_content += "<b>Date de départ prévue</b> : {}<br />".format(
            self.cleaned_data["departure"].strftime('%d/%m/%Y'))
        if self.cleaned_data["message"]:
            html_content += "<b>Message</b> : <br />"
            html_content += self.cleaned_data["message"].replace("\n", "<br />")

        mail_content = strip_tags(html_content.replace("<br />", "\n"))
        mail_from = settings.EMAIL_HOST_USER

        config = SiteConfiguration.objects.get()
        mail_to = [config.email]

        try:
            send_mail(mail_title, mail_content, mail_from, mail_to, fail_silently=False, html_message=html_content)
        except smtplib.SMTPException:
            # @todo log this!!!
            pass


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
        mail_from = settings.EMAIL_HOST_USER
        mail_to = [customer.email]
        try:
            send_mail(title, content, mail_from, mail_to, fail_silently=False, html_message=html_content)
        except smtplib.SMTPException:
            # @todo log this!!!
            pass

        return command
