import os
from dotenv import load_dotenv # Pour les variables d'.env
# Prendre les variables d'environnement
load_dotenv()

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)



SOCIALACCOUNT_PROVIDERS = {
  "OAUTH_PKCE_ENABLED": True,
  'openid_connect': {
    "APPS": [
      {
        "provider_id": "key-lesgrandsvoisins-com",
        "name": "key.lesgrandsvoisins.com",
        "client_id": os.getenv('OPENID_NAME'),
        "secret": os.getenv('OPENID_SECRET'),
        "settings": {
            "server_url": os.getenv('OPENID_URL'),
            # Optional token endpoint authentication method.
            # May be one of "client_secret_basic", "client_secret_post"
            # If omitted, a method from the the server's
            # token auth methods list is used
            "token_auth_method": "client_secret_basic",
        },
      },
    ],
    # 'SOCIALACCOUNT_ONLY': True
  }
}

# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/'
# ACCOUNT_AUTHENTICATION_METHOD = "username"
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
# ACCOUNT_LOGOUT_ON_GET = True
# ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
# ACCOUNT_PRESERVE_USERNAME_CASING = False
# ACCOUNT_SESSION_REMEMBER = True
# ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
# ACCOUNT_USERNAME_BLACKLIST = ["admin", "god"]
# ACCOUNT_USERNAME_MIN_LENGTH = 2