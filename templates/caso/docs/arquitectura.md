# Arquitectura — {{case_title}}

## Capas del modelo

### Capa Macro (ODE)
{{macro_description}}

Ecuación general: `dX/dt = α(F(t) - βX) + ruido + asimilación`

### Capa Micro (ABM)
{{micro_description}}

Dinámica por celda:
```
nuevo = actual
      + difusión × (media_vecinos - actual)
      + acoplamiento_macro × (promedio_global - actual)
      + escala_forzamiento × forzamiento(t)
      - amortiguamiento × actual
      + ruido
      ± asimilación × (obs - actual)
```

## Observable
{{observable}}

## Fuente de datos
{{data_source}}

## Acoplamiento
El parámetro de orden macro restringe las dinámicas locales vía `macro_coupling`.
La asimilación de datos (nudging) conecta observaciones reales al modelo,
justificada teóricamente como la formalización del acoplamiento hiperobjeto–materia.

## Supuestos
- Separación de escalas temporal entre macro y micro
- Estacionariedad local durante ventanas de calibración
- Forzamiento exógeno conocido o estimable
