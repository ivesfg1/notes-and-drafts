from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = [
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-middleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

INTERNAL_IPS = [
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
    # ...
    "127.0.0.1",
    # ...
]
