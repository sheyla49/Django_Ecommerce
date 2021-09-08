from django import forms

class ContactForms(forms.Form):
    Nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Tu nombre'}))
    Email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Tu Correo Electronico'}))
    Descripcion = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Tu Mensaje'}))