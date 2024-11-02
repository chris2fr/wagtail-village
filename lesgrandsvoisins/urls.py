from django.conf import settings
from django.conf.urls.i18n import i18n_patterns # Pour la localisation
from django.contrib import admin
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_transfer import urls as wagtailtransfer_urls # for Wagtail-Transfer

from .forms import RegistrationForm

from dotenv import load_dotenv # Pour les variables d'.env
# Prendre les variables d'environnement
load_dotenv()

from search import views as search_views
from lesgv import views as lesgv_views
from lesgrandsvoisins import views as lesgrandsvoisins_views

urlpatterns = [
  path("registrationform/", lesgrandsvoisins_views.registrationform_view,name="registrationform_view"),
  path("django-admin/", admin.site.urls),
  # path("admin/", include(wagtailadmin_urls)),
  path("cms-admin/", include(wagtailadmin_urls)), # Sites-Faciles préfère ceci
  path('accounts/', include('allauth.urls')),
  path("documents/", include(wagtaildocs_urls)),
  path("search/", search_views.search, name="search"),
  path("wagtail-transfer/", include(wagtailtransfer_urls)), # Pour Wagtail Transfer
  path('htmlmenu', lesgv_views.htmlmenu), # Ajouté
]     

if settings.DEBUG_TOOLBAR:
  urlpatterns += [
    path("__debug__/", include("debug_toolbar.urls")),
  ]

if settings.DEBUG:
  from django.conf.urls.static import static
  from django.contrib.staticfiles.urls import staticfiles_urlpatterns

  # Serve static and media files from development server
  urlpatterns += staticfiles_urlpatterns()
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns( # Pour l'internationalisation de Wagtail_Village et Wagtail_Village_Blog
  path("", include("wagtail_village.urls")),
  path("", include("wagtail_village_blog.urls", namespace="wagtail_village_blog")),
  prefix_default_language=True,
)

urlpatterns = urlpatterns + [
  # path("", include('allauth.urls')),
  
  # For anything not caught by a more specific rule above, hand over to
  # Wagtail's page serving mechanism. This should be the last pattern in
  # the list:
  path("", include(wagtail_urls)),
  # Alternatively, if you want Wagtail pages to be served from a subpath
  # of your site, rather than the site root:
  #  path("pages/", include(wagtail_urls)),
]


