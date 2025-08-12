from celery import shared_task
from apps.documentos.models import Documento
from services.documento_analyzer import DocumentoAnalyzer
import PyPDF2

@shared_task(bind=True, max_retries=3)
def analizar_documento_async(self, documento_id):
    documento = Documento.objects.get(id=documento_id)
    documento.estado = 'PROCESANDO'
    documento.save()
    
    try:
        # Extraer texto
        texto = extraer_texto_pdf(documento.archivo.path)
        
        # Analizar con IA
        analyzer = DocumentoAnalyzer(documento.pliego)
        resultado = analyzer.analizar_documento(texto)
        
        # Guardar resultados
        documento.resultado_analisis = resultado
        documento.estado = 'PROCESADO'
        documento.fecha_procesado = timezone.now()
        documento.save()
        
    except Exception as e:
        documento.estado = 'ERROR'
        documento.save()
        self.retry(exc=e, countdown=60)