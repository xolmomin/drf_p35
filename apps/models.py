from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Model, IntegerField, ImageField, ForeignKey, CASCADE, TextChoices, DateTimeField


class Category(Model):
    name = CharField(max_length=255)


class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField(default=1_000)
    image = ImageField(upload_to='products/%Y/%m/%d')
    category = ForeignKey('apps.Category', CASCADE, related_name='products')


class Order(Model):
    class Status(TextChoices):
        DELIVERING = 'delivering', 'Delivering'
        CANCELED = 'canceled', 'Canceled'
        DELIVERED = 'delivered', 'Delivered'

    owner = ForeignKey('apps.User', CASCADE, related_name='orders')
    status = CharField(max_length=255, choices=Status.choices, default=Status.DELIVERING)
    created_at = DateTimeField(auto_now_add=True)


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        MANAGER = 'manager', 'Manager'

    phone = CharField(max_length=25)
    balance = IntegerField(default=0)
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER)
