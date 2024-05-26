import os

from wagtail_cefran.models import MegaMenu  # , WagtailCefranConfig


# from django.utils.translation import get_language


# from django_cefran.context_processors import site_config

# def site_config(request):
#     # Tries to return the site config object in the current language first.
#     config = WagtailCefranConfig.objects.filter(language=get_language()).first()

#     # Failing that, it returns the first site config object
#     if not config:
#         config = WagtailCefranConfig.objects.first()

#     config.operator_logo_file = config.operator_logo_file_wagtail

#     return {"SITE_CONFIG": config}


def skiplinks(request) -> dict:
    return {
        "skiplinks": [
            {"link": "#content", "label": "Contenu"},
            {"link": "#cefran-navigation", "label": "Menu"},
        ]
    }


def mega_menus(request) -> dict:
    menus = list(MegaMenu.objects.all().values_list("parent_menu_item_id", flat=True))

    return {"mega_menus": menus}


def urlangs(request):
    return {
        "URLANGS": [
            {
                "code": "en",
                "name_local": "English",
                "name": "English",
                "bidi": False,
                "name_translated": "English",
                "url": "/en/" if not os.getenv("URLANG_EN") else os.getenv("URLANG_EN"),
            },
            {
                "code": "fr",
                "name_local": "French",
                "name": "Français",
                "bidi": False,
                "name_translated": "Français",
                "url": "/" if not os.getenv("URLANG_FR") else os.getenv("URLANG_FR"),
            },
        ]
    }
