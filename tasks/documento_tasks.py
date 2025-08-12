from celery import shared_task
from apps.documents.models import Documento
from services.documento_analyzer import DocumentoAnalyzer
import PyPDF2
from django.utils import timezone

@shared_task
def analizar_documento_async(documento_id):
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

def extraer_texto_pdf(ruta):
    with open(ruta, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        return "\n".join([page.extract_text() for page in pdf.pages])