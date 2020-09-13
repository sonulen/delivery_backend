from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.serializers import ProductSetsSerializer, OrderStatusSerializer, OrderSerializer
from repository.models import ProductSets, Order


class ProductSetsViewSet(ReadOnlyModelViewSet):
    queryset = ProductSets.objects.all()
    serializer_class = ProductSetsSerializer


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def destroy(self, request, pk=None, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['patch'], name='Change Status')
    def status(self, request, pk=None):
        serializer = OrderStatusSerializer(
            self.get_object(),
            data=request.data,
            partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)
