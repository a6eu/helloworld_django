from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .serializers import *


# Create your views here.
class OrderListView(mixins.ListModelMixin, GenericAPIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.prefetch_related(
        'order_items',
        'order_items__product',
        'order_items__product__brand',
        'payment_status',
    ).all()
    serializer_class = OrderListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.method == 'POST':
            queryset = Order.objects.all()
            return queryset
        elif self.request.method == 'GET':
            user = self.request.user
            # user_db = UserProfile.objects.get(id=18)
            queryset = Order.objects.filter(user=user).prefetch_related(
                'order_items',
                'order_items__product',
                'order_items__product__brand',
                'payment_status'
            ).all()
            return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderWriteSerializers
        return OrderListSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderDetailView(mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = OrderUpdateSerializer
    queryset = Order
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

