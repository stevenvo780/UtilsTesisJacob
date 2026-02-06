# Reproducibilidad — {{case_title}}

## Semillas y determinismo
- Semilla base: definida en parámetros de simulación
- Todas las fuentes de aleatoriedad usan `numpy.random.default_rng(seed)`
- Resultado idéntico bit-a-bit con misma semilla y misma versión de NumPy

## Versionado
- Código fuente: referenciado por commit de Git
- Datos: cacheados localmente tras primera descarga
- Dependencias: `repos/Simulaciones/requirements.txt`

## Artefactos generados
- `metrics.json` — Métricas computadas (fuente de verdad numérica)
- `report.md` — Reporte narrativo de resultados

## Cómo reproducir
```bash
# Instalar dependencias
python3 -m pip install -r repos/Simulaciones/requirements.txt

# Ejecutar validación (si existe código ejecutable)
python3 scripts/tesis.py validate --case caso_{{case_name}}

# O directamente
python3 repos/Simulaciones/caso_{{case_name}}/src/validate.py
```

## Sincronización de métricas
```bash
# Actualizar docs desde metrics.json
python3 scripts/tesis.py sync
```
