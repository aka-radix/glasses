from typing import Union

from django.db import transaction
from rest_framework import serializers

from glasses.orders.models import Basket, Order, Purchase
from glasses.orders.utils import validate_object_exist
from glasses.products.api.serializers import FrameSerializer, LensSerializer
from glasses.products.models import Frame, Lens
from glasses.users.models import User


class GetUserFromContextMixin:
    def get_user_from_context(self) -> User:
        """Make sure the user exists in the context and is retrievable."""

        user = self.context.get("user")  # type: ignore
        if not user:
            raise serializers.ValidationError(
                "User is not found",
            )
        return user


class BasketSerializer(GetUserFromContextMixin, serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = (
            "total",
            "currency",
            "frame",
            "lens",
        )
        read_only_fields = (
            "total",
            "currency",
        )

    def validate_frame(self, frame: Frame) -> Union[Frame, Lens]:
        user = self.get_user_from_context()
        return validate_object_exist(frame, user)

    def validate_lens(self, lens: Lens) -> Union[Lens, Frame]:
        user = self.get_user_from_context()
        return validate_object_exist(lens, user)

    def update(self, instance, validated_data):
        return instance.add_products(validated_data)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ("id", "order", "frame", "lens")


class OrderSerializer(GetUserFromContextMixin, serializers.ModelSerializer):
    purchase = PurchaseSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = ("user",)
        read_only_fields = (
            "total",
            "currency",
            "purchase",
            "user",
        )

    def validate(self, attrs):
        user = self.get_user_from_context()

        basket = user.basket  # type: ignore
        frame = validate_object_exist(basket.frame, user)
        lens = validate_object_exist(basket.lens, user)
        return {
            "frame": frame,
            "lens": lens,
        }

    @transaction.atomic
    def create(self, validated_data) -> Order:
        user = self.get_user_from_context()

        basket = user.basket  # type: ignore

        order = Order()
        order.save()
        order.user = user  # type: ignore

        Purchase.objects.create(
            frame=FrameSerializer(basket.frame).data,
            lens=LensSerializer(basket.lens).data,
            order=order,
        )
        order.save()

        basket.flush()
        return order
