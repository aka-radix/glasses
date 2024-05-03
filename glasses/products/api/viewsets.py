from django.db import models
from rest_framework import permissions, viewsets

from glasses.products.models import Currency, Frame, Lens

from .serializers import FrameSerializer, LensSerializer


class BaseProductViewSet(viewsets.ModelViewSet):
    """Base viewset containing shared permission and queryset retrieval."""

    queryset = models.QuerySet()

    def get_queryset(self):  # type: ignore
        currency = getattr(self.request.user, "currency", Currency.USD)
        return self.queryset.filter(currency=currency)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class FrameViewSet(BaseProductViewSet):
    queryset = Frame.objects.filter(status=Frame.Status.ACTIVE, stock__gte=1)
    serializer_class = FrameSerializer


class LensViewSet(BaseProductViewSet):
    queryset = Lens.objects.filter(stock__gte=1)
    serializer_class = LensSerializer
