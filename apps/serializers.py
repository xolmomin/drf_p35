from rest_framework.serializers import ModelSerializer

from apps.models import Category, Product, User, Order


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'phone']


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
