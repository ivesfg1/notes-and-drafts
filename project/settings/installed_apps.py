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
    # "imagekit",  # pip install django-imagekit
]

PROJECT_APPS = [
    "apps.base_app",
    "apps.notes",
]

INSTALLED_APPS = DJANGO_BUILT_IN_APPS + THIRD_PARTY_APPS + PROJECT_APPS

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

# AUTH_USER_MODEL = ""
