from django.core.validators import FileExtensionValidator
from django.db.models import ForeignKey, CASCADE, ImageField
from django.db.models.fields import CharField

from apps.models.base import SlugBaseModel, CreatedBaseModel, upload_image_size_5mb_validator, ImageBaseModel


class Seller(SlugBaseModel, CreatedBaseModel):
    name = CharField(max_length=255)
    owner = ForeignKey('apps.User', CASCADE)
    address = CharField(max_length=255)


class Manufacturer(CreatedBaseModel, ImageBaseModel):
    name = CharField(max_length=255)
