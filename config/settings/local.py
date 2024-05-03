from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += [
    "django_extensions",
    "silk",
]


MIDDLEWARE += [
    "nplusone.ext.django.NPlusOneMiddleware",
    "silk.middleware.SilkyMiddleware",
]

NPLUSONE_RAISE = True
