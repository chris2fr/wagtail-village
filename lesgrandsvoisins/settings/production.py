from allauth.account.signals import user_signed_up

from .base import *


DEBUG = False

try:
    from .local import *
except ImportError:
    pass


@receiver(user_signed_up)
def user_signed_up_callback(sender, request, user, **kargs):
    dashboard_user_group = Group.objects.get(name="dashboard")
    user.groups.add(dashboard_user_group)
