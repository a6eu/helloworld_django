from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from .serializers import *
from .models import *


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class NewsListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    pagination_class = PageNumberPagination

    serializer_class = NewsListCreateSerializer
    queryset = News.objects.select_related('created_by').all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        permission = IsAdminUser()

        if not permission.has_permission(request, self):
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)


class NewsDetailView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):
    pagination_class = PageNumberPagination
    permission_classes = [AdminOnly]

    serializer_class = NewsDetailSerializer
    queryset = News.objects.select_related('created_by')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
