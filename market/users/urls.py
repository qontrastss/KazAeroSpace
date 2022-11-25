from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('auth/', UserAuthView.as_view()),
    path('register/', UserRegisterView.as_view())
]