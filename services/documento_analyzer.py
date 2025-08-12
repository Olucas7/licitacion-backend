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

        DOCUMENTOS OBLIGATORIOS:
        {self.pliego.documentos_obligatorios}

        CRITERIOS EVALUACION:
        {self.pliego.criterios_evaluacion}
        
        DOCUMENTO:
        {texto[:10000]}
        
        Devuelve JSON con:
        - precio (cantidad dolares)
        - ⁠ruc (identificador unico de la empresa)
        - precio_propuesto (float)
        - plazo (numero de días)
        - tiempo_experiencia (numero de años)
        - tiempo_garantia (numero de años)
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un analista de ofertas de licitación de la industria de construcción"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message['content'])