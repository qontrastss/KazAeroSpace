from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
    name = models.CharField(blank=True, null=False, max_length=250)
    coordinate = models.CharField(blank=False, null=True, max_length=250)
    address = models.CharField(blank=True, null=False, max_length=250)


CATEGORIES = (
    ("Телефоны и гаджеты", "Телефоны и гаджеты"),
    ("Компьютеры", "Компьютеры"),
    ("Аудио", "Аудио"),
    ("Телевизоры", "Телевизоры"),
    ("Камеры", "Камеры")
)


class Product(models.Model):
    name = models.CharField(blank=True, null=False, max_length=250)
    model = models.CharField(blank=False, null=True, max_length=150)
    description = models.TextField(blank=True, null=True)
    producer = models.CharField(blank=True, null=True, max_length=150)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=True)
    price = models.IntegerField(blank=True, null=False)
    category = models.CharField(choices=CATEGORIES, blank=True, max_length=100)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=False)
    image = models.CharField(blank=True, null=False, max_length=250)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)
    products = models.ManyToManyField(Product, blank=True, null=False)


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)
    products = models.ManyToManyField(Product, blank=True, null=False)