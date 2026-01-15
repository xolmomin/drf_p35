
from django.core.validators import FileExtensionValidator
from django.db.models import JSONField, ForeignKey, CASCADE, ImageField, Model
from django.db.models.fields import CharField, PositiveSmallIntegerField, PositiveIntegerField, TextField

from apps.models.base import SlugBaseModel, CreatedBaseModel, upload_image_size_5mb_validator, ImageBaseModel


class Category(SlugBaseModel, ImageBaseModel):
    name = CharField(max_length=255)
    banner = ImageField(upload_to='categories/banner/%Y/%m/%d',
                        validators=[FileExtensionValidator(['jpeg', 'jpg', 'png', 'webp']),
                                    upload_image_size_5mb_validator],
                        help_text='jpg, png, webp are allowed', blank=True, null=True)


class Product(SlugBaseModel, CreatedBaseModel):
    name = CharField(max_length=255)
    price = PositiveIntegerField()
    discount = PositiveSmallIntegerField(db_default=0)
    specification = JSONField(default=dict, blank=True)
    description = TextField(blank=True)
    seller = ForeignKey('apps.User', CASCADE, limit_choices_to={'type': 'seller'}, related_name='products')
    category = ForeignKey('apps.Category', CASCADE, related_name='products')


class ProductImage(ImageBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='products')

