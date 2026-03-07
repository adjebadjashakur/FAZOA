from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-hkzaxd$28h*3teff@6n4al4!mlk+dng&ij(0#es3u5vpm0ks6-')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition
INSTALLED_APPS = [
    # ⚠️ Jazzmin DOIT être avant django.contrib.admin
    'jazzmin',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'django_filters',

    # Local apps
    'apps.users',
    'apps.clients',
    'apps.commandes',
    'apps.stock',
    'apps.production',
    'apps.ressources',
    'apps.reporting',
    'apps.dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ⚠️ WhiteNoise DOIT être juste après SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==============================================================================
# JAZZMIN CONFIG
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "Fazao Admin",
    "site_header": "Fazao",
    "site_brand": "Fazao Manager",
    # "site_logo": "images/logo.png",
    # "site_icon": "images/favicon.ico",
    "welcome_sign": "Bienvenue sur Fazao Manager",
    "copyright": "Fazao © 2026",

    # ✅ Une seule barre de recherche (1 modèle = 1 zone)
    "search_model": ["users.User"],

    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Voir le site", "url": "/", "new_window": True},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    "order_with_respect_to": [
        "users",
        "clients",
        "commandes",
        "production",
        "stock",
        "ressources",
        "reporting",
        "auth",
    ],

    "icons": {
        "auth":                     "fas fa-users-cog",
        "auth.Group":               "fas fa-users",
        "users.User":               "fas fa-user-tie",
        "clients.Client":           "fas fa-handshake",
        "commandes.Commande":       "fas fa-shopping-cart",
        "production.Production":    "fas fa-industry",
        "stock.Stock":              "fas fa-boxes",
        "ressources.Ressource":     "fas fa-tools",
        "reporting.Report":         "fas fa-chart-bar",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": True,

    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    # ✅ Navbar bleue (primary)
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark navbar-primary",
    "no_navbar_border": True,
    "navbar_fixed": True,

    "layout_boxed": False,
    "footer_fixed": False,

    # ✅ Sidebar bleue foncée
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,

    # ✅ Thème clair/blanc pour le contenu principal
    "theme": "sandstone",
    "dark_mode_theme": None,

    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
}
# ==============================================================================
# URLS & TEMPLATES
# ==============================================================================
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ==============================================================================
# DATABASE
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'fazao_db'),
        'USER': os.getenv('DB_USER', 'shakur'),
        'PASSWORD': os.getenv('DB_PASSWORD', '2184'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# ==============================================================================
# AUTH & PASSWORDS
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard:dashboard'
LOGOUT_REDIRECT_URL = 'users:login'


# ==============================================================================
# MESSAGES
# ==============================================================================
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG:   'debug',
    messages.INFO:    'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR:   'danger',
}


# ==============================================================================
# INTERNATIONALISATION
# ==============================================================================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Lome'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
