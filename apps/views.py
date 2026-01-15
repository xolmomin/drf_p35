# from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import extend_schema
# from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
#     GenericAPIView
# from rest_framework.pagination import LimitOffsetPagination, CursorPagination
# from rest_framework.response import Response
# from rest_framework.throttling import AnonRateThrottle
# from rest_framework.views import APIView
#
# from apps.filters import UserFilterSet, OrderFilterSet
# from apps.models import Category, Product, User, Order
# from apps.paginations import CustomPageNumberPagination, CustomCursorPagination
# from apps.serializers import CategoryModelSerializer, ProductListModelSerializer, UserModelSerializer, \
#     OrderModelSerializer, \
#     RegisterModelSerializer, ProductCreateModelSerializer
#
#
# class RegisterAPIView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterModelSerializer
#
#     def perform_create(self, serializer):
#         serializer.save()
#         # send_email # celery
#
#
# @extend_schema(tags=['products'])
# class CategoryListCreateAPIView(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializer
#     pagination_class = None
#     throttle_classes = [AnonRateThrottle]
#
#
# @extend_schema(tags=['products'])
# class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializer
#
#
# @extend_schema(tags=['products'])
# class ProductListCreateAPIView(ListCreateAPIView):
#     queryset = Product.objects.order_by('id')
#     serializer_class = ProductListModelSerializer
#     filter_backends = DjangoFilterBackend, OrderingFilter, SearchFilter
#     filterset_fields = ['category_id']
#     # filterset_class = ProductFilterSet
#     pagination_class = CustomCursorPagination
#     # search_fields = ("name", "category__name")
#     # ordering_fields = 'price', 'id'
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             self.serializer_class = ProductCreateModelSerializer
#         return super().get_serializer_class()
#
#
#
# @extend_schema(tags=['products'])
# class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListModelSerializer
#
#
#
# @extend_schema(tags=['users'])
# class UserListAPIView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserModelSerializer
#     # filterset_fields = ['is_superuser', 'is_staff']
#     filterset_class = UserFilterSet
#     pagination_class = CustomPageNumberPagination
#
#
# @extend_schema(tags=['orders'])
# class OrderListAPIView(ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderModelSerializer
#     # filterset_fields = ['is_superuser', 'is_staff']
#     filterset_class = OrderFilterSet
