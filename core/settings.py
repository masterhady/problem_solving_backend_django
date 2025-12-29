import os
from pathlib import Path
from decouple import config

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key & Debug
SECRET_KEY = config("SECRET_KEY", default="fallback-secret-key")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=lambda v: [s.strip() for s in v.split(",")] if v else ["*"])
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://*.netlify.app",
    "https://problemsolvingiti.netlify.app",
]
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps بتاعتك هنا 👇
    # "myapp",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # "channels",  # WebSocket support removed
    "api",
]

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL Config
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # 👈 لو هتستخدمي templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ASGI Application for WebSocket support
# ASGI_APPLICATION = "core.asgi.application"

# Channel Layers for WebSocket
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     },
# }


# Password Hashers - Optimized for Development Speed
# Using 1 iteration of PBKDF2 to make login instantaneous in dev
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Reduce iterations for PBKDF2 to 1 (default is 600,000+)
# from django.contrib.auth.hashers import PBKDF2PasswordHasher
# PBKDF2PasswordHasher.iterations = 1

# Database
DB_HOST = config("DB_HOST", default=None)
USE_SQLITE = config("USE_SQLITE", cast=bool, default=False)

# Force Postgres if DB_HOST is provided, even if USE_SQLITE is True
if DB_HOST and not USE_SQLITE:
    print("DEBUG: Using Postgres (DB_HOST detected)")
    try:
        db_host = DB_HOST
        # FIX: Resolve hostname to IPv4 to avoid IPv6 timeouts (saves ~15s)
        import socket
        try:
            db_host = socket.gethostbyname(db_host)
            print(f"Resolved DB_HOST to {db_host} (IPv4)")
        except Exception as e:
            print(f"Could not resolve DB_HOST {db_host}: {e}")

        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": config("DB_NAME", default=""),
                "USER": config("DB_USER", default=""),
                "PASSWORD": config("DB_PASSWORD", default=""),
                "HOST": db_host,
                "PORT": config("DB_PORT", cast=int, default=5432),
                "OPTIONS": {
                    "sslmode": config("DB_SSLMODE", default="require"),
                },
            }
        }
    except Exception as e:
        print(f"Database configuration error: {e}")
        DATABASES = {}
elif USE_SQLITE or not DB_HOST:
    print("DEBUG: Using SQLite")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # This part is now redundant but kept for safety
    DATABASES = {}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Language & Timezone
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# SimpleJWT settings
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),  # Extended to 24 hours for development
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # Extended to 30 days
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Custom user model
AUTH_USER_MODEL = "api.User"
