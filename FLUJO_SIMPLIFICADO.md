# 🔄 Flujo Simplificado - Sistema de Análisis de Licitaciones

## 📋 **Descripción General**

Sistema de **análisis único** donde cada sesión es independiente. No se persisten archivos ni versiones. El flujo tiene un inicio y fin claro durante la sesión de trabajo.

## 🔄 **Flujo de Trabajo**

### **1. Subir Pliego (Documento Base)**
```
Frontend → POST /api/pliegos/upload/
```
- **Entrada**: PDF del pliego + metadatos
- **Proceso**: 
  - Guarda archivo temporalmente
  - Extrae texto con OCR
  - Analiza estructura con IA
  - Define criterios de validación
- **Salida**: Pliego activo para análisis

### **2. Subir Ofertas (Documentos a Analizar)**
```
Frontend → POST /api/documents/upload/
```
- **Entrada**: Múltiples PDFs de ofertas
- **Proceso**:
  - Guarda archivos temporalmente
  - Calcula hash SHA256 (detección duplicados)
  - Encola análisis con IA
  - Compara vs pliego activo
- **Salida**: Ofertas analizadas y validadas

### **3. Panel de Filtros**
```
Frontend → GET /api/offers/
```
- **Funcionalidad**:
  - Lista ofertas válidas
  - Filtros por estado, precio, plazo
  - Ranking por puntuación
  - Selección para comparación

### **4. Comparaciones**
```
Frontend → POST /api/comparisons/
```
- **Entrada**: IDs de ofertas seleccionadas
- **Proceso**:
  - Análisis comparativo con IA
  - Genera resumen ejecutivo
  - Cálculo de indicadores
- **Salida**: Comparación visual + resumen

## 🗂️ **Modelos Simplificados**

### **Pliego**
```python
{
    "id": "uuid",
    "title": "Título del Pliego",
    "temp_path": "/tmp/archivo.pdf",  # Temporal
    "campos_obligatorios": {"oferente": true, "ruc": true},
    "estructura": {"secciones": ["general", "tecnica"]},
    "criterios_eval": {"precio": 0.4, "calidad": 0.6},
    "vigente": true,
    "analysis_data": {},  # Datos extraídos por IA
    "raw_text": "texto extraído del PDF"
}
```

### **Document (Oferta)**
```python
{
    "id": "uuid",
    "original_filename": "oferta_empresa.pdf",
    "temp_path": "/tmp/archivo.pdf",  # Temporal
    "status": "PROCESSED",
    "validation_score": 0.85,
    "is_valid_offer": true,
    "analysis_data": {
        "oferente": "Empresa S.A.",
        "ruc": "12345678",
        "monto": 100000,
        "plazo": 30
    }
}
```

### **Offer (Resultado del Análisis)**
```python
{
    "id": "uuid",
    "oferente": "Empresa S.A.",
    "ruc": "12345678",
    "monto": "100000.00",
    "validation_state": "ACCEPTED",
    "rejection_reason": null,
    "score_rank": 0.85
}
```

## 🔗 **Endpoints Principales**

### **Pliegos**
- `POST /api/pliegos/upload/` - Subir pliego
- `GET /api/pliegos/active/` - Obtener pliego vigente
- `GET /api/pliegos/` - Listar pliegos

### **Documentos (Ofertas)**
- `POST /api/documents/upload/` - Subir ofertas
- `GET /api/documents/{id}/status/` - Estado de análisis
- `GET /api/documents/stats/` - Estadísticas

### **Ofertas (Resultados)**
- `GET /api/offers/` - Lista filtrable
- `POST /api/offers/bulk_action/` - Acciones masivas
- `GET /api/offers/stats/` - Estadísticas

### **Comparaciones**
- `POST /api/comparisons/create_comparison/` - Crear comparación
- `GET /api/comparisons/{id}/analysis/` - Análisis detallado
- `POST /api/comparisons/{id}/generate_summary/` - Resumen IA

## 🧠 **Procesamiento con IA**

### **Análisis de Pliego**
1. **OCR**: Extracción de texto del PDF
2. **Estructura**: Identificación de secciones
3. **Criterios**: Extracción de requisitos y pesos
4. **Validación**: Definición de campos obligatorios

### **Análisis de Ofertas**
1. **OCR**: Extracción de texto
2. **Extracción**: Datos estructurados (oferente, RUC, monto, etc.)
3. **Validación**: Comparación vs pliego
4. **Puntuación**: Cálculo de score de cumplimiento
5. **Clasificación**: Aceptado/Rechazado + razón

### **Comparación**
1. **Análisis**: Comparación lado a lado
2. **Indicadores**: Métricas de comparación
3. **Resumen**: Generación de resumen ejecutivo
4. **Recomendación**: Sugerencias basadas en IA

## 🗑️ **Gestión de Archivos**

### **Almacenamiento Temporal**
- Archivos guardados en `/tmp/`
- Nombres únicos con UUID
- Eliminación automática al finalizar sesión
- No persistencia en S3

### **Limpieza**
- Archivos eliminados al borrar registros
- Limpieza manual disponible
- No acumulación de archivos

## 🔐 **Autenticación**

### **JWT Tokens**
- `POST /api/token/` - Obtener token
- `POST /api/token/refresh/` - Renovar token
- Headers: `Authorization: Bearer <token>`

### **Usuarios**
- `licitacion` / `licitacion123`
- `admin` / `admin123`

## 🚀 **Ventajas del Flujo Simplificado**

1. **Simplicidad**: Sin persistencia compleja
2. **Velocidad**: Procesamiento inmediato
3. **Flexibilidad**: Cada sesión es independiente
4. **Mantenimiento**: Menos complejidad operacional
5. **Escalabilidad**: Fácil de escalar horizontalmente

## 📊 **Métricas de Rendimiento**

- **Tiempo de análisis**: < 30 segundos por oferta
- **Precisión IA**: > 90% en extracción de datos
- **Concurrencia**: Múltiples usuarios simultáneos
- **Almacenamiento**: Temporal, sin acumulación

## 🔧 **Configuración**

### **Variables de Entorno**
```bash
# OpenAI
OPENAI_API_KEY=your_key_here

# Django
SECRET_KEY=your_secret_here
DEBUG=True

# Base de datos
DATABASE_URL=sqlite:///db.sqlite3
```

### **Dependencias**
- Django 4.2+
- DRF 3.14+
- Celery (para procesamiento asíncrono)
- OpenAI (para análisis IA)

## 🎯 **Casos de Uso**

1. **Análisis Rápido**: Evaluación de propuestas en tiempo real
2. **Comparación Inmediata**: Análisis comparativo instantáneo
3. **Validación Automática**: Cumplimiento vs pliego
4. **Resumen Ejecutivo**: Generación automática de reportes
