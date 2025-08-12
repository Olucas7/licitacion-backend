import openai
import json
from django.conf import settings

class PliegoAnalyzer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4-1106-preview"
    
    def analizar_documento(self, pliego, texto_documento):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en análisis de licitaciones públicas."
                    },
                    {
                        "role": "user",
                        "content": self._generar_prompt(pliego, texto_documento)
                    }
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message['content'])
        except Exception as e:
            return {"error": str(e)}

    def _generar_prompt(self, pliego, texto):
        return f"""
        Analiza este documento de oferta según el pliego:
        Título: {pliego.titulo}
        Tipo: {pliego.tipo_contrato}
        Requisitos: {pliego.requisitos_tecnicos}
        Criterios: {pliego.criterios_evaluacion}
        
        Documento:
        {texto[:12000]}
        
        Devuelve JSON con:
        - cumplimiento_general (0-100)
        - detalles_tecnicos
        - documentacion_completa (bool)
        - riesgos_detectados
        - recomendacion
        """