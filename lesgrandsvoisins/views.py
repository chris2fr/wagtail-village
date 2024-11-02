from django.shortcuts import render
from .forms import RegistrationForm
# import requests
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection

import os
import json
from dotenv import load_dotenv # Pour les variables d'.env
# Prendre les variables d'environnement
load_dotenv()

# Create your views here.
def registrationform_view(request):
  context = {}
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      # Process the form data
      context['username'] = form.cleaned_data['username']
      context['firstName'] = form.cleaned_data['firstName']
      context['lastName'] = form.cleaned_data['lastName']
      context['email'] = form.cleaned_data['email']
      context['telephoneNumber'] = form.cleaned_data['telephoneNumber']
      context['password'] = form.cleaned_data['password']
      # Here you can save the data to the database, send an email, etc.
      add_new_user(context)
      return redirect('https://key.lesgrandsvoisins.com/realms/master/account/applications')

      # return render(request, 'registration_success.html', context)
    else:
      context['validate_message'] = "erreur dans les données du formulaire"
  else:
    form = RegistrationForm()
  context['form'] = form;
  return render(request, "registration_form.html", context)

def add_new_user(userdata):
  # keycloak_connection = KeycloakOpenIDConnection(
  #   server_url="https://key.lesgrandsvoisins.com/",
  #   client_id="admin-api",
  #   realm_name="master",
  #   password=os.getenv("NEWUSER_PASSWORD"),
  #   username=os.getenv("NEWUSER_USERNAME")
  # )
  # keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

  admin = KeycloakAdmin(
            server_url="https://key.lesgrandsvoisins.com/",
            username=os.getenv("NEWUSER_USERNAME"),
            password=os.getenv("NEWUSER_PASSWORD"),
            realm_name="master",
          )
  newuserdata = {}
  for i in ['email', 'username', 'firstName', 'lastName', 'telephoneNumber', ]:
    if ("%s" % userdata[i]) != "":
      newuserdata[i] = userdata[i]
  newuserdata["attributes"] = {
        "locale": ["fr"],
      }
  newuserdata["credentials"] = [{"value": userdata["password"],"type": "password",}]
  newuserdata["enabled"] = True
  new_user = admin.create_user(
    newuserdata,
    exist_ok=False)
  # print(req_data)
  # headers = {
  #   "Content-Type": "application/x-www-form-urlencoded"
  # };
  # response = requests.post(api_url, data=json.dumps(req_data),headers=headers)
  # response = requests.post(api_url, json=req_data, headers=headers)
  # response_data=response.json()
  # print(response.json())    
  # token=response_data['access_token']
  # api_url = "https://key.lesgrandsvoisi   ns.com/admin/realms/master/users/count?username=%s" % userdata['username']
  # headers = {
  #   "Authorization": "Bearer %s" %  token,
  #   "Content-Type":"application/json",
  # };
  # response = requests.get(api_url, headers=headers)
  # print(response)
  # print(response.json())
  