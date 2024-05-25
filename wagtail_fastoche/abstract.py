from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.search import index

from django_fastoche.constants import COLOR_CHOICES
from django_fastoche.models import FastocheConfig
from wagtail_fastoche.blocks import STREAMFIELD_COMMON_BLOCKS
from wagtail_fastoche.constants import LIMITED_RICHTEXTFIELD_FEATURES
from wagtail_fastoche.utils import get_streamfield_raw_text


@register_setting(icon="cog")
class WagtailFastocheConfig(ClusterableModel, BaseSiteSetting, FastocheConfig):
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

    def get_context(self, request):
        context = super(SitesFacilesBasePage, self).get_context(request)
        settings = WagtailFastocheConfig.for_request(request)
        context["langcode"] = settings.language
        context["data_fastoche_mourning"] = ""
        if settings.mourning:
            context["data_fastoche_mourning"] = "data-fastoche-mourning"
        context["full_title"] = settings.site_title
        if context["page"].title:
            context["full_title"] = context["page"].title + " - " + context["full_title"]
        return context

    class Meta:
        abstract = True
        verbose_name = _("Base page")
        verbose_name_plural = _("Base pages")
