# Estructura de la Presentación — Modelos Jerárquicos Bayesianos

**Duración estimada:** 1:20 – 1:30 h  
**Audiencia:** Compañeros de clase con base estadística similar  
**Hilo conductor:** Una sola pregunta recorre toda la presentación — *¿Cómo aprendo de un grupo sin ignorar lo que los demás me dicen sobre él?*

---

## Principio de diseño narrativo

La presentación no es una lista de temas. Es un argumento que avanza:

```
Hay un problema real con datos agrupados
    → los enfoques clásicos lo resuelven mal
    → existe un tercer camino: partial pooling
    → así se construye formalmente
    → así funciona el shrinkage (la magia del modelo)
    → así sabemos si el modelo es confiable
    → así se extiende cuando hay predictores
    → así comparamos y elegimos modelos
    → esto es lo que se lleva cada uno
```

Cada slide **termina abriendo** la siguiente. El oyente nunca debe preguntarse "¿por qué me están contando esto ahora?"

---

## SLIDE 1 — Portada

**Qué mostrar:** Título, subtítulo, nombres.  
**Tiempo:** 1 min

### Qué decir en voz alta
> "Vamos a hablar de modelos jerárquicos bayesianos. No vamos a empezar con la definición formal — vamos a empezar con la intuición detrás de la idea."

**Conexión a la siguiente:** El título queda en el aire. La siguiente slide lo aterriza con un ejemplo concreto.

---

## SLIDE 2 — Modelo de Modelos (La Arquitectura Base)

**Idea central:** Anclar el concepto de "jerarquía" en una situación de la vida real. Mostrar las 3 capas sin matemáticas.

### Qué mostrar
- Comparación visual: Mirar solo al estudiante vs. Mirar a toda la universidad.
- Las 3 Capas: Nivel 3 (Universidad) → Nivel 2 (Salón) → Nivel 1 (Estudiante).

### Qué decir en voz alta
> "Supongamos que queremos evaluar el rendimiento de un estudiante. Si usamos solo sus notas (información local), la evaluación es inestable si el estudiante es nuevo. Si usamos el promedio de la universidad (información global), ignoramos quién es él realmente."
>
> "La solución: El estudiante está en un salón. Lo que sé del salón ayuda al estudiante, y lo que sé de los salones me habla de la universidad. Esta arquitectura de 3 niveles es el corazón del modelo jerárquico."

### Conexión a la siguiente
> "Pero para que este modelo funcione, tenemos que cambiar nuestra forma de pensar sobre qué es un parámetro. Necesitamos ser bayesianos."

---

## SLIDE 3 — Clásico vs Bayesiano (Dos filosofías)

**Idea central:** Explicar por qué tratar los parámetros como distribuciones es la clave de todo.

### Qué mostrar
- Tarjeta Clásica: El parámetro es un número fijo.
- Tarjeta Bayesiana: El parámetro es una variable aleatoria (con distribución).

### Qué decir en voz alta
> "La jerarquía solo funciona si aceptamos que todo tiene incertidumbre. La visión clásica dice que el parámetro que buscamos es un número fijo 'ahí afuera'. Pero la visión bayesiana trata al parámetro como una variable aleatoria con su propia distribución."
>
> "Al tratar los parámetros de cada grupo como distribuciones, podemos modelar de dónde vienen esas distribuciones. Este es el lenguaje natural para la jerarquía."

### Conexión a la siguiente
> "Con esta filosofía en mente, veamos cómo se escribe esto en matemáticas."

---

## SLIDE 4 — El modelo normal jerárquico (Especificación Formal)

**Idea central:** El modelo se construye de abajo hacia arriba formalmente.

### Qué mostrar
- Los tres niveles con sus fórmulas, presentados de manera progresiva.
- Tabla de parámetros con interpretación en prosa.
- Gráfico interactivo: Descomposición de varianza.

