#!/bin/bash

# Script para cargar datos de ejemplo en GRCU Manager
# Uso: ./manage_seed.sh [TRADICIONAL|AGIL]

set -e  # Salir si hay errores

METODOLOGIA=${1:-TRADICIONAL}

echo "======================================================================"
echo "🌱 SEED DATA - GRCU Manager"
echo "======================================================================"
echo ""
echo "Metodología seleccionada: $METODOLOGIA"
echo ""

# Verificar que la metodología sea válida
if [ "$METODOLOGIA" != "TRADICIONAL" ] && [ "$METODOLOGIA" != "AGIL" ]; then
    echo "❌ Error: Metodología debe ser TRADICIONAL o AGIL"
    echo "Uso: ./manage_seed.sh [TRADICIONAL|AGIL]"
    exit 1
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

echo "Cargando 20 requerimientos con metodología $METODOLOGIA..."
echo ""

python manage.py seed_requerimientos --metodologia "$METODOLOGIA"

echo ""
echo "======================================================================"
echo "✅ Datos cargados exitosamente"
echo "======================================================================"
echo ""
echo "📌 Para ver los datos:"
echo "   python manage.py runserver"
echo "   Luego accede al dashboard del líder"
echo ""
