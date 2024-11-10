from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=#*s%lbx2t&h25-na0nkkztdzf4qi+=gl9t46kd2l2yg2se4on"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "media/"

# STATICFILES_DIRS = [
#     os.path.join(PROJECT_DIR, "static"),
# ]

INSTALLED_APPS = ["debug_toolbar"] + INSTALLED_APPS

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

# import socket  # only if you haven't already imported this
# hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
# INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "172.19.168.52","172.19.168.1"]
# INTERNAL_IPS = ("172.19.168.1")


DEBUG_PROPAGATE_EXCEPTIONS = True
SECRET_KEY = "django-insecure--se+s(y1h)c^0(b2!sadfsadfsafasdfsafddd$3na2)8!$-i24"

if DEBUG:

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
    SHOW_TOOLBAR_CALLBACK: show_toolbar
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]
    RENDER_PANELS = True
    INTERNAL_IPS = ["127.0.0.1", "localhost", "::1", "localhost:8000", "127.0.0.1:8000"]


try:
    from .local import *
except ImportError:
    pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "django-debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
