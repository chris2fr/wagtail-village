from django.apps import AppConfig


# from allauth.account.signals import user_signed_up
# from django.contrib.auth.models import Group


# def user_signed_up_callback(sender, request, user, **kargs):
#     dashboard_user_group = Group.objects.get(name="dashboard")
#     user.groups.add(dashboard_user_group)


class LesGrandsVoisinsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lesgrandsvoisins"

    # def ready(self):
    #     user_signed_up.connect(user_signed_up_callback)
