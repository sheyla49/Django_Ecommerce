from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse

User = get_user_model()

class Address(models.Model):
    ADDRESS_CHOICES = (
        ('B', 'Billing'), #direccion de cobro que se tiene
        ('S', 'Shipping'), #direccion de entrega
    )
    #especificar usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
     #usuarios seleccionar su default address

    def _str_(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.city}, {self.zip_code}"

#nombres verbosos como plural
class  Meta:
    verbose_name_plural = 'Adresses'

class ColourVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SizeVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=150)
    #cargarlo urls
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    price = models.IntegerField(default=0) #decimal
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=False)
    available_colours = models.ManyToManyField(ColourVariation)
    available_sizes = models.ManyToManyField(SizeVariation)

    def __str__(self):
        return self.title
#llamamos a la funcion para obtener el url absoluto ... redirigir a otro sitio
    def get_absolute_url(self):
        return reverse("cart:product-detail", kwargs={'slug': self.slug})

    def get_price(self):
        return "{:.2f}".format(self.price / 100)

#vinculo del modelo y la cantidad de lo q tiene en el carrito
class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    colour = models.ForeignKey(ColourVariation, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariation, on_delete=models.CASCADE)

#representacion en cadena texto

    def _str_(self):
        return f"{self.quantity} x {self.product.title}"

    def get_raw_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_item_price(self):
        price = self.get_raw_total_item_price() #1000
        return "{:.2f}".format(price / 100)

#la compra, vincular con el usuario
class Order(models.Model):
    user = models.ForeignKey(
            User,blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(blank=True, null=True) #fecha fue comprado
    ordered = models.BooleanField(default=False)

#Si el usuario borro su direccion para que lo pueda colocar en la compra
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL)

    def _str_(self):
        return self.reference_number

# instancia que devuelve el numero de referencia para cuando haga una orden
    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"
        
    def get_raw_subtotal(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_raw_total_item_price()
        return total

    def get_subtotal(self):
        subtotal = self.get_raw_subtotal()
        return "{:.2f}".format(subtotal / 100)


    def get_raw_total(self):
        subtotal = self.get_raw_subtotal()
        tax = 0.18
        total = subtotal + tax
        return total

    def get_total(self):
        total = self.get_raw_total()
        return "{:.2f}".format(total / 100)

# clase para los pagos
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=(
    ('Paylpal', 'Paypal'),
    ))
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    amount = models.FloatField()
    raw_response = models.TextField() #API del p  rocesador de pagos

    def _str_(self):
        return self.reference_number


    @property
    def reference_number(self):
        return f"PAYMENT.{self.order}-{self.pk}"
#pk es el orden de pago (primerkey)

def pre_save_product_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = slugify(instance.title)

pre_save.connect(pre_save_product_receiver, sender=Product)
