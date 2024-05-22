from wagtail_fastoche.models import MegaMenu  # , WagtailFastocheConfig


# from django.utils.translation import get_language


# from django_fastoche.context_processors import site_config

# def site_config(request):
#     # Tries to return the site config object in the current language first.
#     config = WagtailFastocheConfig.objects.filter(language=get_language()).first()

#     # Failing that, it returns the first site config object
#     if not config:
#         config = WagtailFastocheConfig.objects.first()

#     config.operator_logo_file = config.operator_logo_file_wagtail

#     return {"SITE_CONFIG": config}


def skiplinks(request) -> dict:
    return {
        "skiplinks": [
            {"link": "#content", "label": "Contenu"},
            {"link": "#fastoche-navigation", "label": "Menu"},
        ]
    }


def mega_menus(request) -> dict:
    menus = list(MegaMenu.objects.all().values_list("parent_menu_item_id", flat=True))

    return {"mega_menus": menus}
