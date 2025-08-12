from rest_framework import serializers
from .models import Pliego

class PliegoSerializer(serializers.ModelSerializer):
    publicado_por = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Pliego
        fields = '__all__'
        read_only_fields = ['publicado_por', 'fecha_creacion']

class PliegoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pliego
        fields = [
            'titulo', 'tipo_contrato', 'archivo', 
            'fecha_publicacion', 'fecha_cierre',
            'requisitos_tecnicos', 'documentos_obligatorios',
            'criterios_evaluacion'
        ]
        extra_kwargs = {
            'archivo': {'required': True}
        }