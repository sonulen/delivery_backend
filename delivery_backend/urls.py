from rest_framework.routers import DefaultRouter

from api.views import ProductSetsViewSet, OrdersViewSet, RecipientViewSet

router = DefaultRouter()
router.register(r'product-sets', ProductSetsViewSet)
router.register(r'orders', OrdersViewSet)
router.register(r'recipients', RecipientViewSet)
urlpatterns = router.urls
