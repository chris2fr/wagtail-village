from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from wagtail import urls as wagtail_urls

from wagtail_cefran.views import SearchResultsView, TagsListView, TagView


# from django_cefran import urls as django_cefran_urls  # , views
# from django_cefran.cefran_components import ALL_TAGS

# # from django_distill import distill_path
# from wagtail import urls as wagtail_urls


urlpatterns = [
    path(_("search/"), SearchResultsView.as_view(), name="wagtail_cefran_search"),
    path("tags/<str:tag>/", TagView.as_view(), name="global_tag"),
    path("tags/", TagsListView.as_view(), name="global_tags_list"),
    path("", include(wagtail_urls)),
]
