MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # https://pypi.org/project/django-cors-headers/
    "corsheaders.middleware.CorsMiddleware",  # doc manda botar antes de CommonMiddleware # TODO: Ver maneira de fazer isso dinamicamente, igual fiz no debug toolbar
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
