from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class FavoritesListView(mixins.ListModelMixin, GenericAPIView):
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FavoritesAddDeleteView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.kwargs['pk']
        product = generics.get_object_or_404(Product, id=product_id)

        if Favorites.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Product is already in favorites.")

        serializer.save(user=user, product=product)

    def perform_destroy(self, instance):
        user = self.request.user
        product = instance.product

        if not Favorites.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Product is not in favorites.")

        instance.delete()