from django.db import models
from django.contrib.auth import get_user_model

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

class Product(models.Model):
    title = models.CharField(max_length=150)
    #cargarlo urls
    slug = models.SlugField()
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=False)

    def __str__(self):
        return self.title
#vinculo del modelo y la cantidad de lo q tiene en el carrito
class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

#representacion en cadena texto

    def _str_(self):
        return f"{self.quantity} x {self.product.title}"

#la compra, vincular con el usuario
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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