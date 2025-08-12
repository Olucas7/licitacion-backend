from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pliego
from .serializers import PliegoSerializer
from tasks.pliego_tasks import procesar_pliego_async

class PliegoViewSet(viewsets.ModelViewSet):
    queryset = Pliego.objects.all()
    serializer_class = PliegoSerializer
    
    def perform_create(self, serializer):
        pliego = serializer.save(subido_por=self.request.user)
        import pdb; pdb.set_trace()
        procesar_pliego_async.delay(str(pliego.id))
    
    @action(detail=True, methods=['post'])
    def subir_documentos(self, request, pk=None):
        import pdb; pdb.set_trace()
        pliego = self.get_object()
        archivos = request.FILES.getlist('archivos')
        
        documentos = []
        for archivo in archivos:
            doc = pliego.documentos.create(
                archivo=archivo,
                nombre_original=archivo.name
            )
            documentos.append(doc)
            from tasks.documento_tasks import analizar_documento_async
            analizar_documento_async.delay(str(doc.id))
        
        return Response({
            'mensaje': f'{len(documentos)} documentos subidos para análisis',
            'documentos': documentos
        }, status=status.HTTP_201_CREATED)