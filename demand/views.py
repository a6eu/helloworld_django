from django.shortcuts import render
from rest_framework.generics import *

from .models import Demand
from .serializers import *

from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_staff

        return True


class DemandView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    permission_classes = [AdminOnly]

    queryset = Demand.objects.all()
    serializer_class = DemandListCreateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)