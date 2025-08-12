from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Documento
from .serializers import DocumentoSerializer

class DocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['pliego', 'estado']
    ordering_fields = ['porcentaje_cumplimiento', 'fecha_subida']