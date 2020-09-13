from rest_framework.routers import DefaultRouter

from api.views import ProductSetsViewSet, OrdersViewSet

router = DefaultRouter()
router.register(r'product-sets', ProductSetsViewSet)
router.register(r'orders', OrdersViewSet)
urlpatterns = router.urls
