from django.utils.translation import gettext_lazy as _

from wagtail_village.models import ContentPage


class WagtailVillageLesgrandsvoisinsHome(ContentPage):
    class Meta:
        verbose_name = _("Home Page Les Grands Voisins")
