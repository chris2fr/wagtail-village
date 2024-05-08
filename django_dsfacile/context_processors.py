from django.utils.translation import get_language

from django_dsfacile.models import DsfacileConfig


def site_config(request):
    # Tries to return the site config object in the current language first.
    config = DsfacileConfig.objects.filter(language=get_language()).first()

    # Failing that, it returns the first site config object
    if not config:
        config = DsfacileConfig.objects.first()

    return {"SITE_CONFIG": config}
