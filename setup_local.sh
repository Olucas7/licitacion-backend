#!/bin/bash

# Script de configuración local para el proyecto de licitaciones
echo "🚀 Configurando entorno local para el proyecto de licitaciones..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde env.example..."
    cp env.example .env
    echo "✅ Archivo .env creado. Por favor edita las variables según tu configuración."
else
    echo "✅ Archivo .env ya existe."
fi

# Construir y levantar los servicios
echo "🐳 Construyendo y levantando servicios Docker..."
docker-compose down -v
docker-compose build
docker-compose up -d db redis

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté listo..."
until docker-compose exec -T db pg_isready -U licitacion_user -d licitacion_db; do
    echo "Esperando PostgreSQL..."
    sleep 2
done

echo "✅ PostgreSQL está listo!"

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones de Django..."
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate

# Crear superusuario
echo "👤 Creando superusuario..."
docker-compose run --rm web python manage.py createsuperuser --noinput || echo "Superusuario ya existe o error en la creación."

# Levantar todos los servicios
echo "🚀 Levantando todos los servicios..."
docker-compose up -d

# Mostrar estado de los servicios
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Servicios disponibles:"
echo "   - Django API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/api/docs/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo ""
echo "🔧 Comandos útiles:"
echo "   - Ver logs: docker-compose logs -f"
echo "   - Parar servicios: docker-compose down"
echo "   - Reiniciar: docker-compose restart"
echo "   - Shell Django: docker-compose exec web python manage.py shell"
echo ""
echo "⚠️  Recuerda editar el archivo .env con tus credenciales reales."
