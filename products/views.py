from django_filters.rest_framework import DjangoFilterBackend
from .filter import ProductFilter
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.filters import SearchFilter
from .serializers import *
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class ProductDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Product.objects.select_related('brand', 'category')
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProductUpdateSerializer
        return ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Product.objects.select_related('brand', 'category')
    serializer_class = ProductSearchCreateSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'article']
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


