from django.urls import path

from apps.views import RegionListAPIView, DistrictListAPIView, CategoryListCreateAPIView, CustomTokenObtainPairView, \
    UserGetMeRetrieveAPIView, SellerCreateAPIView, UserCheckPhoneAPIView, UserRegisterCreateAPIView, \
    UserChangePasswordUpdateAPIView, UserProfileUpdateAPIView, CartItemListAPIView, CustomTokenRefreshView, \
    CartItemUpdateDestroyAPIView, FavoriteListAPIView, FavoriteDestroyAPIView

# from apps.views import CategoryRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView, ProductListCreateAPIView, \
#     ProductRetrieveUpdateDestroyAPIView, UserListAPIView, OrderListAPIView, RegisterAPIView

urlpatterns = [
    path('regions/', RegionListAPIView.as_view()),
    path('districts/', DistrictListAPIView.as_view()),
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('sellers/', SellerCreateAPIView.as_view()),
    # path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view()),
    # path('products/', ProductListCreateAPIView.as_view()),
    # path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view()),
    #
    # path('users/', UserListAPIView.as_view()),
    # path('orders/', OrderListAPIView.as_view()),
    #
    # path('users/register/', RegisterAPIView.as_view()),

    path('users/get-me/', UserGetMeRetrieveAPIView.as_view(), name='users_get_me'),
    path('users/change-password/', UserChangePasswordUpdateAPIView.as_view(), name='users_change_password'),
    path('users/update/', UserProfileUpdateAPIView.as_view(), name='users_profile_update'),
    path('users/favorites/', FavoriteListAPIView.as_view(), name='favorites'),
    path('users/favorites/<int:pk>', FavoriteDestroyAPIView.as_view(), name='favorites_destroy'),
    path('users/carts/', CartItemListAPIView.as_view(), name='cart_items'),
    path('users/carts/<int:pk>', CartItemUpdateDestroyAPIView.as_view(), name='cart_item_update'),

    path('auth/user-exists/<int:phone>', UserCheckPhoneAPIView.as_view(), name='users_check_phone'),
    path('auth/register/', UserRegisterCreateAPIView.as_view(), name='users_register'),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
