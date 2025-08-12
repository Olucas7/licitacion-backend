from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PliegoViewSet

router = DefaultRouter()
router.register(r'', PliegoViewSet, basename='pliego')

urlpatterns = [
    path('<uuid:pk>/subir_documentos/', PliegoViewSet.as_view({'post': 'subir_documentos'}), name='pliego-subir-documentos'),
] + router.urls