from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_transfer import urls as wagtailtransfer_urls

# from .models import FeedMeModel, RssFeedMeFeeds
# from .views import FeedMeListView, FeedMeDetailView

# from snotra_rss import urls as snotra_urls
# from feedreader import urls as feedreader_urls
# from puput import urls as puput_urls 
from lesgv import views as lesgv_views

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('wagtail-transfer/', include(wagtailtransfer_urls)),
    path('htmlmenu', lesgv_views.htmlmenu),
    # path("__debug__/", include("debug_toolbar.urls")),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    #from debug_toolbar import urls as debug_toolbar_urls
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls")),]
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # path(r'', include('puput.urls')),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
    # path('<slug:slug>', FeedMeDetailView.as_view(), name='feed_me_detail'),
    # path('', FeedMeListView.as_view(), name='feed_me_list'),
    # path('feed/rss', RssFeedMeFeeds(), name="feed_me_feed"),  
    # path("", include(snotra_urls)),
    # url(r'', include(snotra_urls))
    # path('feedreader/', include(feedreader_urls)),
    # path('blog/items', lesgv_views.items, name = 'items'),
    # path('blog/posts', lesgv_views.posts, name = 'posts'),
]
