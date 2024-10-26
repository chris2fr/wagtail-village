from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import  FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail import blocks
import lesgv.services
# from lesgv.blocks import GhostIndexBlock
# from modelcluster.fields import ParentalKey

from django.http import HttpResponseRedirect

from django import template
register = template.Library()

@register_setting
class WagtailSettings(BaseGenericSetting):
    site_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    homepage_link = models.URLField(
        null=True,
        blank=True,
    )
    footer1 = RichTextField(blank=True, null=True)
    footer2 = RichTextField(blank=True, null=True)
    theme = models.CharField(max_length=32,choices=[('generique','generique'),
                                                    ('boule','boule'),
                                                    ('lesartsvoisins','lesartsvoisins'),],
                                                    blank=True,null=True,default='generique')
    menu =     menu = StreamField([
        ("menu", blocks.StructBlock([
            ("label", blocks.CharBlock()),
            ("url",blocks.URLBlock()),
            ("submenu", blocks.ListBlock(blocks.StructBlock([
                ("label", blocks.CharBlock()),
                ("url",blocks.URLBlock())
            ]),required=False
            )),
        ]),
    )],use_json_field=True, blank=True, null=True)
    panels = [
        FieldPanel('site_logo'),
        FieldPanel('homepage_link'),
        FieldPanel('menu'),
        FieldPanel('footer1'),
        FieldPanel('footer2'),
        FieldPanel('theme'),
    ]
    class Meta:
        verbose_name = "Default Settings for All Websites"

@register_setting
class WebsiteSettings(BaseSiteSetting):
    site_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    homepage_link = models.URLField(
        null=True,
        blank=True,
    )
    footer1 = RichTextField(blank=True, null=True)
    footer2 = RichTextField(blank=True, null=True)
    menu =     menu = StreamField([
        ("menu", blocks.StructBlock([
            ("label", blocks.CharBlock()),
            ("url",blocks.URLBlock()),
            ("submenu", blocks.ListBlock(blocks.StructBlock([
                ("label", blocks.CharBlock()),
                ("url",blocks.URLBlock())
            ]),required=False
            )),
        ]),
    )],use_json_field=True, blank=True, null=True)
    theme = models.CharField(max_length=32,choices=[('generique','generique'),
                                                    ('boule','boule'),
                                                    ('lesartsvoisins','lesartsvoisins'),],
                                                    blank=True,null=True,default='generique')
    csscolors = models.TextField(blank=True, null=True)
    panels = WagtailSettings.panels + [
        FieldPanel('csscolors'),
    ]
    
    class Meta:
        verbose_name = "Settings Per Website"

def notanytest(val):
    return (any([
        val is None,
        val == '',
        val == '<p></p>',
    ]))

def lesgvGetMenuItems(page):
  menuitems = page.get_children().filter(live=True, show_in_menus=True)
  return menuitems

def lesgvGetBreadcrumbs(page):
  breadcrumbs = []
  for a in page.get_ancestors():
      if (not a.is_root()):
          breadcrumb = {
              "url": a.url,
              "title":a.title,
              "children":[]
          }
          for c in a.get_children().filter(live=True, show_in_menus=True):
              breadcrumb["children"] += [{
                  "url": c.url,
                  "title":c.title
              }]
          breadcrumbs += [breadcrumb]
  return breadcrumbs