### Qué decir en voz alta
> "Nivel 1: Los datos que observamos siguen una Normal con una media propia de su grupo, y un ruido σ_y."
> "Nivel 2: Esas medias de grupo vienen de una Normal poblacional con media μ y variación σ_μ."
> "Nivel 3: Los hiperpriors. μ y las desviaciones también tienen distribuciones a priori."
>
> "La varianza total se parte en dos: la variación entre grupos y la variación dentro de los grupos."

### Conexión a la siguiente
> "Bien, esa es la teoría. Pero en el mundo real, ¿qué clase de problemas requieren esta herramienta?"

---

## SLIDE 5 — ¿Para qué se usa? (Motivación General)

**Idea central:** Mostrar que este no es un modelo de nicho, sino una herramienta fundamental para problemas comunes en la ciencia de datos.

### Qué mostrar
- 4 tarjetas con iconos: Datos Anidados, Muestras Desbalanceadas, Múltiples Experimentos, Predicción a Nuevos Grupos.

### Qué decir en voz alta
> "Los datos del mundo real rara vez son independientes. Usamos este modelo cuando tenemos pacientes en hospitales o estudiantes en colegios (datos anidados). Es vital cuando tenemos muestras desbalanceadas: el modelo estabiliza a los grupos pequeños. También se usa para meta-análisis y para poder predecir qué pasará con un grupo nuevo usando la distribución poblacional."

### Conexión a la siguiente
> "Sabiendo para qué sirve, veamos un problema estadístico real con datos de Spotify."

---

## SLIDE 6 — El problema: datos con estructura de grupos

**Idea central:** Aterrizar el concepto en un dataset real.

### Qué mostrar
- Un scatter plot interactivo: puntos coloreados por grupo (artistas con sus canciones).
- Pregunta visible: ¿Son estas observaciones independientes?

### Qué decir en voz alta
> "Supongamos que tenemos 350 canciones de 44 artistas en Spotify. ¿Puedo tratarlas como 350 observaciones independientes? La respuesta es no. Las canciones de un mismo artista se parecen más entre sí. Ignorar esta estructura tiene consecuencias."

### Conexión a la siguiente
> "Entonces, ¿cómo han intentado resolver esto? Hay dos respuestas clásicas. Y las dos están mal."

---

## SLIDE 7 — Las dos respuestas clásicas (y por qué fallan)

**Idea central:** Complete pooling y no pooling son los dos extremos de un continuo.

### Qué mostrar
- Tabla: Complete Pooling / No Pooling / Partial Pooling.
- Gráfico interactivo con estimaciones de los 12 artistas bajo cada enfoque.

### Qué decir en voz alta
> "El Complete Pooling ignora los grupos: un solo promedio para todo. Produce sesgo. El No Pooling trata cada artista como un universo aparte. Produce varianza altísima en grupos pequeños y no puede predecir grupos nuevos."
>
> "Lo que necesitamos es algo en el medio. El modelo jerárquico que acabamos de construir."

### Conexión a la siguiente
> "Una vez calculado el modelo jerárquico, las estimaciones sufren un fenómeno fascinante: el shrinkage."

---

## SLIDE 8 — Shrinkage: la propiedad clave del modelo jerárquico

**Idea central:** El shrinkage no es un defecto — es el comportamiento óptimo dado lo que el modelo sabe de cada grupo.

### Qué mostrar
- Fórmula del estimador posterior (promedio ponderado) y de λ_j.
- Gráfico de línea interactivo (λ_j vs n_j).
- Gráfico de barras interactivo de Shrinkage.

### Qué decir en voz alta
> "La estimación jerárquica es un promedio ponderado entre la media del grupo y la media global. Si un artista tiene 30 canciones, el modelo confía en sus datos (peso alto). Si tiene 2 canciones, el modelo dice 'no tengo suficiente información, me acerco a la media global'."
>
> "El gráfico demuestra esto: los artistas con pocas canciones son fuertemente 'encogidos' (shrinkage) hacia el promedio global."

