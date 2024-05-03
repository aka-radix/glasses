from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .api.viewsets import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
urlpatterns = router.urls

urlpatterns += [
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "token/blacklist/",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
]
