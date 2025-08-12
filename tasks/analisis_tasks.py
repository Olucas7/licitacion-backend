from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from services.pliego_analyzer import PliegoAnalyzer
from apps.documents.models import Documento
import PyPDF2

@shared_task(bind=True, max_retries=3)
def analizar_documento_pliego(self, documento_id):
    try:
        documento = Documento.objects.get(id=documento_id)
        documento.estado = 'PROCESANDO'
        documento.save()
        
        texto = self._extraer_texto(documento.archivo.path)
        resultado = PliegoAnalyzer().analizar_documento(documento.pliego, texto)
        
        documento.resultado_analisis = resultado
        documento.porcentaje_cumplimiento = resultado.get('cumplimiento_general', 0)
        documento.estado = 'PROCESADO'
        documento.save()
        
        return {'documento_id': str(documento.id), 'estado': 'completado'}
        
    except ObjectDoesNotExist as e:
        self.retry(exc=e, countdown=60)
    except Exception as e:
        documento.estado = 'ERROR'
        documento.save()
        self.retry(exc=e, countdown=120)

    def _extraer_texto(self, ruta_archivo):
        with open(ruta_archivo, 'rb') as f:
            lector = PyPDF2.PdfReader(f)
            return " ".join([p.extract_text() for p in lector.pages if p.extract_text()])