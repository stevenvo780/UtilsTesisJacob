# Protocolo de Simulación — {{case_title}}

## Fases de ejecución

### Fase 1: Datos sintéticos (verificación interna)
1. Generar serie temporal con ODE de parámetros conocidos + ruido
2. Calibrar ABM y ODE sobre datos sintéticos (split temporal)
3. Evaluar C1–C5 contra verdad conocida
4. **Criterio de paso:** todos los criterios deben cumplirse con datos controlados

### Fase 2: Datos reales (validación empírica)
1. Obtener datos observacionales de {{data_source}}
2. Calibrar parámetros sobre partición de entrenamiento
3. Evaluar C1–C5 sobre partición de validación
4. **Criterio de paso:** EDI > 0.30 para confirmar hiperobjeto

## Calibración
- **ODE:** Regresión lineal sobre primeras diferencias → α, β
- **ABM:** Búsqueda en grilla sobre difusión, acoplamiento, amortiguamiento
- **Split temporal:** Entrenamiento (primera mitad) / Validación (segunda mitad)

## Perturbaciones de robustez (C2)
- 10 ejecuciones con parámetros perturbados ±10%
- Verificar estabilidad del EDI y correlaciones

## Criterios de parada
- Convergencia de calibración (mejora < 1% en RMSE)
- Máximo 1000 iteraciones de búsqueda
