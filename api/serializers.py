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
        detail = None

        if attrs['name'] == attrs['surname']:
            detail = "Name and surname must be different"
        if attrs['name'] == attrs['patronymic']:
            detail = "Name and patronymic must be different"
        if attrs['surname'] == attrs['patronymic']:
            detail = "Surname and patronymic must be different"

        if detail:
            raise ValidationError(
                detail=detail,
                code=400)

        return attrs


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
