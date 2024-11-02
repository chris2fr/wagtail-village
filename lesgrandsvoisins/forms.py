# import the standard Django Forms
# from built-in library
from django.utils.translation import gettext_lazy as _
from django import forms 
from django.core import validators

# declare a new model with a name "GeeksModel"
class RegistrationForm(forms.Form ):
    # fields of the model
    username = forms.CharField(validators=[validators.validate_slug], required = True, label_suffix='*')
    firstName = forms.CharField(max_length = 200, required = False)
    lastName = forms.CharField(max_length = 200, required = True, label_suffix='*')
    email = forms.EmailField(widget = forms.EmailInput(), required = True, label_suffix='*')
    telephoneNumber = forms.CharField(max_length = 32, required = False, label=_("Numéro de téléphone"))
    password = forms.CharField(widget = forms.PasswordInput(), required = True, label_suffix='*')
    # img = forms.ImageField(upload_to = "images/")

    def __str__(self):
        return self.username    

