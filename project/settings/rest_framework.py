from datetime import timedelta

# Rest Framework Configuration
# Docs: https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# Rest Framework SimpleJWT Configuration
# Docs: https://django-rest-framework-simplejwt.readthedocs.io/

# if DEBUG:
#     SIMPLE_JWT = {
#         'ACCESS_TOKEN_LIFETIME': timedelta(weeks=200),
#     }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(weeks=200),
}