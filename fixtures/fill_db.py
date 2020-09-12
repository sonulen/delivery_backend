from datetime import timedelta
from random import randint

from django.utils import timezone

from fixtures.food_boxes_stubs import FoodBoxes
from fixtures.recipient_stubs import Recipients
from repository.models import ProductSets, Recipient, Order


def eraseDataBase():
    Order.objects.all().delete()
    ProductSets.objects.all().delete()
    Recipient.objects.all().delete()
    print("All object deleted!")


def fillOrder():
    product_count = ProductSets.objects.count()

    if product_count == 0:
        return

    for recipient in Recipient.objects.all():
        product = ProductSets.objects.all()[randint(0, product_count - 1)]

        Order.objects.create(
            delivery_datetime=timezone.now() + timedelta(hours=1),
            recipient=recipient,
            product_set=product
        )


def fillRecipients(recipients):
    for recipient in recipients:
        Recipient.objects.create(
            surname=recipient['info']['surname'],
            name=recipient['info']['name'],
            patronymic=recipient['info']['patronymic'],
            phone_number=recipient['contacts']['phoneNumber'],
            delivery_address=recipient['address']
        )


def fillFoodBoxes(boxes):
    for box in boxes:
        ProductSets.objects.create(
            title=box['name'],
            description=box['about']
        )


def fillDbWithFixtures():
    food_boxes_json = FoodBoxes().request()
    if food_boxes_json:
        fillFoodBoxes(food_boxes_json)

    recipients_json = Recipients().request()
    if recipients_json:
        fillRecipients(recipients_json)

    if food_boxes_json and recipients_json:
        fillOrder()


# ./manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 --format json > db.json
def fill():
    print("Очистить db? [y/n]")
    if "y" == input():
        eraseDataBase()
    fillDbWithFixtures()


def printDb():
    for product in ProductSets.objects.all():
        print(product)
    for recipient in Recipient.objects.all():
        print(recipient)
    for order in Order.objects.all():
        print(order)
