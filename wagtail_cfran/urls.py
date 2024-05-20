from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django_distill import distill_path
from wagtail import urls as wagtail_urls

from django_cfran import views
from django_cfran.cfran_components import ALL_TAGS
from wagtail_cfran.views import SearchResultsView, TagsListView, TagView


def get_all_tags():
    for key in ALL_TAGS:
        yield ({"tag_name": key})


urlpatterns = [
    path(_("search/"), SearchResultsView.as_view(), name="cms_search"),
    path("tags/<str:tag>/", TagView.as_view(), name="global_tag"),
    path("tags/", TagsListView.as_view(), name="global_tags_list"),
    path("", include(wagtail_urls)),
    distill_path(
        "doc-contributing",
        views.doc_contributing,
        name="doc_contributing",
        distill_file="django_cfran/doc-contributing/index.html",
    ),
    distill_path(
        "doc-install",
        views.doc_install,
        name="doc_install",
        distill_file="django_cfran/doc-install/index.html",
    ),
    distill_path(
        "doc-usage",
        views.doc_usage,
        name="doc_usage",
        distill_file="django_cfran/doc-usage/index.html",
    ),
    distill_path(
        "components/",
        views.components_index,
        name="components_index",
        distill_file="django_cfran/components/index.html",
    ),
    distill_path(
        "components/header/",
        views.page_component_header,
        name="page_component_header",
        distill_file="django_cfran/components/header/index.html",
    ),
    distill_path(
        "components/footer/",
        views.page_component_footer,
        name="page_component_footer",
        distill_file="django_cfran/components/footer/index.html",
    ),
    distill_path(
        "components/follow/",
        views.page_component_follow,
        name="page_component_follow",
        distill_file="django_cfran/components/follow/index.html",
    ),
    distill_path(
        "components/<slug:tag_name>/",
        views.page_component,
        name="page_component",
        distill_func=get_all_tags,
    ),
    distill_path(
        "form/",
        views.doc_form,
        name="doc_form",
        distill_file="django_cfran/form/index.html",
    ),
    # distill_path(
    #     "form/example/",
    #     views.page_form,
    #     name="page_form",
    #     distill_file="django_cfran/form/example/index.html",
    # ),
    # distill_path(
    #     "form/example-formset/",
    #     views.AuthorCreateView.as_view(),
    #     name="form_formset",
    #     distill_file="django_cfran/form/example-formset/index.html",
    # ),
    # distill_path(
    #     "resources/colors",
    #     views.resource_colors,
    #     name="resource_colors",
    #     distill_file="django_cfran/resources/colors/index.html",
    # ),
    distill_path(
        "resources/icons",
        views.resource_icons,
        name="resource_icons",
        distill_file="django_cfran/resources/icons/index.html",
    ),
    distill_path(
        "resources/pictograms",
        views.resource_pictograms,
        name="resource_pictograms",
        distill_file="django_cfran/resources/pictograms/index.html",
    ),
    distill_path(
        "search/",
        views.search,
        name="page_search",
        distill_file="django_cfran/search/index.html",
    ),
]
