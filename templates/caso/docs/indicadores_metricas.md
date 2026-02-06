# Indicadores y Métricas — {{case_title}}

## Métricas Primarias

| Métrica | Descripción | Umbral |
|---------|-------------|--------|
| **EDI** | Índice de Dependencia Efectiva: `(rmse_reduced - rmse_abm) / rmse_reduced` | > 0.30 para validar |
| **CR**  | Ratio de Cohesión: `correlación_interna / correlación_externa` | > 2.0 (Symploké) |
| **EI**  | Información Efectiva (Hoel): determinismo - degeneración | > 0 para emergencia |

## Métricas de Error

| Métrica | Descripción |
|---------|-------------|
| RMSE ABM | Error del modelo micro contra observaciones |
| RMSE ODE | Error del modelo macro contra observaciones |
| RMSE reducido | Error del ABM sin acoplamiento macro (línea base) |

## Criterios C1–C5

| Criterio | Test | Umbral |
|----------|------|--------|
| C1 | Convergencia: RMSE < umbral, correlación > 0.7 | Dominio-específico |
| C2 | Robustez: estabilidad bajo perturbación ±10% | Varianza < 1.0 |
| C3 | Replicación: varianza de ventana consistente | Determinista con semilla |
| C4 | Validez: coherencia con leyes del dominio | Más forzamiento → más respuesta |
| C5 | Incertidumbre: sensibilidad acotada | < 1.0 unidades |

## Fuente de verdad
Los valores numéricos se computan en `metrics.json` y se sincronizan automáticamente
a este documento mediante `python3 scripts/tesis.py sync`.

<!-- AUTO:RESULTS:START -->
| Métrica | Sintético | Real |
|---------|-----------|------|
| EDI     | —         | —    |
| CR      | —         | —    |
| Estado  | Pendiente | Pendiente |
<!-- AUTO:RESULTS:END -->
