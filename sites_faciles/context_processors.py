import os

from sites_faciles.models import MegaMenu  # , WagtailSitesFacilesConfig
from sites_faciles.sites_faciles_page.models import WagtailSitesFacilesConfig


# from django.utils.translation import get_language


# from django_design_system.context_processors import site_config

# def site_config(request):
#     # Tries to return the site config object in the current language first.
#     config = WagtailSitesFacilesConfig.objects.filter(language=get_language()).first()

#     # Failing that, it returns the first site config object
#     if not config:
#         config = WagtailSitesFacilesConfig.objects.first()

#     config.operator_logo_file = config.operator_logo_file_wagtail

#     return {"SITE_CONFIG": config}


def skiplinks(request) -> dict:
    return {
        "skiplinks": [
            {"link": "#content", "label": "Contenu"},
            {"link": "#village-navigation", "label": "Menu"},
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


def sitevars(request):
    settings = WagtailSitesFacilesConfig.for_request(request)
    return {
        "langcode": settings.language,
        "home_url": "/{}/".format(settings.language),
        "data_sites_faciles_mourning": "data-village-mourning" if settings.mourning else "",
        "full_site_title": settings.site_title,
    }
    #
    # context["langcode"] = settings.language
    # context["data_sites_faciles_mourning"] = ""
    # if settings.mourning:
    #     context["data_sites_faciles_mourning"] = "data-village-mourning"
    # context["full_title"] = settings.site_title
    # if context["page"].title:
    #     context["full_title"] = context["page"].title + " - " + context["full_title"]
    # context["search_description"] = False
    # if hasattr(context["page"], "search_description") and context["page"].search_description:
    #     context["search_description"] = context["page"].search_description
