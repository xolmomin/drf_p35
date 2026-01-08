from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination

from apps.filters import UserFilterSet, OrderFilterSet
from apps.models import Category, Product, User, Order
from apps.paginations import CustomPageNumberPagination
from apps.serializers import CategoryModelSerializer, ProductModelSerializer, UserModelSerializer, OrderModelSerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filterset_fields = ['category_id']


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # filterset_fields = ['is_superuser', 'is_staff']
    filterset_class = UserFilterSet
    pagination_class = CustomPageNumberPagination


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    # filterset_fields = ['is_superuser', 'is_staff']
    filterset_class = OrderFilterSet
