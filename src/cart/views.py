import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from .utils import get_or_set_order_session
from .models import Product, OrderItem, Address, Payment, Order
from .forms import AddtoCartForm, AddressForm
from django.shortcuts import get_object_or_404, reverse, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ProductListView(generic.ListView):
    template_name='cart/product_list.html'
    queryset=Product.objects.all()


class ProductDetailView(generic.FormView):
    template_name = 'cart/product_detail.html'
    form_class = AddtoCartForm

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

#funcion redirigir al home
    def get_success_url(self):
        return reverse("cart:summary") #TODO: cart

#creando una instancia y esta adquiriendo el product.id
    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs["product_id"] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

#incrementar la cantidad de lo ya añadido al carrito
        item_filter = order.items.filter(
            product=product,
            colour=form.cleaned_data['colour'],
            size=form.cleaned_data['size']
            )

        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity'])
            item.save()
#si no existe nada en el carrito entonces agregamos
        else:
            new_item = form.save(commit=False)
            new_item.product = product
#definir la orden
            new_item.order = order
            new_item.save()

        return super(ProductDetailView, self).form_valid(form)

#**kwargs (son los argumentos)
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context ['product'] = self.get_object()
        return context

class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context

# aumentar cantidad

class IncreaseQuantityView(generic.View): #producto exacto que deseas incrementar
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("cart:summary")

class DecreaseQuantityView(generic.View): #producto exacto que deseas incrementar
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])

        if  order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("cart:summary")


class RemoveFromCartView(generic.View): #producto exacto que deseas incrementar
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("cart:summary")


class CheckoutView(generic.FormView):
    form_class = AddressForm
    template_name = 'cart/checkout.html'
    

    def get_success_url(self):
        return reverse("cart:payment") # TODO: payment

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_billing_address = form.cleaned_data.get('selected_billing_address')

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                address_type= 'B',
                user = self.request.user,
                address_line_1=form.cleaned_data['billing_address_line_1'],
                address_line_2=form.cleaned_data['billing_address_line_2'],
#                zip_code = form.cleaned_data['billing_zip_code'],
                city=form.cleaned_data['billing_city'],
            )
            order.billing_address = address #guardar en la orden

        order.save()
        messages.info(
            self.request,"Añadiste exitosamente tu dirección")
        return super(CheckoutView, self).form_valid(form)

# guardar informacion proporcionada para hacer compra
    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"]=self.request.user.id
        return kwargs
#De lo que estamos comprando y ordenado
    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context


class PaymentView(generic.TemplateView):
    template_name = 'cart/payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context ["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context ['order'] = get_or_set_order_session(self.request)
        context ['CALLBACK_URL'] = reverse("cart:thank-you")
        return context

class ConfirmOrderView(generic.View):
    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        body = json.loads(request.body) #para ver que el pago ha sido completado
        payment = Payment.objects.create(
            order=order,
            successful=True,
            raw_response = json.dumps(body),
            amount = float(body["purchase_units"][0]["amount"]["value"]),
            payment_method='Paypal'
        )
        order.ordered = True
        order.ordered_date = datetime.date.today()
        order.save()
        return JsonResponse({"data": "Success"})

class ThankYouView(generic.TemplateView):
    template_name = 'cart/thanks.html'

class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'order.html'
    queryset = Order.objects.all()
    context_object_name = 'order'