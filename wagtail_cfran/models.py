from django.db import models
from django.forms.widgets import Textarea
from django.utils.translation import gettext_lazy as _
from django_cfran.models import CfranConfig
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField

# from wagtail.images import get_image_model_string
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet

from wagtail_cfran.abstract import SitesFacilesBasePage
from wagtail_cfran.constants import LIMITED_RICHTEXTFIELD_FEATURES
from wagtail_cfran.managers import TagManager
from wagtail_cfran.widgets import WagtailCfranIconPickerWidget


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


@register_setting(icon="cog")
class WagtailCfranConfig(ClusterableModel, BaseSiteSetting, CfranConfig):
    class Meta:
        verbose_name = _("Site configuration")
        verbose_name_plural = _("Site configurations")

    # # Operator logo
    # operator_logo_file_wagtail = models.ForeignKey(
    #     get_image_model_string(),
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    #     verbose_name=_("Operator logo"),
    # )
    footer_description_wagtail = RichTextField(
        _("Description"),
        default="",
        blank=True,
        features=LIMITED_RICHTEXTFIELD_FEATURES,
    )

    # operator_logo_alt = models.CharField(
    #     _("Logo alt text"),
    #     max_length=200,
    #     blank=True,
    #     help_text=_("Must contain the text present in the image."),
    # )
    # operator_logo_width = models.DecimalField(
    #     _("Width (em)"),
    #     max_digits=3,
    #     decimal_places=1,
    #     null=True,
    #     default="0.0",
    #     help_text=_(
    #         "To be adjusted according to the width of the logo.\
    #         Example for a vertical logo: 3.5, Example for a horizontal logo: 8."
    #     ),
    # )

    search_bar = models.BooleanField("Barre de recherche dans l’en-tête", default=False)  # type: ignore
    theme_modale_button = models.BooleanField("Choix du thème clair/sombre", default=False)  # type: ignore

    site_panels = [
        FieldPanel("site_title"),
        FieldPanel("site_tagline"),
        FieldPanel("footer_description_wagtail"),
        FieldPanel("footer_description"),
        FieldPanel("notice"),
        MultiFieldPanel(
            [
                FieldPanel("operator_logo_file"),
                FieldPanel("operator_logo_alt"),
                FieldPanel("operator_logo_width"),
            ],
            heading=_("Operator logo"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("search_bar"),
                FieldPanel("mourning"),
                FieldPanel("beta_tag"),
                FieldPanel("theme_modale_button"),
            ],
            heading=_("Advanced settings"),
        ),
    ]

    brand_panels = [
        MultiFieldPanel(
            [
                FieldPanel("header_brand"),
                FieldPanel("header_brand_html"),
            ],
            heading=_("Header"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_brand"),
                FieldPanel("footer_brand_html"),
            ],
            heading=_("Footer"),
        ),
    ]

    newsletter_social_media_panels = [
        MultiFieldPanel(
            [
                FieldPanel("newsletter_description"),
                FieldPanel("newsletter_url"),
            ],
            heading=_("Newsletter"),
        ),
        InlinePanel("social_media_items", label=_("Social media items")),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(site_panels, heading=_("Generic")),
            ObjectList(brand_panels, heading=_("Brand block")),
            ObjectList(newsletter_social_media_panels, heading=_("Newsletter and social media")),
        ]
    )

    def show_newsletter_block(self):
        if self.newsletter_description and self.newsletter_url:
            return True
        else:
            return False

    def show_social_block(self):
        return bool(self.social_media_items.count())

    def show_newsletter_and_social_block(self):
        # Returns true if at least one of the two blocks is used
        if self.show_newsletter_block() or self.show_social_block():
            return True
        else:
            return False


class SocialMediaItem(Orderable):
    site_config = ParentalKey(WagtailCfranConfig, related_name="social_media_items")
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
        FieldPanel("icon_class", widget=WagtailCfranIconPickerWidget),
    ]

    class Meta:
        verbose_name = _("Social media item")
        verbose_name_plural = _("Social media items")


# Mega-Menus
class MegaMenuCategory(Orderable):
    mega_menu = ParentalKey("wagtail_cfran.MegaMenu", related_name="categories", on_delete=models.CASCADE)
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
