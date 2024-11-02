# import the standard Django Forms
# from built-in library
from captcha.fields import CaptchaField
from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _


# declare a new model with a name "GeeksModel"
class signup(forms.Form):
    # fields of the model
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("nomdutilisateur"), "class": "required"}),
        validators=[validators.validate_slug],
        label=_("Pseudo d'utilisateur"),
        required=True,
        label_suffix=" * ",
    )
    firstName = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Prénom")}),
        max_length=200,
        label=_("Prénom"),
        required=False,
        label_suffix=" ",
    )
    lastName = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Nom de Famille"), "class": "required"}),
        max_length=200,
        label=_("Nom de famille"),
        required=True,
        label_suffix="* ",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("nomdutilisateur@example.com"), "class": "required"}),
        label=_("Email"),
        required=True,
        label_suffix=" * ",
    )
    telephoneNumber = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("+33 6 12 34 56 78")}),
        max_length=32,
        required=False,
        label=_("Numéro de téléphone"),
        label_suffix="   ",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "required"}),
        label=_("Mot de passe"),
        required=True,
        label_suffix=" * ",
    )
    captcha = CaptchaField()

    # img = forms.ImageField(upload_to = "images/")

    def __str__(self):
        return self.username
