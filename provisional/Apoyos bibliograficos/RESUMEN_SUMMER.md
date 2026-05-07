# Resumen operativo de `SUMMER .pdf`

Notas para usar como contexto de diseno y narrativa en `presentacion.html`.

## Hilo visual del PDF

El PDF explica modelos jerarquicos con una progresion visual:

1. **Complete pooling:** todas las observaciones dependen de un unico parametro poblacional.
2. **No pooling:** cada grupo tiene sus propios parametros y no comparte informacion.
3. **Partial pooling:** los parametros de grupo vienen de una distribucion poblacional comun.

La forma grafica recurrente es:

```text
Population
   ↓
label 1     label 2     ...     label m
   ↓           ↓                  ↓
y_11,y_21   y_12,y_22           y_1m,y_2m
```

## Ejemplo de turismo

Contexto:

- Ciudades: Cartagena, Medellin, Bogota.
- 5 turistas por ciudad.
- Respuesta: gasto turistico total.
- Predictor: dias de estadia.
- Grupo: ciudad.

Objetivo:

Mostrar como el modelo jerarquico mejora la estimacion al compartir informacion entre ciudades relacionadas, sobre todo cuando hay pocos datos por grupo.

## Mensajes clave

- Complete pooling es estable, pero oculta diferencias entre ciudades.
- No pooling captura diferencias locales, pero puede sobreajustar con pocos datos.
- Partial pooling balancea flexibilidad y estabilidad.
- El modelo jerarquico permite que cada ciudad tenga su propia recta, pero sus parametros se informan por una distribucion comun.
- Para ciudades nuevas como Cali, no pooling no tiene parametros; partial pooling puede predecir usando la distribucion poblacional.

## Formulas utiles

Complete pooling:

```text
y_i = mu + beta * days_i + epsilon_i
```

No pooling:

```text
y_ij = mu_j + beta_j * days_ij + epsilon_ij
```

Partial pooling:

```text
y_ij = mu_j + beta_j * days_ij + epsilon_ij
mu_j   ~ N(mu_0, sigma_mu^2)
beta_j ~ N(beta_0, sigma_beta^2)
```

## Implicacion para las slides

La presentacion debe mostrar primero la arquitectura:

```text
Colombia
  ├── Cartagena -> turistas
  ├── Medellin  -> turistas
  └── Bogota    -> turistas
```

Luego comparar estrategias:

```text
mezclar todo  vs  separar todo  vs  conectar grupos
```

