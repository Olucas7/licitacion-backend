from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Pliego
from .serializers import PliegoSerializer, PliegoCreateSerializer
from apps.documents.serializers import DocumentoSerializer

class PliegoViewSet(viewsets.ModelViewSet):
    queryset = Pliego.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return PliegoCreateSerializer
        return PliegoSerializer
    
    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)
    
    @action(detail=True, methods=['post'])
    def subir_documentos(self, request, pk=None):
        pliego = self.get_object()
        archivos = request.FILES.getlist('archivos')
        
        documentos_creados = []
        for archivo in archivos:
            documento = pliego.documentos.create(
                archivo=archivo,
                nombre_original=archivo.name
            )
            documentos_creados.append(documento)
            from tasks.analisis_tasks import analizar_documento_pliego
            analizar_documento_pliego.delay(str(documento.id))
        
        return Response({
            'mensaje': f'{len(documentos_creados)} documentos subidos para análisis',
            'documentos': DocumentoSerializer(documentos_creados, many=True).data
        }, status=status.HTTP_201_CREATED)