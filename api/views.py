from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.serializers import ProductSetsSerializer, OrderStatusSerializer, OrderSerializer, RecipientSerializer, \
    RecipientFullNameSerializer, RecipientDeliveryAddressSerializer
from repository.models import ProductSets, Order, Recipient


class ProductSetsViewSet(ReadOnlyModelViewSet):
    queryset = ProductSets.objects.all()
    serializer_class = ProductSetsSerializer


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # Фильтр сделан на основе: https://stackoverflow.com/questions/58837940/django-rest-framework-filter-by-date-range
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ['exact'],
        'delivery_datetime': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'order_created_datetime': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'status': ['exact']
    }

    def update(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

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


class RecipientViewSet(ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer

    __forbidden_fields = ['name', 'surname', 'patronymic', 'delivery_address']

    def partial_update(self, request, *args, **kwargs):
        if self.__is_valid_request(request):
            return Response(
                {'error': 'It is forbidden to update the passed fields'},
                status=status.HTTP_403_FORBIDDEN)

        serializer = RecipientSerializer(self.get_object(), data=request.data, partial=True,
                                         context={'request': request})
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def __is_valid_request(self, request):
        for field in request.data.keys():
            if field in self.__forbidden_fields:
                return True
        return False

    @action(methods=['patch'], detail=True, name='Change full name')
    def full_name(self, request, pk=None):
        serializer = RecipientFullNameSerializer(
            self.get_object(),
            data=request.data,
            partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @action(methods=['patch'], detail=True, name='Change delivery address')
    def delivery_address(self, request, pk=None):
        serializer = RecipientDeliveryAddressSerializer(
            self.get_object(),
            data=request.data)

        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
