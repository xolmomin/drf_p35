from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import Region, District, Category, Product, User, Order, Seller


class RegionModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class DistrictModelSerializer(ModelSerializer):
    class Meta:
        model = District
        # fields = '__all__'
        exclude = 'region',


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone']


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
class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', ]

        read_only_fields = []
        # extra_kwargs = {
        #     'address': {'write_only': True}
        # }


class SellerModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Seller
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs) -> dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["data"] = UserModelSerializer(self.user).data

        return data

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
