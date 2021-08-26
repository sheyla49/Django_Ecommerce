from django import forms

class ContactForms(forms.From):
    name=forms.CharField(max_lenght=100)