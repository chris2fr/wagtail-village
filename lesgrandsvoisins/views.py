import os

from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv  # Pour les variables d'.env

# import requests
from keycloak import KeycloakAdmin

from .forms import signup


# Prendre les variables d'environnement
load_dotenv()


# Create your views here.
def signup_view(request):
    context = {}
    if request.method == "POST":
        form = signup(request.POST)

        if form.is_valid():
            # Process the form data
            context["username"] = form.cleaned_data["username"]
            context["firstName"] = form.cleaned_data["firstName"]
            context["lastName"] = form.cleaned_data["lastName"]
            context["email"] = form.cleaned_data["email"]
            context["telephoneNumber"] = form.cleaned_data["telephoneNumber"]
            context["password"] = form.cleaned_data["password"]
            # Here you can save the data to the database, send an email, etc.
            admin = KeycloakAdmin(
                server_url="https://key.lesgrandsvoisins.com/",
                username=os.getenv("NEWUSER_USERNAME"),
                password=os.getenv("NEWUSER_PASSWORD"),
                realm_name="master",
            )
            newuserdata = {}
            formdata = {}
            user_id = admin.get_user_id(context["username"])
            if user_id:
                return render(request, "registration_username.html", {"username": context["username"]})
                # return 'https://key.lesgrandsvoisins.com/realms/master/account/applications'
            email_users = admin.get_users({"email": context["email"]})
            if len(email_users) > 0:
                formdata["username"] = email_users[0]["username"]
                formdata["href"] = "https://key.lesgrandsvoisins.com/realms/master/account/applications"
                return render(request, "registration_email.html", formdata)
            for i in [
                "email",
                "username",
                "firstName",
                "lastName",
                "telephoneNumber",
            ]:
                if ("%s" % context[i]) != "":
                    newuserdata[i] = context[i]
            newuserdata["attributes"] = {
                "locale": ["fr"],
            }
            newuserdata["credentials"] = [
                {
                    "value": context["password"],
                    "type": "password",
                }
            ]
            newuserdata["enabled"] = True
            new_user = admin.create_user(newuserdata, exist_ok=False)
            if new_user:
                return redirect("https://key.lesgrandsvoisins.com/realms/master/account/applications")
        else:
            context["info"] = "Erreur dans les données du formulaire (CAPTCHA ?)"
    else:
        context["info"] = request.GET.get("info")
        form = signup()
    context["form"] = form
    context["page"] = {}
    context["page"]["title"] = _("Enregistrement de personne utilisatrice")
    return render(request, "registration_form.html", context)

    # print(req_data)
    # headers = {
    #   "Content-Type": "application/x-www-form-urlencoded"
    # };
    # response = requests.post(api_url, data=json.dumps(req_data),headers=headers)
    # response = requests.post(api_url, json=req_data, headers=headers)
    # response_data=response.json()
    # print(response.json())
    # token=response_data['access_token']
    # api_url = "https://key.lesgrandsvoisins.com/admin/realms/master/users/count?username=%s" % userdata['username']
    # headers = {
    #   "Authorization": "Bearer %s" %  token,
    #   "Content-Type":"application/json",
    # };
    # response = requests.get(api_url, headers=headers)
    # print(response)
    # print(response.json())
