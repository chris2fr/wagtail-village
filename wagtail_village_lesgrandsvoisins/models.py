from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField

from wagtail_village.blocks import STREAMFIELD_COMMON_BLOCKS
from wagtail_village.models import ContentPage


class WagtailVillageLesgrandsvoisinsHome(ContentPage):
    title_rich = RichTextField(null=True, blank=True, verbose_name=_("Titre Homepage"))
    description_rich = RichTextField(null=True, blank=True, verbose_name=_("Description Homepage"))

    section_2_description_rich = RichTextField(null=True, blank=True, verbose_name=_("Description Section 2"))
    section_2_body = StreamField(
        STREAMFIELD_COMMON_BLOCKS,
        blank=True,
        use_json_field=True,
    )

    section_3_body = StreamField(
        STREAMFIELD_COMMON_BLOCKS,
        blank=True,
        use_json_field=True,
    )

    content_panels = (
        [
            FieldPanel("title_rich"),
            FieldPanel("description_rich"),
        ]
        + ContentPage.content_panels
        + [
            FieldPanel("section_2_description_rich"),
            FieldPanel("section_2_body"),
            FieldPanel("section_3_body"),
        ]
    )

    class Meta:
        verbose_name = _("Home Page Les Grands Voisins")
