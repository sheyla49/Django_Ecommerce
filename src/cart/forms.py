from django import forms
from .models import OrderItem, ColourVariation, Product, SizeVariation

#formulario para agregar al carrito
class AddtoCartForm(forms.ModelForm):
    colour = forms.ModelChoiceField(queryset=ColourVariation.objects.none())
    size = forms.ModelChoiceField(queryset=SizeVariation.objects.none())



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
