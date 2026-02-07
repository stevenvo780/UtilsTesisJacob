#!/usr/bin/env bash
# replay_cases.sh — Re-ejecuta los casos disputados con semillas fijas
# Uso: bash repos/scripts/replay_cases.sh
# Genera outputs/metrics.json y outputs/report.md en cada caso
set -euo pipefail

CASES=("caso_clima" "caso_contaminacion" "caso_movilidad")
BASE="repos/Simulaciones"

echo "=== Replay de casos con código actual ==="
echo "Fecha: $(date -Iseconds)"
echo "Commit: $(git rev-parse --short HEAD)"
echo ""

for caso in "${CASES[@]}"; do
    echo "--- Ejecutando $caso ---"
    cd "$BASE/$caso/src"
    python3 validate.py 2>&1 | tail -5
    cd - > /dev/null
    echo ""
done

echo "=== Replay completado ==="
echo "Verificar resultados en $BASE/caso_*/outputs/metrics.json"
