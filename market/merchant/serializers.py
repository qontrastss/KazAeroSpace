from django.db.models import Q
from rest_framework import serializers

from .models import Product, Favorites, Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ('coordinate',)


class ProductShortSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    store = StoreSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category', 'producer', 'model', 'is_favorite', 'store', 'image')

    def get_image(self, obj):
        return obj.productimage_set.all().values_list('image', flat=True)

    def get_is_favorite(self, obj):
        fav_products = Favorites.objects.filter(user=self.context['request'].user).first()
        return True if fav_products and obj in fav_products.products.all() else False


class ProductRecomendSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'model', 'store_name', 'price')

    def get_store_name(self, obj):
        return obj.store.name if obj.store else None


class ProductDetailedSerializer(serializers.ModelSerializer):
    similar_products = serializers.SerializerMethodField()
    store = StoreShortSerializer()

    class Meta:
        model = Product
        fields = '__all__'

    def get_similar_products(self, obj):
        return ProductRecomendSerializer(Product.objects.filter(Q(model__icontains=obj.model)).exclude(id=obj.id), many=True).data

