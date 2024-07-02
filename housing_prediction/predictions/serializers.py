from rest_framework import serializers
from .models import RegionData

class RegionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionData
        fields = '__all__'