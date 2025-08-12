import openai
import json
from django.conf import settings

class DocumentoAnalyzer:
    def __init__(self, pliego):
        self.pliego = pliego
        openai.api_key = settings.OPENAI_API_KEY
    
    def analizar_documento(self, texto):
        prompt = f"""
        Analiza este documento de oferta según el pliego:
        
        REQUISITOS DEL PLIEGO:
        {self.pliego.requisitos_tecnicos}
        
        DOCUMENTO:
        {texto[:10000]}
        
        Devuelve JSON con:
        - cumplimiento_porcentaje (0-100)
        - cumplimiento_requisitos (lista)
        - faltantes (lista)
        - monto_ofertado (float)
        - observaciones (texto)
        - riesgos (lista)
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Eres un analista de ofertas de licitación"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message['content'])