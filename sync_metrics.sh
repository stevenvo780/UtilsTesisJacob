#!/usr/bin/env bash
# sync_metrics.sh — Sincroniza metrics.json de Simulaciones → TesisDesarrollo
# Uso: bash repos/scripts/sync_metrics.sh
set -euo pipefail

declare -A MAP=(
    ["caso_clima"]="01_caso_clima"
    ["caso_contaminacion"]="03_caso_contaminacion"
    ["caso_movilidad"]="13_caso_movilidad"
)

SIM_BASE="repos/Simulaciones"
TESIS_BASE="TesisDesarrollo/02_Modelado_Simulacion"

echo "=== Sincronización metrics.json ==="
echo "Fecha: $(date -Iseconds)"
echo "Commit: $(git rev-parse --short HEAD)"
echo ""

for sim_name in "${!MAP[@]}"; do
    tesis_name="${MAP[$sim_name]}"
    src="$SIM_BASE/$sim_name/outputs/metrics.json"
    dst="$TESIS_BASE/$tesis_name/metrics.json"
    if [ -f "$src" ]; then
        cp "$src" "$dst"
        echo "✅ $sim_name → $tesis_name"
    else
        echo "⚠️  $src no existe"
    fi
done

echo ""
echo "=== Verificando consistencia ==="
python3 repos/scripts/verificar_consistencia.py
