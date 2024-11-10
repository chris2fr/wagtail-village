from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from wagtail import urls as wagtail_urls

from wagtail_design_system.views import SearchResultsView, TagsListView, TagView
from wagtail_design_system.wagtail_design_system_blog.urls import urlpatterns as wagtail_design_system_blog_urlpatterns


# from django_design_system import urls as django_design_system_urls  # , views
# from django_design_system.sites_faciles_components import ALL_TAGS

# # from django_distill import distill_path
# from wagtail import urls as wagtail_urls


urlpatterns = [
    # Look into search TODO
    path(_("search/"), SearchResultsView.as_view(), name="sites_faciles_search"),
    path("tags/<str:tag>/", TagView.as_view(), name="global_tag"),
    path("tags/", TagsListView.as_view(), name="global_tags_list"),
    path("", include(wagtail_urls)),
] + wagtail_design_system_blog_urlpatterns
