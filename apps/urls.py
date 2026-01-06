from django.urls import path

from apps.views import CategoryRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView, ProductListCreateAPIView, \
    ProductRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('products/', ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view()),
]
