from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from glasses.orders.api.serializers import (
    BasketSerializer,
    OrderSerializer,
    PurchaseSerializer,
)
from glasses.orders.models import Basket, Order, Purchase


class BasketViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    def get_serializer_context(self):
        return {
            "user": self.request.user,
        }

    def get_object(self) -> Basket:
        return self.queryset.get(user=self.request.user)

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["PATCH"])
    def add(self, *args, **kwargs) -> Response:
        return self.update(*args, **kwargs)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.select_related("purchase").all()
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        return {
            "user": self.request.user,
        }

    def get_queryset(self):  # type: ignore
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["GET"])
    def get_last_order(self) -> Response:
        order = self.get_queryset().last()
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class PurchaseViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):  # type: ignore
        return self.queryset.filter(order__user=self.request.user)
