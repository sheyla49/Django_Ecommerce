from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic
from .forms import ContactForms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Order

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.updated({
            "orders": Order.objects.filter(user=self.request.user, ordered=True)
        })
        return context

class Homeview(generic.TemplateView):
    template_name = 'index.html'

# Create your views here.
class ContactView(generic.FormView):
    form_class=ContactForms
    template_name='contact.html'

    def get_success_url(self):
        return reverse("contact")

# si es valido el correo lo vamos a enviar
    def form_valid(self, form):
        messages.info(
            self.request, "Hemos recibido tu correo")
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        message = form.cleaned_data.get("message")
        full_message = """
                Mensaje recibido de {name}, {email}
                _______________________

                {message}
                """
        send_mail(
            subject="Mensaje recibio por Contact Form",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)
