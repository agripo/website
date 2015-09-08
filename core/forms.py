from django import forms

from core.models import Command, Product, CommandProduct, AgripoUser

class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Command
        fields = ('delivery', 'message', )
        widgets = {
            'delivery': forms.fields.Select(attrs={'class': 'form-control input-lg', }),
            'message': forms.Textarea(attrs={'class': 'form-control input-lg textarea-3-lines', })}

    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
        self.fields['message'].required = False

    def save(self):
        command = super().save(commit=False)
        command.customer = AgripoUser.objects.get(pk=self.customer.pk)
        command.save()
        cart_products = Product.static_get_cart_products()
        command.total = 0
        for product in cart_products:
            the_product = Product.objects.get(id=product['id'])
            quantity = product['quantity']
            command.total += quantity * the_product.price
            command_product = CommandProduct(command=command, product=the_product, quantity=quantity)
            command_product.save()
            the_product.buy(quantity)

        command.save()
        Product.static_clear_cart()
        return command
