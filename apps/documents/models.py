from django.db import models
from apps.pliegos.models import Pliego

class Documento(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PROCESANDO', 'Procesando'),
        ('PROCESADO', 'Procesado'),
        ('ERROR', 'Error'),
    )
    
    pliego = models.ForeignKey(Pliego, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='ofertas/')
    nombre_original = models.CharField(max_length=255)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    # Resultados del análisis
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    resultado_analisis = models.JSONField(default=dict, blank=True)
    fecha_procesado = models.DateTimeField(null=True, blank=True)