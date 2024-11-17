"""
WSGI config for lesgrandsvoisins project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lesgrandsvoisins.settings.production")


application = get_wsgi_application()


@receiver(user_signed_up)
def user_signed_up_callback(sender, request, user, **kargs):
    dashboard_user_group = Group.objects.get(name="dashboard")
    user.groups.add(dashboard_user_group)
