"""
Aplicación auditoria - Sistema de registro y monitoreo de actividades.

Esta aplicación maneja el registro de todas las actividades importantes del sistema,
incluyendo logins, cambios administrativos, creación/eliminación de recursos, y
proporciona un dashboard para administradores con métricas y filtros avanzados.

Módulos:
    - models: Definición del modelo RegistroActividad para almacenar eventos.
    - views: Vistas del dashboard de auditoría con métricas y gráficos.
    - utils: Funciones auxiliares para registrar actividades específicas.
    - admin: Configuración del panel de administración (solo lectura).
    - urls: Rutas del dashboard de auditoría.
    - tests: Tests unitarios para modelos y vistas.
"""
