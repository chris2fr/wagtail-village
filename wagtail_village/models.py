from django.db import models
from django.forms.widgets import Textarea
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

# from wagtail.images import get_image_model_string
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet

from wagtail_village.abstract import SitesFacilesBasePage, WagtailVillageConfig
from wagtail_village.managers import TagManager
from wagtail_village.widgets import WagtailVillageIconPickerWidget


class ContentPage(SitesFacilesBasePage):
    tags = ClusterTaggableManager(through="TagContentPage", blank=True)

    class Meta:
        verbose_name = _("Content page")

    settings_panels = SitesFacilesBasePage.settings_panels + [
        FieldPanel("tags"),
    ]


class TagContentPage(TaggedItemBase):
    content_object = ParentalKey("ContentPage", related_name="contentpage_tags")


@register_snippet
class Tag(TaggitTag):
    objects = TagManager()

    class Meta:
        proxy = True


class MonospaceField(models.TextField):
    """
    A TextField which renders as a large HTML textarea with monospace font.
    """

    def formfield(self, **kwargs):
        kwargs["widget"] = Textarea(
            attrs={
                "rows": 12,
                "class": "monospace",
                "spellcheck": "false",
            }
        )
        return super().formfield(**kwargs)


@register_setting(icon="code")
class AnalyticsSettings(BaseSiteSetting):
    class Meta:
        verbose_name = "Scripts de suivi"

    head_scripts = MonospaceField(
        blank=True,
        null=True,
        verbose_name="Scripts de suivi <head>",
        help_text="Ajoutez des scripts de suivi entre les balises <head>.",
    )

    body_scripts = MonospaceField(
        blank=True,
        null=True,
        verbose_name="Scripts de suivi <body>",
        help_text="Ajoutez des scripts de suivi vers la fermeture de la balise <body>.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("head_scripts"),
                FieldPanel("body_scripts"),
            ],
            heading="Scripts de suivi",
        ),
    ]


class SocialMediaItem(Orderable):
    site_config = ParentalKey(WagtailVillageConfig, related_name="social_media_items")
    title = models.CharField(_("Title"), max_length=200, default="", blank=True)

    url = models.URLField(
        _("URL"),
        default="",
        blank=True,
    )
    icon_class = models.CharField(_("Icon class"), max_length=200, default="", blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        FieldPanel("icon_class", widget=WagtailVillageIconPickerWidget),
    ]

    class Meta:
        verbose_name = _("Social media item")
        verbose_name_plural = _("Social media items")


# Mega-Menus
class MegaMenuCategory(Orderable):
    mega_menu = ParentalKey("wagtail_village.MegaMenu", related_name="categories", on_delete=models.CASCADE)
    category = models.ForeignKey("wagtailmenus.FlatMenu", on_delete=models.CASCADE, verbose_name=_("Category"))

    class Meta:
        verbose_name = _("Mega menu category")
        verbose_name_plural = _("Mega menu categories")


@register_snippet
class MegaMenu(ClusterableModel):
    name = models.CharField(_("Name"), max_length=255)
    parent_menu_item = models.ForeignKey(
        "wagtailmenus.MainMenuItem", on_delete=models.CASCADE, related_name="megamenu_parent_menu_items"
    )
    description = models.TextField(_("Description"), blank=True)
    main_link = models.URLField(_("Main link"), blank=True, null=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("parent_menu_item"),
        FieldPanel("description"),
        FieldPanel("main_link"),
        InlinePanel(
            "categories",
            max_num=4,
            heading=_("Categories"),
            help_text=_("Maximum 4 categories, each with maximum 8 links."),
        ),
    ]

    def __str__(self):  # type: ignore
        return self.name

    def get_categories(self):
        return self.categories.order_by("sort_order")

    class Meta:
        verbose_name = _("Mega menu")
