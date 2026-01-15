# from django.contrib.auth.hashers import make_password
# from rest_framework.exceptions import ValidationError
# from rest_framework.fields import CharField
# from rest_framework.serializers import ModelSerializer, Serializer
#
# from apps.models import Category, Product, User, Order
#
#
# class RegisterModelSerializer(ModelSerializer):
#     password = CharField(max_length=255, write_only=True)
#     confirm_password = CharField(max_length=255, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'phone', 'password', 'confirm_password']
#
#     def validate_username(self, value: str):
#         if not value.isalpha():
#             raise ValidationError('Invalid username!')
#         return value
#
#     def validate_phone(self, value: str):
#         if not value.startswith('+') or len(value) != 13:
#             raise ValidationError('Invalid phone!')
#         return value
#
#     def validate(self, data):
#         password = data.get('password')
#         confirm_password = data.pop('confirm_password', None)
#         if password != confirm_password:
#             raise ValidationError('Passwords do not match!')
#         data['password'] = make_password(password)
#         return data
#
#
# class CategoryModelSerializer(ModelSerializer):
#     address = CharField(max_length=255, default='valijon', read_only=True)
#
#     class Meta:
#         model = Category
#         # fields = '__all__'
#         fields = ['id', 'name', 'address']
#         # exclude = ['name']
#
#         read_only_fields = []
#         # extra_kwargs = {
#         #     'address': {'write_only': True}
#         # }
#
#     def validate_name(self, value):
#         if value.startswith('vali'):
#             raise ValidationError('Vali deb saqlamaymiz!')
#         return value
#
#     def to_representation(self, instance):
#         repr = super().to_representation(instance)
#         repr['plus_id'] = instance.pk * 2
#
#         return repr
#
#
# class ProductListModelSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', 'discount', 'in_stock']
#
#
# class ProductCreateModelSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', 'discount', 'quantity', 'category']
#
#
# class UserModelSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'username', 'phone']
#
#
# class OrderModelSerializer(ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
