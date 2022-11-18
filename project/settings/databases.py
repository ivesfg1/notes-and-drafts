from .base import BASE_DIR, get_variable_from_env

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": get_variable_from_env("DATABASE_ENGINE"),
        "NAME": get_variable_from_env("DATABASE_NAME"),
        "USER": get_variable_from_env("DATABASE_USER"),
        "PASSWORD": get_variable_from_env("DATABASE_PASSWORD"),
        "HOST": get_variable_from_env("DATABASE_HOST"),
        "PORT": get_variable_from_env("DATABASE_PORT"),
    }
}
