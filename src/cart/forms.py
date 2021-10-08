from django import forms
from .models import OrderItem, ColourVariation, Product, SizeVariation, Address
from django.contrib.auth import get_user_model


User = get_user_model()

#formulario para agregar al carrito
class AddtoCartForm(forms.ModelForm):
    colour = forms.ModelChoiceField(queryset=ColourVariation.objects.none())
    size = forms.ModelChoiceField(queryset=SizeVariation.objects.none())
    quantity = forms.IntegerField(min_value=1)


    class Meta:
        model = OrderItem
        fields = ['quantity', 'colour', 'size']

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=product_id)
        super().__init__(*args, **kwargs)

#setear nuestro color
        self.fields['colour'].queryset = product.available_colours.all()
#setear nuestro tamaño
        self.fields['size'].queryset = product.available_sizes.all()


class AddressForm(forms.Form):

    billing_address_line_1 = forms.CharField(required=False)
    billing_address_line_2 = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)

    selected_billing_address = forms.ModelChoiceField(
        Address.objects.none(), required=False
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)

        billing_address_qs = Address.objects.filter(
            user=users,
            address_type='B',
        )

        self.fields['selected_billing_address'].queryset = billing_address_qs

#los datos sean correctamente ingresados
    def clean(self):
        data = self.cleaned_data

        selected_billing_address = data.get('selected_billing_address', None)
        if selected_billing_address is None:
            if not data.get('billing_address_line_1', None):
                self.add_error("billing_address_line_1","Por Favor complete este campo")
            if not data.get('billing_address_line_2', None):
                self.add_error("billing_address_line_2","Por Favor complete este campo")
            if not data.get('billing_city', None ):
                self.add_error("billing_city","Por Favor complete este campo")