### Conexión a la siguiente
> "Ya entendemos cómo aprende el modelo. Ahora, ¿qué pasa cuando queremos agregar un predictor explicativo — como la edad en una carrera?"

---

## SLIDE 9 — Extensión con predictores: regresión jerárquica

**Idea central:** Ahora la relación entre predictor y respuesta también varía por grupo.

### Qué mostrar
- Panel interactivo con líneas de regresión superpuestas (Pooled, Rand Intercepts, Rand Slopes).
- Dataset: Cherry Blossom Run (edad vs tiempo).

### Qué decir en voz alta
> "Cambiamos de dataset: edad vs tiempo de carrera. El modelo pooled asume la misma recta para todos. El modelo de 'random intercepts' le da a cada corredor su propia velocidad base, pero asume que todos envejecen igual. El modelo de 'random slopes' va más allá: cada corredor tiene su propio punto de partida Y su propio ritmo de envejecimiento."

### Conexión a la siguiente
> "Tenemos el modelo completo. Ahora viene la pregunta práctica: ¿cómo predigo?"

---

## SLIDE 10 — Predicción: corredor conocido vs. corredor nuevo

**Idea central:** El modelo jerárquico hace predicciones diferentes según si el grupo ya fue observado. Es honestidad estadística.

### Qué mostrar
- Gráfico interactivo con dos distribuciones predictivas superpuestas (conocido vs nuevo).

### Qué decir en voz alta
> "Si el corredor ya participó antes, la predicción es precisa. Sabemos quién es. Pero si el corredor es nuevo, no tenemos sus parámetros. El modelo tiene que muestrear de la distribución poblacional. La incertidumbre es mucho mayor."
> "Esta banda ancha no es un defecto — es honestidad. El modelo sabe lo que no sabe."

### Conexión a la siguiente
> "Tenemos varios modelos posibles. ¿Cuál elegimos? Necesitamos comparar capacidad predictiva."

---

## SLIDE 11 — Comparación de modelos: LOO-CV

**Idea central:** LOO-CV evalúa qué tan bien predice el modelo. Demuestra objetivamente que el jerárquico gana.

### Qué mostrar
- Gráfico interactivo horizontal con el ELPD_LOO de los tres modelos de regresión.

### Qué decir en voz alta
> "Leave-One-Out Cross Validation evalúa la capacidad de generalizar a datos no vistos. El resultado es el ELPD. Más alto es mejor. El modelo pooled pierde estrepitosamente. Entre interceptos aleatorios y pendientes aleatorias, el modelo nos dice qué estructura es la más adecuada para la realidad."

### Conexión a la siguiente
> "Hemos recorrido el camino completo y probado que el modelo jerárquico gana. Cerremos con las tres ideas que se quedan."

---

## SLIDE 12 — Resumen: tres ideas y un criterio

**Idea central:** Todo se organiza alrededor de tres propiedades.

### Qué mostrar
- Gráfico de Radar interactivo comparando Simplicidad, Flexibilidad, Grupos pequeños, etc.
- Las tres propiedades clave.

### Qué decir en voz alta
> "Cuando los datos tienen estructura de grupos, ignorarla es un error. Llévense estas tres cosas:
> 1. Intercambiabilidad parcial: respeta la estructura.
> 2. Shrinkage adaptativo: contracción proporcional a la ignorancia local.
> 3. Predicción calibrada: mayor incertidumbre ante lo desconocido."
>
> "Los modelos jerárquicos no son más complicados — simplemente son más honestos."


## Guía de tiempos estimados

