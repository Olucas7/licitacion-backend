from rest_framework import serializers
from .models import Pliego

class PliegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pliego
        fields = ['id', 'titulo', 'archivo', 'fecha_subida', 'subido_por']
        read_only_fields = ['fecha_subida', 'subido_por']

class PliegoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pliego
        fields = '__all__'