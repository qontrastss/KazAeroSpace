from django.urls import path

from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view()),
    # path('products/map/', ProductByMapListView.as_view()),
    path('products/<int:pk>/', ProductView.as_view()),

    path('search/', get_similar_words),

    path('favorites/add/<int:pk>/', add_favorites),
    path('favorites/', FavoriteListView.as_view()),

    path('cart/add/<int:pk>/', add_cart),
    path('cart/', CartListView.as_view()),
]