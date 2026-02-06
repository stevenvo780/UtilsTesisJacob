# Caso {{case_title}}

## Resumen

{{description}}

## Hipótesis

{{hypothesis}}

## Dominio

**Área:** {{domain}}
**Observable:** {{observable}}
**Fuente de datos:** {{data_source}}

## Modelo Híbrido

- **Macro (ODE):** {{macro_description}}
- **Micro (ABM):** {{micro_description}}

## Resultados

<!-- AUTO:RESULTS:START -->
| Métrica | Sintético | Real |
|---------|-----------|------|
| EDI     | —         | —    |
| CR      | —         | —    |
| RMSE ABM| —         | —    |
| C1      | —         | —    |
| C2      | —         | —    |
| C3      | —         | —    |
| C4      | —         | —    |
| C5      | —         | —    |
| Estado  | Pendiente | Pendiente |
<!-- AUTO:RESULTS:END -->

## Archivos clave

- `report.md` — Reporte de validación generado
- `metrics.json` — Métricas computadas (fuente de verdad numérica)
- `docs/` — Documentación técnica del caso

## Reproducibilidad

Pipeline C1–C5 documentado en `docs/validacion_c1_c5.md`.
Semillas fijas para reproducibilidad determinista.
