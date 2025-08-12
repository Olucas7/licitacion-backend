import openai
import json
from django.conf import settings

class PliegoAnalyzer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    def analizar_pliego(self, texto):
        prompt = f"""
        Extrae información estructurada de este pliego de licitación:
        
        {texto[:10000]}
        
        Devuelve JSON con:
        - tipo_contrato (OBRA/SERVICIO/SUMINISTRO)
        - fecha_publicacion (YYYY-MM-DD)
        - fecha_cierre (YYYY-MM-DD)
        - requisitos_tecnicos (lista)
        - documentos_obligatorios (lista)
        - criterios_evaluacion (dict con criterio:peso)
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Eres un experto en extraer información de pliegos de licitación"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message['content'])