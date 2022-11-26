from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .models import Product, Favorites, Cart
from .serializers import ProductShortSerializer, ProductDetailedSerializer


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductShortSerializer

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        return Product.objects.filter(Q(name__icontains=query)) if query else Product.objects.all()

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductByMapListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductShortSerializer

    def get_queryset(self):
        coordinate = self.request.data.get('coordinate', None)
        distance = self.request.data.get('distance', None)

        coordinate

        Product.objects.all()


class ProductView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductDetailedSerializer
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def get_similar_words(request):
    import difflib
    word = request.data.get('word', None)
    if word:
        model_list = Product.objects.all().values_list('model', flat=True)
        result = difflib.get_close_matches(word, model_list, 3, 0.5)
    else:
        result = []
    return Response(result, HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_favorites(request, pk):
    product = Product.objects.filter(id=pk).first()
    favorite = Favorites.objects.filter(user=request.user).first()
    if not favorite:
        favorite = Favorites.objects.create(user=request.user)
    if product not in favorite.products.all():
        favorite.products.add(product)
    else:
        favorite.products.remove(product)
    return Response(HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_cart(request, pk):
    product = Product.objects.filter(id=pk).first()
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)
    if product not in cart.products.all():
        cart.products.add(product)
    else:
        cart.products.remove(product)
    return Response(HTTP_200_OK)


class FavoriteListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductShortSerializer

    def get_queryset(self):
        favorite = Favorites.objects.filter(user=self.request.user).first()
        return favorite.products.all() if favorite else None

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductShortSerializer

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user).first()
        return cart.products.all() if cart else None

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)