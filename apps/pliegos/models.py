from django.db import models
from django.conf import settings
import uuid

class Pliego(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=512, default='Pliego')
    archivo = models.FileField(upload_to='pliegos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Campos que serán llenados por IA
    tipo_contrato = models.CharField(max_length=50, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)
    requisitos_tecnicos = models.JSONField(default=list, blank=True)
    documentos_obligatorios = models.JSONField(default=list, blank=True)
    criterios_evaluacion = models.JSONField(default=dict, blank=True)
    metadata_pliego = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.titulo