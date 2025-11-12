from rest_framework import serializers
from .models import EnvironmentalData

class EnvironmentalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalData
        fields = '__all__' 
