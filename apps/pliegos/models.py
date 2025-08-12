from django.db import models
from django.conf import settings
import uuid

class Pliego(models.Model):
    TIPO_CONTRATO_CHOICES = [
        ('OBRA', 'Obra Pública'),
        ('SERVICIO', 'Servicio'),
        ('SUMINISTRO', 'Suministro'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=512)
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES)
    archivo = models.FileField(upload_to='pliegos/')
    fecha_publicacion = models.DateField()
    fecha_cierre = models.DateField()
    requisitos_tecnicos = models.JSONField(default=list)
    documentos_obligatorios = models.JSONField(default=list)
    criterios_evaluacion = models.JSONField(default=dict)
    publicado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_contrato_display()})"