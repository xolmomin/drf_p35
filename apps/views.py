from django.db.models import Subquery
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, \
    RetrieveAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.models import Region, District, Category, User, Seller, CartItem, Cart, Favorite, Product
#
# from apps.filters import UserFilterSet, OrderFilterSet
# from apps.models import Category, Product, User, Order
# from apps.paginations import CustomPageNumberPagination, CustomCursorPagination
from apps.serializers import RegionModelSerializer, \
    DistrictModelSerializer, \
    CategoryModelSerializer, \
    CustomTokenObtainPairSerializer, \
    UserModelSerializer, \
    SellerModelSerializer, \
    UserRegisterModelSerializer, \
    UserChangePasswordModelSerializer, \
    UserProfileUpdateModelSerializer, \
    CartItemModelSerializer, \
    FavoriteModelSerializer  # CategoryModelSerializer, ProductListModelSerializer, UserModelSerializer, \
from apps.tasks import register_sms


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


@extend_schema(tags=['auth'])
class UserCheckPhoneAPIView(APIView):
    def get(self, request, phone):
        is_exists = User.objects.filter(phone=phone).exists()
        if not is_exists:
            register_sms.enqueue(phone)

        return Response({'data': {'is_exists': is_exists}})


@extend_schema(tags=['users'])
class UserGetMeRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = IsAuthenticated,

    def get_object(self):
        return self.request.user


@extend_schema(tags=['users'])
class UserProfileUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateModelSerializer
    permission_classes = IsAuthenticated,
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user


@extend_schema(tags=['users'])
class UserChangePasswordUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordModelSerializer
    permission_classes = IsAuthenticated,
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True})


@extend_schema(tags=['auth'])
class UserRegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer


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

class FavoriteListAPIView(ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class FavoriteDestroyAPIView(DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


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


@extend_schema(tags=['users'])
class CartItemListAPIView(ListCreateAPIView):
    queryset = CartItem.objects.select_related('product', 'product__seller')
    serializer_class = CartItemModelSerializer
    pagination_class = None
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        serializer.save(cart=cart)


@extend_schema(tags=['users'])
class CartItemUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemModelSerializer
    permission_classes = IsAuthenticated,
    http_method_names = ['patch', 'delete']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(cart__user=self.request.user)


@extend_schema(tags=['auth'])
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=['auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass
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
