from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path

# from django.utils.translation import gettext_lazy as _
# from django_village import urls as djangovillage_urls
# from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_transfer import urls as wagtailtransfer_urls


# from wagtail_village import urls as wagtailvillage_urls
# from wagtail_village.views import SearchResultsView, TagsListView, TagView


urlpatterns = [
    path("cms-admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("wagtail-transfer/", include(wagtailtransfer_urls)),
]
if settings.DEBUG_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

# urlpatterns += [
#     path("", include(wagtail_urls)),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include("wagtail_village.urls")),
    path("", include("wagtail_village_blog.urls", namespace="wagtail_village_blog")),
    prefix_default_language=True,
)
