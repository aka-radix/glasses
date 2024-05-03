from rest_framework.routers import DefaultRouter

from glasses.orders.api.viewsets import (
    BasketViewSet,
    OrderViewSet,
    PurchaseViewSet,
)

router = DefaultRouter()
router.register(r"basket", BasketViewSet, basename="basket")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"purchases", PurchaseViewSet, basename="purchases")
urlpatterns = router.urls
