from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path

# from django.utils.translation import gettext_lazy as _
# from django_cefran import urls as djangocefran_urls
# from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls


# from wagtail_cefran import urls as wagtailcefran_urls
# from wagtail_cefran.views import SearchResultsView, TagsListView, TagView


urlpatterns = [
    path("cms-admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
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
    path("", include("wagtail_cefran.urls")),
    path("", include("wagtail_cefran.blog.urls", namespace="wagtail_cefran.blog")),
    prefix_default_language=False,
)
