from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count
from django.db.models.expressions import F
from django.forms.widgets import Textarea
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language, gettext_lazy as _
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
    TitleFieldPanel,
)
from wagtail.admin.widgets.slug import SlugInput
from wagtail.contrib.forms.models import AbstractFormField, EmailFormMixin, FormMixin
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Orderable, Page
from wagtail.models.i18n import Locale, TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from django_design_system.constants import COLOR_CHOICES
from django_design_system.models import DjangoDesignSystemConfig
from sites_faciles.blocks import STREAMFIELD_COMMON_BLOCKS
from sites_faciles.constants import LIMITED_RICHTEXTFIELD_FEATURES
from sites_faciles.managers import TagManager
from sites_faciles.utils import get_streamfield_raw_text
from sites_faciles.widgets import WagtailSitesFacilesIconPickerWidget


@register_setting(icon="cog")
class WagtailSitesFacilesConfig(ClusterableModel, BaseSiteSetting, DjangoDesignSystemConfig):
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
        # FieldPanel("footer_description"),
        FieldPanel("language"),
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


class SitesFacilesBasePage(Page):
    """
    This class defines a base page model that will be used
    by all pages in Sites Faciles
    """

    body = StreamField(
        STREAMFIELD_COMMON_BLOCKS,
        blank=True,
        use_json_field=True,
    )

    header_with_title = models.BooleanField(_("Show title in header image?"), default=False)  # type: ignore

    header_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Header image"),
    )

    header_color_class = models.CharField(
        _("Background color"),
        choices=COLOR_CHOICES,
        null=True,
        blank=True,
        help_text=_("Uses the French Design System colors"),
    )

    header_large = models.BooleanField(_("Full width"), default=False)  # type: ignore
    header_darken = models.BooleanField(_("Darken background image"), default=False)  # type: ignore

    header_cta_text = models.CharField(
        _("Call to action text"),
        null=True,
        blank=True,
    )

    header_cta_label = models.CharField(
        _("Call to action label"),
        null=True,
        blank=True,
    )

    header_cta_link = models.URLField(
        _("Call to action link"),
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body", heading=_("Body")),
    ]

    panels = Page.content_panels + [
        FieldPanel("body", heading=_("Body")),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, _("Common page configuration")),
        MultiFieldPanel(
            [
                FieldPanel("header_with_title"),
                FieldPanel("header_image"),
                FieldPanel("header_color_class"),
                FieldPanel("header_large"),
                FieldPanel("header_darken"),
                FieldPanel("header_cta_text"),
                FieldPanel("header_cta_label"),
                FieldPanel("header_cta_link"),
            ],
            heading=_("Header options"),
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    def get_absolute_url(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.search_description:
            search_description = get_streamfield_raw_text(self.body, max_words=20)
            if search_description:
                self.search_description = search_description
        return super().save(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # settings = WagtailSitesFacilesConfig.for_request(request)
        # context["langcode"] = settings.language
        # context["data_sites_faciles_mourning"] = ""
        # if settings.mourning:
        #     context["data_sites_faciles_mourning"] = "data-village-mourning"
        # context["full_title"] = settings.site_title
        if context["page"].title:
            context["full_title"] = context["page"].title + " - "  # + context["full_site_title"]
        # context["search_description"] = False
        if hasattr(context["page"], "search_description") and context["page"].search_description:
            context["search_description"] = context["page"].search_description
        return context

    class Meta:
        abstract = True
        verbose_name = _("Base page")
        verbose_name_plural = _("Base pages")


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
    site_config = ParentalKey(WagtailSitesFacilesConfig, related_name="social_media_items")
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
        FieldPanel("icon_class", widget=WagtailSitesFacilesIconPickerWidget),
    ]

    class Meta:
        verbose_name = _("Social media item")
        verbose_name_plural = _("Social media items")


# Mega-Menus
class MegaMenuCategory(Orderable):
    mega_menu = ParentalKey("sites_faciles.MegaMenu", related_name="categories", on_delete=models.CASCADE)
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
