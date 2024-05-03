from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("glasses.users.urls")),
    path("api/", include("glasses.products.urls")),
]
