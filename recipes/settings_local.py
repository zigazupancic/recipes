"""
Django local settings for recipes project.

For offline work (on a local database).

"""

from recipes.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recipes',
        'USER': 'recipesuser',
        'PASSWORD': 'recipespass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
