from rest_framework import serializers
from .models import Documento

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
        read_only_fields = ['estado', 'fecha_subida', 'fecha_procesado']

class DocumentoAnalisisSerializer(serializers.ModelSerializer):
    pliego_titulo = serializers.CharField(source='pliego.titulo', read_only=True)
    
    class Meta:
        model = Documento
        fields = [
            'id', 'nombre_original', 'estado', 
            'porcentaje_cumplimiento', 'pliego_titulo',
            'fecha_subida', 'fecha_procesado'
        ]