| Slide | Tema | Tiempo |
|-------|------|--------|
| 1 | Portada | 1 min |
| 2 | Modelo de Modelos | 4 min |
| 3 | Clásico vs Bayesiano | 5 min |
| 4 | Especificación Formal | 10 min |
| 5 | ¿Para qué se usa? (Motivación) | 4 min |
| 6 | Problema de datos agrupados (Spotify) | 7 min |
| 7 | Tres estrategias + fallos | 10 min |
| 8 | Shrinkage | 10 min |
| 9 | Regresión jerárquica (predictores) | 12 min |
| 10 | Predicción | 8 min |
| 11 | LOO-CV | 8 min |
| 12 | Resumen | 4 min |
| **Total** | | **~1:23 h** |

## Frases de conexión entre slides (leer como guía)

| Transición | Frase de cierre de la slide anterior |
|------------|--------------------------------------|
| 1 → 2 | *"No vamos a empezar con la definición formal — vamos a empezar con la intuición detrás de la idea."* |
| 2 → 3 | *"Pero para que este modelo funcione, tenemos que cambiar nuestra forma de pensar sobre qué es un parámetro. Necesitamos ser bayesianos."* |
| 3 → 4 | *"Con esta filosofía en mente, veamos cómo se escribe esto en matemáticas."* |
| 4 → 5 | *"Bien, esa es la teoría. Pero en el mundo real, ¿qué clase de problemas requieren esta herramienta?"* |
| 5 → 6 | *"Sabiendo para qué sirve, veamos un problema estadístico real con datos de Spotify."* |
| 6 → 7 | *"Entonces, ¿cómo han intentado resolver esto? Hay dos respuestas clásicas. Y las dos están mal."* |
| 7 → 8 | *"Una vez calculado el modelo jerárquico, las estimaciones sufren un fenómeno fascinante: el shrinkage."* |
| 8 → 9 | *"Ya entendemos cómo aprende el modelo. Ahora, ¿qué pasa cuando queremos agregar un predictor explicativo — como la edad en una carrera?"* |
| 9 → 10 | *"Tenemos el modelo completo. Ahora viene la pregunta práctica: ¿cómo predigo?"* |
| 10 → 11 | *"Tenemos varios modelos posibles. ¿Cuál elegimos? Necesitamos comparar capacidad predictiva."* |
| 11 → 12 | *"Hemos recorrido el camino completo y probado que el modelo jerárquico gana. Cerremos con las tres ideas que se quedan."* |

---
## Preguntas frecuentes que pueden surgir del público

**"¿Por qué no usar simplemente efectos fijos por grupo?"**
> Los efectos fijos estiman un parámetro por grupo sin compartir información. Con grupos pequeños, la estimación es inestable. Además, los efectos fijos consumen grados de libertad y no permiten predecir grupos nuevos.

**"¿El shrinkage no introduce sesgo?"**
> Sí, introduce algo de sesgo — pero reduce varianza de manera que el error cuadrático medio total mejora. El estimador jerárquico domina en riesgo cuadrático al no-pooling cuando los grupos no son demasiado distintos entre sí.

**"¿Cuántos grupos necesito para que el modelo jerárquico tenga sentido?"**
> El libro no da un número mínimo exacto, pero la recomendación práctica es al menos 5–10 grupos. Con menos grupos, los hiperparámetros μ y σ_μ no se estiman bien y el shrinkage puede ser excesivo.

**"¿Qué pasa si el ICC es cercano a 0?"**
> Si ρ ≈ 0, los grupos son prácticamente indistinguibles y el complete pooling habría sido razonable. El modelo jerárquico no daña — simplemente no aporta ventaja adicional. El σ_μ posterior será cercano a 0 y habrá mucho shrinkage.

**"¿Por qué PSIS-LOO y no AIC/BIC?"**
> AIC y BIC penalizan por número de parámetros, lo cual es problemático en modelos jerárquicos donde los parámetros de grupo son parcialmente pooled (no son "libres" en el sentido usual). LOO-CV evalúa directamente la capacidad predictiva sin asumir nada sobre el número efectivo de parámetros.
