# """
# Configuración local para desarrollo
# """
# from .settings import *

# # Configuración de debug para desarrollo
# DEBUG = True

# # Configuración de base de datos local (SQLite para desarrollo rápido)
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# # Configuración de CORS para desarrollo
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]

# CORS_ALLOW_ALL_ORIGINS = True  # Solo para desarrollo

# # Configuración de logging para desarrollo
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#         'file': {
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',
#             'formatter': 'verbose',
#         },
#     },
#     'root': {
#         'handlers': ['console', 'file'],
#         'level': 'INFO',
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#         'apps': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }

# # Configuración de archivos estáticos para desarrollo
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# # Configuración de archivos media para desarrollo
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # Configuración de email para desarrollo (console backend)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# # Configuración de cache para desarrollo (usar cache en memoria)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake',
#     }
# }

# # Configuración de sesiones para desarrollo
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# # Configuración de DRF para desarrollo
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'rest_framework.renderers.JSONRenderer',
#     'rest_framework.renderers.BrowsableAPIRenderer',
# )

# # Configuración de JWT para desarrollo
# SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=24)  # Más tiempo para desarrollo
# SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=7)

# # Configuración de Celery para desarrollo (síncrono para pruebas)
# CELERY_TASK_ALWAYS_EAGER = True  # Ejecutar tareas síncronamente
# CELERY_TASK_EAGER_PROPAGATES = True

# # Configuración de S3 para desarrollo (opcional)
# if not os.getenv('AWS_ACCESS_KEY_ID'):
#     # Usar almacenamiento local si no hay credenciales de S3
#     DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
#     AWS_S3_ENDPOINT_URL = None

# # Configuración de seguridad para desarrollo
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False

# # Configuración de debug toolbar (opcional)
# # if DEBUG:
# #     INSTALLED_APPS += ['debug_toolbar']
# #     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# #     INTERNAL_IPS = ['127.0.0.1', 'localhost']

# # Configuración de testing
# TEST_RUNNER = 'django.test.runner.DiscoverRunner'

