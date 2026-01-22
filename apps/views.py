from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    GenericAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination, CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from random import randint

from apps.models import Region, District, Category, User, Seller
#
# from apps.filters import UserFilterSet, OrderFilterSet
# from apps.models import Category, Product, User, Order
# from apps.paginations import CustomPageNumberPagination, CustomCursorPagination
from apps.serializers import RegionModelSerializer, \
    DistrictModelSerializer, \
    CategoryModelSerializer, \
    CustomTokenObtainPairSerializer, \
    UserModelSerializer, \
    SellerModelSerializer  # CategoryModelSerializer, ProductListModelSerializer, UserModelSerializer, \
from apps.tasks import send_sms_code


class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionModelSerializer
    pagination_class = None


class DistrictListAPIView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictModelSerializer
    filter_backends = DjangoFilterBackend,
    filterset_fields = 'region_id',
    pagination_class = None


class UserCheckPhoneAPIView(APIView):
    def get(self, request, phone):
        is_exists = User.objects.filter(phone=phone).exists()
        if not is_exists:
            code = randint(100000, 999999)
            send_sms_code.enqueue(phone, code)

        return Response({'data': {'is_exists': is_exists}})


class UserGetMeRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = IsAuthenticated,

    def get_object(self):
        return self.request.user


class UserRegisterCreateAPIView(CreateAPIView):
    pass


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
@extend_schema(tags=['products'])
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = None
    permission_classes = IsAuthenticated,


class SellerCreateAPIView(CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerModelSerializer
    permission_classes = IsAuthenticated,


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
