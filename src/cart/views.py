from django.shortcuts import render
from django.views import generic
from .utils import get_or_set_order_session
from .models import Product, OrderItem
from .forms import AddtoCartForm
from django.shortcuts import get_object_or_404, reverse, redirect


# Create your views here.
class ProductListView(generic.ListView):
    template_name='cart/product_list.html'
    queryset = Product.objects.all()


class ProductDetailView(generic.FormView):
    template_name = 'cart/product_detail.html'
    form_class =  AddtoCartForm

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

#funcion redirigir al home
    def get_success_url(self):
        return reverse("cart:summary") #TODO: cart

#creando una instancia y esta adquiriendo el product.id
    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs['product_id'] = self.get_object().id
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
            item.quantity = int(form.cleaned_data['quantity'])
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
    template_name='cart/cart.html'
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

