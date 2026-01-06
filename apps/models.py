from django.db.models import CharField, Model, IntegerField, ImageField, ForeignKey, CASCADE


class Category(Model):
    name = CharField(max_length=255)


class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField(default=1_000)
    image = ImageField(upload_to='products/%Y/%m/%d')
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
