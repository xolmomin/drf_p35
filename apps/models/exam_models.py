from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

# --- UTILS & VALIDATORS ---
uz_phone_validator = RegexValidator(
    regex=r'^(\+998|998)?[0-9]{9}$',
    message="Telefon raqam +998901234567 formatida bo‘lishi kerak"
)


def upload_image_size_5mb_validator(obj):
    if obj.size > 5 * 1024 * 1024:
        raise ValidationError('Rasm hajmi 5MB dan oshmasligi kerak')


# --- BASE MODELS ---
class SlugBaseModel(models.Model):
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            if hasattr(self, 'name'):
                self.slug = slugify(self.name)
            elif hasattr(self, 'title'):
                self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ImageBaseModel(models.Model):
    image = models.ImageField(
        upload_to='images/%Y/%m/%d',
        null=True, blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), upload_image_size_5mb_validator]
    )

    class Meta:
        abstract = True


class CreatedBaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# --- MAIN MODELS ---

class User(AbstractUser):
    class Type(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        SELLER = 'seller', 'Seller'
        MANAGER = 'manager', 'Manager'

    phone = models.CharField(max_length=15, validators=[uz_phone_validator], unique=True)
    type = models.CharField(max_length=25, choices=Type.choices, default=Type.USER)
    birth_date = models.DateField(null=True, blank=True)

    username = None
    USERNAME_FIELD = 'phone'


class Category(SlugBaseModel, ImageBaseModel, MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('apps.User', models.CASCADE, related_name='sellers')


class Product(SlugBaseModel, CreatedBaseModel):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    discount = models.PositiveSmallIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)  # Ombordagi soni
    description = models.TextField(blank=True)
    seller = models.ForeignKey('apps.Seller', models.CASCADE, related_name='products')
    category = models.ForeignKey('apps.Category', models.CASCADE, related_name='products')


class ProductImage(ImageBaseModel):
    product = models.ForeignKey('apps.Product', models.CASCADE, related_name='images')


class Cart(models.Model):
    user = models.OneToOneField('apps.User', models.CASCADE, related_name='cart')


class CartItem(models.Model):
    cart = models.ForeignKey('apps.Cart', models.CASCADE, related_name='items')
    product = models.ForeignKey('apps.Product', models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Favorite(models.Model):
    user = models.ForeignKey('apps.User', models.CASCADE, related_name='favorites')
    product = models.ForeignKey('apps.Product', models.CASCADE, related_name='favored_by')
