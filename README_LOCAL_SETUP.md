# Configuración Local - Sistema de Licitaciones

## 🚀 Configuración Rápida

### Prerrequisitos
- Docker y Docker Compose instalados
- Git

### Pasos de Configuración

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd licitacion-backend
```

2. **Ejecutar script de configuración automática**
```bash
./setup_local.sh
```

3. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus credenciales
```

4. **Levantar servicios**
```bash
docker-compose up -d
```

## 🐳 Servicios Docker

### Servicios Incluidos
- **web**: Django API (puerto 8000)
- **db**: PostgreSQL 15 (puerto 5432)
- **redis**: Redis 7 (puerto 6379)
- **celery**: Worker de Celery
- **celery-beat**: Scheduler de Celery

### Configuración de Base de Datos
- **Base de datos**: `licitacion_db`
- **Usuario**: `licitacion_user`
- **Contraseña**: `licitacion_pass`
- **Host**: `db` (dentro de Docker) / `localhost` (desde host)
- **Puerto**: `5432`

## 🔧 Comandos Útiles

### Gestión de Servicios
```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Parar servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver estado de servicios
docker-compose ps
```

### Django Management
```bash
# Shell de Django
docker-compose exec web python manage.py shell

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### Base de Datos
```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U licitacion_user -d licitacion_db

# Backup de base de datos
docker-compose exec db pg_dump -U licitacion_user licitacion_db > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U licitacion_user -d licitacion_db < backup.sql
```

### Celery
```bash
# Ver workers de Celery
docker-compose exec web celery -A tasks.celery_app inspect active

# Limpiar cola de Celery
docker-compose exec web celery -A tasks.celery_app purge

# Ver tareas en cola
docker-compose exec web celery -A tasks.celery_app inspect reserved
```

## 🌐 URLs de Acceso

### Desarrollo Local
- **API Django**: http://localhost:8000
- **Documentación API**: http://localhost:8000/api/docs/
- **Admin Django**: http://localhost:8000/admin/
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Credenciales por Defecto
- **Superusuario**: Se crea automáticamente con el script
- **Base de datos**: licitacion_user / licitacion_pass

## 📁 Estructura de Archivos

```
licitacion-backend/
├── docker-compose.yml      # Configuración de servicios
├── init.sql               # Script de inicialización de PostgreSQL
├── setup_local.sh         # Script de configuración automática
├── env.example            # Variables de entorno de ejemplo
├── backend/
│   ├── settings.py        # Configuración principal
│   └── settings_local.py  # Configuración local
└── apps/
    ├── pliegos/           # App de pliegos
    ├── documents/         # App de documentos
    ├── offers/            # App de ofertas
    └── comparisons/       # App de comparaciones
```

## 🔒 Variables de Entorno

### Requeridas
```bash
# Base de datos
POSTGRES_DB=licitacion_db
POSTGRES_USER=licitacion_user
POSTGRES_PASSWORD=licitacion_pass

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### Opcionales (para funcionalidad completa)
```bash
# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET=your_bucket

# OpenAI
OPENAI_API_KEY=your_key
```

## 🐛 Solución de Problemas

### PostgreSQL no se conecta
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps db

# Ver logs de PostgreSQL
docker-compose logs db

# Reiniciar PostgreSQL
docker-compose restart db
```

### Migraciones fallan
```bash
# Eliminar base de datos y recrear
docker-compose down -v
docker-compose up -d db
docker-compose exec web python manage.py migrate
```

### Celery no procesa tareas
```bash
# Verificar workers
docker-compose logs celery

# Reiniciar Celery
docker-compose restart celery celery-beat
```

### Problemas de permisos
```bash
# Dar permisos al script
chmod +x setup_local.sh

# Limpiar volúmenes Docker
docker-compose down -v
docker system prune -f
```

## 📊 Monitoreo

### Logs
```bash
# Ver todos los logs
docker-compose logs -f

# Ver logs específicos
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f celery
```

### Métricas de Base de Datos
```bash
# Conectar a PostgreSQL y ver estadísticas
docker-compose exec db psql -U licitacion_user -d licitacion_db -c "
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE schemaname = 'public' 
ORDER BY tablename, attname;
"
```

## 🚀 Desarrollo

### Configuración de IDE
- **Python Interpreter**: Usar el del contenedor Docker
- **Database**: Conectar a localhost:5432
- **Debug**: Configurar para ejecutar en contenedor

### Hot Reload
Los cambios en el código se reflejan automáticamente gracias al volumen montado.

### Testing
```bash
# Ejecutar tests
docker-compose exec web python manage.py test

# Ejecutar tests específicos
docker-compose exec web python manage.py test apps.offers
```

## 📝 Notas Importantes

1. **Persistencia**: Los datos de PostgreSQL y Redis se mantienen en volúmenes Docker
2. **Seguridad**: Esta configuración es solo para desarrollo
3. **Performance**: PostgreSQL está optimizado para desarrollo local
4. **Backup**: Hacer backups regulares de la base de datos
5. **Updates**: Actualizar dependencias regularmente

## 🔄 Actualizaciones

```bash
# Actualizar código
git pull

# Reconstruir imágenes
docker-compose build

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Reiniciar servicios
docker-compose restart
```
