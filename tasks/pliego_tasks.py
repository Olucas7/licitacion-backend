from celery import shared_task
from apps.pliegos.models import Pliego
from services.pliego_analyzer import PliegoAnalyzer
import PyPDF2

@shared_task
def procesar_pliego_async(pliego_id):
    pliego = Pliego.objects.get(id=pliego_id)
    
    # Extraer texto del pliego
    texto = extraer_texto_pdf(pliego.archivo.path)
    
    # Analizar con IA
    analyzer = PliegoAnalyzer()
    resultado = analyzer.analizar_pliego(texto)
    
    # Actualizar pliego con los metadatos
    pliego.tipo_contrato = resultado.get('tipo_contrato')
    pliego.fecha_publicacion = resultado.get('fecha_publicacion')
    pliego.fecha_cierre = resultado.get('fecha_cierre')
    pliego.requisitos_tecnicos = resultado.get('requisitos_tecnicos', [])
    pliego.documentos_obligatorios = resultado.get('documentos_obligatorios', [])
    pliego.criterios_evaluacion = resultado.get('criterios_evaluacion', {})
    pliego.metadata_pliego = resultado
    pliego.save()

def extraer_texto_pdf(ruta):
    with open(ruta, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        return "\n".join([page.extract_text() for page in pdf.pages])