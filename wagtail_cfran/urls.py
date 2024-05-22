from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django_cfran import urls as django_cfran_urls  # , views
from django_cfran.cfran_components import ALL_TAGS

# from django_distill import distill_path
from wagtail import urls as wagtail_urls

from wagtail_cfran.views import SearchResultsView, TagsListView, TagView


def get_all_tags():
    for key in ALL_TAGS:
        yield ({"tag_name": key})


urlpatterns = [
    path(_("search/"), SearchResultsView.as_view(), name="cms_search"),
    path("tags/<str:tag>/", TagView.as_view(), name="global_tag"),
    path("tags/", TagsListView.as_view(), name="global_tags_list"),
    path("", include(wagtail_urls)),
] + django_cfran_urls.urlpatterns
