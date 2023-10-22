from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydbname',
        'USER': 'mydbuser',
        'PASSWORD': 'mydbpassword',
        'HOST': 'db',  
        'PORT': '5432',
    }
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
