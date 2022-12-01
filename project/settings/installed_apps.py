# Application definition

DJANGO_BUILT_IN_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",  # pip install django-cors-headers
    "rest_framework",  # pip install djangorestframework
    "rest_framework_simplejwt",  # pip install djangorestframework-simplejwt,
]

PROJECT_APPS = [
    "apps.base_app",
    "apps.user_profile",
    "apps.groups",
    "apps.notes",
]

INSTALLED_APPS = DJANGO_BUILT_IN_APPS + THIRD_PARTY_APPS + PROJECT_APPS
