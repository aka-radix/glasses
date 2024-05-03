from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("glasses.users.urls")),
    path("api/", include("glasses.products.urls")),
    path("api/", include("glasses.orders.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
