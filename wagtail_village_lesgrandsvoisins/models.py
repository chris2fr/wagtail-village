from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField

from wagtail_village.blocks import STREAMFIELD_COMMON_BLOCKS
from wagtail_village.models import ContentPage


SECTION_CHOICES = [
    ("layout01", _("Design 1")),
    ("layout02", _("Design 2")),
    ("layout03", _("Design 3")),
    ("layout04", _("Design 4")),
    ("layout05", _("Design 5")),
    ("layout06", _("Design 6")),
]


class HomeSectionBlock(blocks.StructBlock):
    layout = blocks.ChoiceBlock(
        label=_("Design"),
        choices=SECTION_CHOICES,
        required=False,
        default="layout02",
        help_text=_("Choisir une mise en page variable"),
    )
    content = blocks.StreamBlock(
        STREAMFIELD_COMMON_BLOCKS, blank=True, use_json_field=True, verbose_name=_("Heme Section Content")
    )


class WagtailVillageLesgrandsvoisinsHome(ContentPage):
    sections = StreamField([("sections", HomeSectionBlock())], blank=True, use_json_field=True)
    section_1_body = StreamField(
        STREAMFIELD_COMMON_BLOCKS,
        blank=True,
        use_json_field=True,
    )

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

    content_panels = ContentPage.content_panels + [
        FieldPanel("sections"),
        FieldPanel("section_1_body"),
        FieldPanel("section_2_description_rich"),
        FieldPanel("section_2_body"),
        FieldPanel("section_3_body"),
    ]

    class Meta:
        verbose_name = _("Home Page Les Grands Voisins")
