from rest_framework.routers import DefaultRouter

from glasses.products.api.viewsets import FrameViewSet, LensViewSet

router = DefaultRouter()
router.register(r"frames", FrameViewSet, basename="frames")
router.register(r"lenses", LensViewSet, basename="lenses")
urlpatterns = router.urls
