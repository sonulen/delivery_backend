from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField
from rest_framework.serializers import ModelSerializer

from repository.models import ProductSets, Recipient, Order


class ProductSetsSerializer(ModelSerializer):
    class Meta:
        model = ProductSets
        fields = '__all__'


class RecipientSerializer(ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'

    def validate_phone_number(self, number: str):
        import phonenumbers
        from phonenumbers import NumberParseException

        try:
            phone = phonenumbers.parse(number, None)
        except NumberParseException as e:
            raise ValidationError(detail=str(e), code=400)
        else:
            if not phonenumbers.is_possible_number(phone):
                raise ValidationError(
                    detail="Impossible phone number",
                    code=400)
            if not phonenumbers.is_valid_number(phone):
                raise ValidationError(
                    detail="Invalid phone number",
                    code=400)
            return number

    def validate(self, attrs):
        from api.utils import validate_name
        return validate_name(attrs)


class RecipientDeliveryAddressSerializer(ModelSerializer):
    class Meta:
        model = Recipient
        fields = [
            'id',
            'delivery_address',
        ]


class RecipientFullNameSerializer(ModelSerializer):
    class Meta:
        model = Recipient
        fields = [
            'id',
            'surname',
            'name',
            'patronymic',
        ]

    def validate(self, attrs):
        from api.utils import validate_name
        return validate_name(attrs)


class OrderSerializer(ModelSerializer):
    order_created_datetime = DateTimeField(input_formats=["%d-%m-%YT%H:%M"])
    delivery_datetime = DateTimeField(input_formats=["%d-%m-%YT%H:%M"])

    class Meta:
        model = Order
        fields = '__all__'

    def validate_delivery_datetime(self, delivery_datetime: datetime):
        dt = delivery_datetime - datetime.now(tz=delivery_datetime.tzinfo)
        if dt.seconds < 0:
            raise ValidationError(
                detail='Delivery time is less than actual time',
                code=400)

        return delivery_datetime


class OrderStatusSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
        ]
