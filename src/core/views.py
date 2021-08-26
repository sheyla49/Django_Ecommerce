from django.shortcuts import render
from django.views import generic 

class Homeview(generic.TemplateView):
    template_name = 'index.html'


# Create your views here.
class ContactView(generic.FormView):
    form_class=
    template_name='contact.html'