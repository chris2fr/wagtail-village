from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from wagtail_fastoche import urls as wagtail_fastoche_urls
from wagtail_fastoche.views import SearchResultsView, TagsListView, TagView


urlpatterns = [
    path("cms-admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

urlpatterns += [
    path("", include(wagtail_urls)),
]
urlpatterns += wagtail_fastoche_urls.urlpatterns

urlpatterns += i18n_patterns(
    path("", include("wagtail_fastoche.blog.urls", namespace="blog")),
    path(_("search/"), SearchResultsView.as_view(), name="page_search"),
    path("tags/<str:tag>/", TagView.as_view(), name="global_tag"),
    path("tags/", TagsListView.as_view(), name="global_tags_list"),
    prefix_default_language=False,
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