class FaireMainPage(Page):
    # body = RichTextField(blank=True, null=True, features=["h2", "h3", "h4", "h5", "bold", "italic", "ol", "ul", "hr", "link", "document", "image", "embed", "code", "blockquote", "media" ])
    body = RichTextField(blank=True, null=True)
    intro = RichTextField(blank=True, null=True)
    # posts_index = StreamField([
    #     ('ghost_index_blog',GhostIndexBlock(required=False))
    #     ], use_json_field=True, blank=True, null=True
    #     , max_num=1)
    footer1 = RichTextField(blank=True, null=True)
    footer2 = RichTextField(blank=True, null=True)
    redirect_url = models.URLField(blank=True, null=True)
    extramenu = StreamField([
        ("menu", blocks.StructBlock([
            ("label", blocks.CharBlock()),
            ("url",blocks.URLBlock()),
            ("submenu", blocks.ListBlock(blocks.StructBlock([
                ("label", blocks.CharBlock()),
                ("url",blocks.URLBlock())
            ]),required=False
            )),
        ]),
    )],use_json_field=True, blank=True, null=True)
    ghost_post_tag = models.SlugField(blank=True, null=True)
    theme = models.CharField(max_length=32,choices=[('generique','generique'),
                                                    ('boule','boule'),
                                                    ('lesartsvoisins','lesartsvoisins'),]
                                                    ,blank=True,null=True,default='generique')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    page_description = "Faire Ma Page, Une page"
    # parent_page_types = ['wagtailcore.Page','lesgv.FaireMainHomePage','lesgv.FaireMainPage','lesgv.FaireMainMenu']
    # subpage_types = ['lesgv.FaireMainPage','lesgv.FaireMainAgendaItemPage']
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('intro'),
        FieldPanel('ghost_post_tag'),
        FieldPanel('image')
    ]
    settings_panels = [
        FieldPanel('theme'),
        FieldPanel('extramenu'),
        FieldPanel('footer1'),
        FieldPanel('footer2'),
        FieldPanel('redirect_url'),
    ]
    # def serve(self, request):
    #     if self.redirect_url and not notanytest(self.redirect_url):
    #         # Perform the redirect
    #         return HttpResponseRedirect(self.redirect_url)
    #     else:
    #         # Handle the case when redirect_url is empty or false
    #         # For example, render a custom template or return a different response
    #         return super().serve(request)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['website_settings'] = WebsiteSettings.for_request(request=request)
        context['wagtail_settings'] = WagtailSettings.load(request_or_site=request)

        for item in ['site_logo','homepage_link','footer1','footer2','theme','menu']:
            context[item] = getattr(context['website_settings'],item)
            if (notanytest(context[item])):
                context[item] = getattr(context['wagtail_settings'],item)
        for item in ['site_logo','homepage_link','footer1','footer2','theme','menu']:
            context[item] = getattr(context['website_settings'],item)
            if (hasattr(self,item) and getattr(self,item) != ""):
                context[item] = getattr(self,item)
            elif (notanytest(context[item])):
                context[item] = getattr(context['wagtail_settings'],item)    
        if (hasattr(self,'extramenu') and getattr(self,'extramenu') != ""):
            context['extramenu'] = getattr(self,'extramenu')
        else:
            context['extramenu'] = []
        context['menuitems'] = lesgvGetMenuItems(self)
        context['breadcrumbs'] = lesgvGetBreadcrumbs(self)
        
        if (not context['theme']):
            context['theme'] = "generique"
        context['static_images'] = {}
        for item in ['TL','TR','BL','BR','ML','MR','BC']:
            context['static_images'][item] = "images/fairemain/{theme}/fairemain_{item}.svg".format(theme = context['theme'],item = item)
        context["posts"] = []
        if (self.ghost_post_tag):
            context['posts'] = lesgv.services.get_blog_posts(lesgv.services.ProcessGhostParams({"ghost_tag": self.ghost_post_tag,"ghost_limit":8}))
        return context
    
class FaireMainMenu(FaireMainPage):
    parent_page_types = ['wagtailcore.Page','lesgv.FaireMainHomePage','lesgv.FaireMainPage']
    subpage_types = [ ]
    max_count_per_parent = 1
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['menuitems'] = lesgvGetMenuItems(self.get_parent())
        context['breadcrumbs'] = lesgvGetBreadcrumbs(self.get_parent())
        return context

class RelatedAgendaItemHomePage(Orderable):
    home_page = ParentalKey(
        'FaireMainHomePage',
        related_name='agenda_home',
    )
    agenda_item = models.ForeignKey(
        'FaireMainAgendaItemPage',
        related_name="+",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel('agenda_item'),
    ]

class FaireMainHomePage(FaireMainPage):
    agenda = RichTextField(blank=True, null=True)
    ghost_tag = models.CharField(blank=True, null=True, max_length=32)
    ghost_filter = models.CharField(blank=True, null=True, max_length=32)
    ghost_order = models.CharField(blank=True, null=True, max_length=32)
    # ghost_formats = models.CharField(blank=True, null=True, max_length=32)
    ghost_limit = models.CharField(blank=True, null=True, max_length=8)
    ghost_include = models.CharField(blank=True, null=True, max_length=32)
    page_description = "Faire Main Home Page: Une page home "
    parent_page_types =['wagtailcore.Page','lesgv.FaireMainHomePage']
    # subpage_types = ['lesgv.FaireMainPage','lesgv.FaireMainAgendaItemPage','lesgv.FaireMainMenu',]
    content_panels = FaireMainPage.content_panels + [
        InlinePanel('agenda_home',label="Items de l'agenda"),
        FieldPanel('agenda'),
        FieldPanel('ghost_tag'),
        FieldPanel('ghost_filter'),
        FieldPanel('ghost_order'),
        FieldPanel('ghost_limit'),
        FieldPanel('ghost_include'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        params = {
            'ghost_tag': self.ghost_tag,
            'ghost_limit': self.ghost_limit,
            'ghost_include': self.ghost_include,
            'ghost_order': self.ghost_order,
            'ghost_filter': self.ghost_filter,
            'ghost_page':  request.GET.get('page', 1)
        }
        context['posts'] = lesgv.services.get_blog_posts(lesgv.services.ProcessGhostParams(params))
        context['related_agenda'] = RelatedAgendaItemHomePage.objects.filter(home_page=self)
        return context 
    
class FaireMainAgendaItemPage(FaireMainPage):
    # home_page = ParentalKey(FaireMainHomePage, on_delete=models.CASCADE, related_name='agenda_home_item',null = True, blank = True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    place = models.CharField(blank=True, null=True, max_length=128)
    place_url = models.URLField(blank=True, null=True)
    page_description = "Faire Ma Agenda Item Page, Un évènement"
    parent_page_types = ['lesgv.FaireMainPage','lesgv.FaireMainAgendaItemPage']
    subpage_types = ['lesgv.FaireMainAgendaItemPage']
    content_panels = FaireMainPage.content_panels + [
        FieldPanel('start'),
        FieldPanel('end'),
        FieldPanel('place'),
        FieldPanel('place_url'),
    ] 

