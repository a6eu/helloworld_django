from rest_framework import serializers, status
from demand.models import Demand


class DemandListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = '__all__'
