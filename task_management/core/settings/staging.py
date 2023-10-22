from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.str('RDS_DB_NAME'),
        'USER': env.str('RDS_USERNAME'),
        'PASSWORD': env.str('RDS_PASSWORD'),
        'HOST': env.str('RDS_HOSTNAME'),
        'PORT': env.str('PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
            # Attempt to improve performance of selects.
            'isolation_level': 'read uncommitted'
        }
    }
}