# import the standard Django Forms
# from built-in library
from captcha.fields import CaptchaField
from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _


# declare a new model with a name "GeeksModel"
class signup(forms.Form):
    # fields of the model
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("nomdutilisateur@example.com"),
                "class": "required",
                "onChange": "javascript:id_username.value=this.value.replace(/@.*/,'')",
            }
        ),
        label=_("Email"),
        required=True,
    )
    firstName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Prénom"),
                "onChange": "javascript:id_displayName.value=id_firstName.value + ' ' + id_lastName.value",
            }
        ),
        max_length=200,
        label=_("Prénom"),
        required=False,
    )
    lastName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Nom de Famille"),
                "class": "required",
                "onChange": "javascript:id_displayName.value=id_firstName.value + ' ' + id_lastName.value",
            }
        ),
        max_length=200,
        label=_("Nom de famille"),
        required=True,
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("nomdutilisateur"), "class": "required"}),
        validators=[validators.validate_slug],
        label=_("identifiant"),
        required=True,
    )
    telephoneNumber = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("+33 6 12 34 56 78")}),
        max_length=32,
        required=False,
        label=_("Numéro de téléphone"),
    )
    displayName = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Oumar Xhi")}),
        max_length=200,
        label=_("Nom usuel affiché"),
        required=False,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "required", "onClick": "javascript:peekAtPass(this)"}),
        label=_("Mot de passe"),
        required=True,
    )
    captcha = CaptchaField()

    # img = forms.ImageField(upload_to = "images/")

    def __str__(self):
        return self.username
