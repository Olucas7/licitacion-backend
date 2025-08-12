# API Endpoints - Sistema de Licitaciones

## Autenticación

### JWT Token
```
POST /api/token/
POST /api/token/refresh/
```

## Pliegos

### Subir Pliego
```
POST /api/pliegos/upload/
```
**Body (multipart/form-data):**
- `title`: string (requerido)
- `file`: file (requerido)
- `fecha_publicacion`: date (opcional)
- `campos_obligatorios`: JSON (opcional)
- `estructura`: JSON (opcional)
- `garantias_minimas`: decimal (opcional)
- `criterios_eval`: JSON (opcional)

### Obtener Pliego Vigente
```
GET /api/pliegos/active/
```

### Listar Pliegos
```
GET /api/pliegos/
```
**Query Parameters:**
- `vigente`: boolean
- `created_by`: integer
- `search`: string
- `ordering`: string

### Detalle de Pliego
```
GET /api/pliegos/{id}/
```

### Subir Versión de Pliego
```
POST /api/pliegos/{id}/upload_version/
```
**Body (multipart/form-data):**
- `file`: file (requerido)
- `version`: integer (requerido)

### Marcar Pliego como Vigente
```
POST /api/pliegos/{id}/set_active/
```

### Versiones de Pliego
```
GET /api/versions/
GET /api/versions/{id}/
```

## Documentos

### Subida Masiva de Documentos
```
POST /api/documents/upload/
```
**Body (multipart/form-data):**
- `files`: array of files (requerido, máximo 50)
- `pliego_id`: UUID (opcional)

### Listar Documentos
```
GET /api/documents/
```
**Query Parameters:**
- `status`: string (PENDING, PROCESSING, PROCESSED, ERROR)
- `pliego`: UUID
- `uploader`: integer
- `search`: string
- `ordering`: string

### Estado de Documento
```
GET /api/documents/{id}/status/
```

### Estadísticas de Documentos
```
GET /api/documents/stats/
```

### Reintentar Procesamiento
```
POST /api/documents/{id}/retry/
```

### Eliminación Masiva
```
DELETE /api/documents/bulk_delete/
```
**Body:**
- `document_ids`: array of UUIDs

## Ofertas

### Listar Ofertas
```
GET /api/offers/
```
**Query Parameters:**
- `validation_state`: string (ACCEPTED, REJECTED)
- `rejection_reason`: string
- `min_monto`: decimal
- `max_monto`: decimal
- `oferente`: string
- `ruc`: string
- `pliego_id`: UUID
- `ordering`: string (score_rank, monto, created_at, oferente)

### Detalle de Oferta
```
GET /api/offers/{id}/
```

### Estadísticas de Ofertas
```
GET /api/offers/stats/
```

### Recomputar Ranking
```
POST /api/offers/{id}/recompute_rank/
```
**Body:**
- `ranking_criteria`: JSON (opcional)
- `force_recompute`: boolean (opcional)

### Validación Manual
```
POST /api/offers/{id}/validate_manually/
```
**Body:**
- `validation_state`: string (ACCEPTED, REJECTED)
- `rejection_reason`: string (requerido si REJECTED)

### Acciones Masivas
```
POST /api/offers/bulk_action/
```
**Body:**
- `offer_ids`: array of UUIDs
- `action`: string (recompute_rank, export, compare)
- `parameters`: JSON (opcional)

### Exportar Ofertas
```
GET /api/offers/export/
```
**Query Parameters:**
- `format`: string (json, csv, excel)

## Comparaciones

### Crear Comparación
```
POST /api/comparisons/create_comparison/
```
**Body:**
- `offer_ids`: array of UUIDs (mínimo 2, máximo 10)
- `ranking_base`: string (price, score, composite)
- `thresholds`: JSON (opcional)
- `include_summary`: boolean (opcional)

### Listar Comparaciones
```
GET /api/comparisons/
```
**Query Parameters:**
- `created_by`: integer
- `ordering`: string

### Detalle de Comparación
```
GET /api/comparisons/{id}/
```

### Generar Resumen Ejecutivo
```
POST /api/comparisons/{id}/generate_summary/
```
**Body:**
- `summary_type`: string (executive, detailed, financial)
- `language`: string (es, en)

### Análisis Detallado
```
GET /api/comparisons/{id}/analysis/
```

### Exportar Comparación
```
POST /api/comparisons/{id}/export/
```
**Body:**
- `format`: string (pdf, excel, json)
- `include_charts`: boolean (opcional)
- `include_summary`: boolean (opcional)

### Estadísticas de Comparaciones
```
GET /api/comparisons/stats/
```

## Códigos de Estado

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: No autorizado
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Ejemplos de Respuesta

### Oferta
```json
{
  "id": "uuid",
  "oferente": "Empresa ABC",
  "ruc": "12345678",
  "monto": "100000.00",
  "plazo": 30,
  "garantia": "5000.00",
  "validation_state": "ACCEPTED",
  "rejection_reason": null,
  "score_rank": 0.85,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Comparación
```json
{
  "id": "uuid",
  "created_by": "usuario",
  "offers": [...],
  "executive_summary": "Resumen ejecutivo...",
  "metadata": {
    "ranking_base": "composite",
    "thresholds": {},
    "offer_count": 3
  },
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Filtros Disponibles

### Ofertas
- `validation_state`: Aceptado/Rechazado
- `rejection_reason`: Razón específica de rechazo
- `min_monto`/`max_monto`: Rango de precios
- `oferente`: Nombre de la empresa
- `ruc`: Número RUC
- `pliego_id`: ID del pliego

### Documentos
- `status`: Estado del procesamiento
- `pliego`: Pliego asociado
- `uploader`: Usuario que subió

### Comparaciones
- `created_by`: Usuario que creó
- `created_at`: Fecha de creación

## Ordenamiento

### Ofertas
- `score_rank`: Por ranking
- `monto`: Por precio
- `created_at`: Por fecha
- `oferente`: Por nombre

### Documentos
- `uploaded_at`: Por fecha de subida
- `processed_at`: Por fecha de procesamiento
- `original_filename`: Por nombre de archivo

### Comparaciones
- `created_at`: Por fecha de creación
