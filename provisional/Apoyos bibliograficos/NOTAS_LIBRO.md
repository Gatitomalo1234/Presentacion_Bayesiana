# Notas del libro: *Bayes Rules!* — Capítulos 15, 16 y 17

**Libro:** *Bayes Rules! An Introduction to Applied Bayesian Modeling*  
**Autores:** Alicia A. Johnson, Miles Q. Ott, Mine Dogucu  
**URL:** https://www.bayesrulesbook.com  
**Capítulos cubiertos:** 15 (motivación), 16 (sin predictores), 17 (con predictores)

---

## Capítulo 15 — Hierarchical Models Are Exciting

### Idea central

Este capítulo no construye modelos — **motiva por qué existen**. El argumento es simple: cuando los datos tienen estructura de grupos (observaciones dentro de grupos, grupos dentro de poblaciones), los enfoques clásicos fallan de maneras predecibles y evitables.

La pregunta que guía el capítulo: **¿cómo aprendo de un grupo sin ignorar a los demás?**

### Dataset: Cherry Blossom Run

- Carrera de 10 millas en Washington D.C.
- **252 observaciones** de **36 participantes** (edades 50–60 años)
- Cada corredor participó en múltiples años
- Variable respuesta: tiempo neto de carrera
- Estructura jerárquica natural: observaciones anidadas dentro de corredores

Este dataset aparece de nuevo en los capítulos 16 y 17 con distinto enfoque.

### Los tres enfoques comparados

#### 1. Complete Pooling

- **Supuesto:** todas las observaciones son intercambiables — un solo parámetro describe a todos los corredores
- **Implementación:** modelo de regresión estándar ignorando la variable de grupo
- **Problema:** viola el supuesto de independencia. Dos mediciones del mismo corredor son más similares entre sí que dos mediciones de corredores distintos
- **Consecuencia:** los errores estándar son artificialmente pequeños → conclusiones demasiado confiadas → inferencia incorrecta
- **Metáfora del libro:** asumir que todos los estudiantes de todas las escuelas son equivalentes para estimar el efecto de un maestro

#### 2. No Pooling

- **Supuesto:** cada grupo es un universo independiente — parámetros separados sin relación entre sí
- **Implementación:** un modelo independiente por grupo (36 regresiones para 36 corredores)
- **Problema 1:** con pocos datos por grupo, las estimaciones son inestables y tienen alta varianza
- **Problema 2:** no se puede predecir para grupos nuevos (un corredor que no estaba en el entrenamiento)
- **Problema 3:** ignora información valiosa: lo que sabemos de un corredor es relevante para entender a otro de edad similar
- **Metáfora del libro:** tratar cada escuela como si no tuviera nada que ver con las demás

#### 3. Partial Pooling (Modelos Jerárquicos)

- **Supuesto:** los grupos son distintos pero provienen de la misma población — comparten estructura
- **Idea clave:** *"cada grupo es único... pero todos los grupos están conectados y contienen información valiosa sobre los demás"*
- **Implementación:** los parámetros de grupo ($\mu_j$) se modelan como variables aleatorias con distribución propia
- **Ventaja 1:** grupos con pocos datos se "aprietan" (shrinkage) hacia la media global — reducen varianza a costa de algo de sesgo
- **Ventaja 2:** grupos con muchos datos mantienen sus estimaciones propias
- **Ventaja 3:** permite predecir grupos nuevos usando la distribución poblacional
- **Metáfora del libro:** reconocer que las escuelas operan bajo el mismo sistema educativo, aunque cada una sea distinta

### Concepto de Shrinkage

El shrinkage es el fenómeno por el cual las estimaciones jerárquicas se acercan a la media global comparado con las estimaciones no-pooling. La intensidad del shrinkage depende de:

1. **Tamaño del grupo:** grupos pequeños → más shrinkage (se confía menos en los datos propios)
2. **Variabilidad entre grupos** (σ_μ): si los grupos son muy distintos, hay menos shrinkage
3. **Variabilidad dentro del grupo** (σ_y): si hay mucho ruido dentro del grupo, más shrinkage

### Por qué el capítulo es importante

- Es el puente conceptual que justifica toda la maquinaria matemática de los capítulos 16 y 17
- Sin entender la motivación, las fórmulas parecen arbitrarias
- El argumento central: **no es que los datos grupales sean complicados — es que ignorar la estructura grupal es una elección activa con consecuencias estadísticas concretas**

---

## Capítulo 16 — Hierarchical Models Without Predictors

### Idea central

Construir el modelo jerárquico más simple posible: sin predictores, solo media por grupo. El objetivo es entender la estructura matemática antes de añadir complejidad.

### Dataset: Spotify

- **350 canciones** de **44 artistas**
- Variable respuesta: popularidad (escala 0–100)
- Número de canciones por artista: heterogéneo (algunos con 2, otros con 25+)
- Estructura jerárquica: canciones dentro de artistas

### Los tres modelos formales

#### Complete Pooling

$$Y_{ij} \mid \mu, \sigma_y \sim \mathcal{N}(\mu, \sigma_y^2)$$

Un solo parámetro $\mu$ para todas las canciones de todos los artistas. La pertenencia al artista no entra en el modelo.

#### No Pooling

$$Y_{ij} \mid \mu_j, \sigma_y \sim \mathcal{N}(\mu_j, \sigma_y^2)$$
$$\mu_j \sim \mathcal{N}(50, 25^2) \quad \text{(prior independiente por artista)}$$

Cada artista $j$ tiene su propio parámetro $\mu_j$, estimado sin comunicación con los demás artistas.

#### Modelo Jerárquico (Partial Pooling)

**Nivel 1 — Canción dentro del artista:**
$$Y_{ij} \mid \mu_j, \sigma_y \sim \mathcal{N}(\mu_j, \sigma_y^2)$$

**Nivel 2 — Artista dentro de la población:**
$$\mu_j \mid \mu, \sigma_\mu \sim \mathcal{N}(\mu, \sigma_\mu^2)$$

**Distribuciones a priori (hiperpriors):**
$$\mu \sim \mathcal{N}(50, 25^2)$$
$$\sigma_y \sim \text{Exp}(1)$$
$$\sigma_\mu \sim \text{Exp}(1)$$

### Parámetros clave y su interpretación

| Parámetro | Nombre | Interpretación |
|-----------|--------|----------------|
| $\mu$ | Media global | Popularidad promedio de cualquier artista en la población |
| $\sigma_\mu$ | Desv. estándar entre grupos | ¿Cuánto varían los artistas en términos de popularidad media? |
| $\mu_j$ | Media del artista $j$ | Popularidad media del artista $j$ específicamente |
| $\sigma_y$ | Desv. estándar dentro del grupo | ¿Cuánto varían las canciones de un mismo artista? |

### Descomposición de la varianza

La varianza total de una observación se descompone en:

$$\text{Var}(Y_{ij}) = \sigma_\mu^2 + \sigma_y^2$$

- $\sigma_\mu^2$: variabilidad entre artistas (entre grupos)
- $\sigma_y^2$: variabilidad entre canciones del mismo artista (dentro del grupo)

### Correlación intragrupo (ICC)

$$\rho = \frac{\sigma_\mu^2}{\sigma_\mu^2 + \sigma_y^2}$$

- $\rho \approx 1$: casi toda la variación viene de diferencias entre artistas (grupos muy distintos)
- $\rho \approx 0$: los artistas son indistinguibles — usar complete pooling sería razonable
- Interpretación práctica: dos canciones del mismo artista tienen correlación $\rho$ entre sí

### Shrinkage: formalización

La estimación jerárquica de $\mu_j$ es un promedio ponderado entre:
- La media bruta del grupo: $\bar{Y}_j$
- La media global: $\mu$

El peso del shrinkage hacia la media global aumenta cuando:
- $n_j$ (número de canciones del artista) es pequeño
- $\sigma_\mu$ es pequeño relativo a $\sigma_y$ (los artistas no son tan distintos)

### Implementación en R (rstanarm)

```r
library(rstanarm)
modelo_jerarquico <- stan_glmer(
  popularity ~ (1 | artist),
  data = spotify,
  family = gaussian,
  prior_intercept = normal(50, 25),
  prior_aux = exponential(1),
  prior_covariance = decov(reg = 1, conc = 1, shape = 1, scale = 1)
)
```

La sintaxis `(1 | artist)` especifica intercepts aleatorios por artista.

### Herramientas de diagnóstico y visualización

| Función | Paquete | Uso |
|---------|---------|-----|
| `mcmc_trace()` | bayesplot | Verificar convergencia de las cadenas |
| `pp_check()` | bayesplot | Posterior predictive check |
| `ppc_intervals()` | bayesplot | Intervalos de predicción por grupo |
| `spread_draws()` | tidybayes | Extraer muestras del posterior |
| `mean_qi()` | tidybayes | Resumen del posterior (media + HDI) |
| `tidy()` | broom.mixed | Tabla de coeficientes |

### Grupos como variables de agrupamiento vs. predictores

El libro hace una distinción importante:
- **Variable de agrupamiento** (ej. `artist`): define la jerarquía, sus niveles son una muestra de una población mayor → se modela con efectos aleatorios
- **Variable predictora** (ej. `genre`): sus niveles son *todos* los relevantes → se modela con efectos fijos

Regla práctica: si pudieras haber observado otros valores posibles de esa variable (otros artistas, otras escuelas), es una variable de agrupamiento.

---

## Capítulo 17 — Normal Hierarchical Models with Predictors

### Idea central

Extender el modelo jerárquico para incluir predictores continuos. Ahora cada grupo puede tener no solo una media distinta (intercept) sino también una relación distinta con el predictor (slope).

### Dataset: Running (Cherry Blossom)

- **252 observaciones** de **36 corredores** (mismos datos que cap. 15)
- Variable respuesta: tiempo neto de carrera (minutos)
- Predictor: edad del corredor (centrada en la media del dataset)
- Estructura jerárquica: observaciones anidadas dentro de corredores

### Los tres modelos comparados

#### Modelo 1: Regresión Pooled

$$Y_{ij} \mid \beta_0, \beta_1, \sigma \sim \mathcal{N}(\beta_0 + \beta_1 \cdot \text{age}_{ij}, \sigma^2)$$

Una sola recta de regresión. Supone que la relación edad-tiempo es igual para todos los corredores y el punto de partida también.

**Problema:** los 36 corredores son muy distintos en velocidad base y en cómo envejecen.

#### Modelo 2: Random Intercepts

**Nivel 1:**
$$Y_{ij} \mid \beta_{0j}, \beta_1, \sigma_y \sim \mathcal{N}(\beta_{0j} + \beta_1 \cdot \text{age}_{ij},\; \sigma_y^2)$$

**Nivel 2:**
$$\beta_{0j} \mid \beta_0, \sigma_0 \sim \mathcal{N}(\beta_0, \sigma_0^2)$$

**Priors:**
$$\beta_0 \sim \mathcal{N}(0, 35^2), \quad \beta_1 \sim \mathcal{N}(0, 2.5^2), \quad \sigma_y \sim \text{Exp}(1), \quad \sigma_0 \sim \text{Exp}(1)$$

Cada corredor tiene su propia velocidad base ($\beta_{0j}$), pero todos comparten la misma pendiente de edad ($\beta_1$). Supone que todos envejecen al mismo ritmo.

**Sintaxis R:**
```r
net ~ age_c + (1 | runner)
```

#### Modelo 3: Random Intercepts + Slopes

**Nivel 1:**
$$Y_{ij} \mid \beta_{0j}, \beta_{1j}, \sigma_y \sim \mathcal{N}(\beta_{0j} + \beta_{1j} \cdot \text{age}_{ij},\; \sigma_y^2)$$

**Nivel 2 (bivariado):**
$$\begin{pmatrix}\beta_{0j}\\ \beta_{1j}\end{pmatrix} \mid \beta_0, \beta_1, \Sigma \sim \mathcal{N}_2\!\left(\begin{pmatrix}\beta_0\\ \beta_1\end{pmatrix},\; \Sigma\right)$$

Donde $\Sigma$ es la matriz de covarianza:
$$\Sigma = \begin{pmatrix}\sigma_0^2 & \rho\,\sigma_0\,\sigma_1 \\ \rho\,\sigma_0\,\sigma_1 & \sigma_1^2\end{pmatrix}$$

**Sintaxis R:**
```r
net ~ age_c + (age_c | runner)
```

El parámetro $\rho$ captura la correlación entre la velocidad base y la tasa de envejecimiento: ¿los corredores más rápidos envejecen más rápido o más lento?

### Parámetros del modelo de random slopes

| Parámetro | Interpretación |
|-----------|----------------|
| $\beta_0$ | Tiempo medio global a la edad centrada |
| $\beta_1$ | Efecto global de la edad (minutos adicionales por año) |
| $\beta_{0j}$ | Tiempo base del corredor $j$ |
| $\beta_{1j}$ | Efecto de la edad para el corredor $j$ específico |
| $\sigma_0$ | Variabilidad entre corredores en velocidad base |
| $\sigma_1$ | Variabilidad entre corredores en tasa de envejecimiento |
| $\rho$ | Correlación entre intercept y slope de cada corredor |
| $\sigma_y$ | Variabilidad de una carrera a otra del mismo corredor |

### Prior de decov (descomposición de covarianza)

El libro usa el prior `decov` de rstanarm para la matriz $\Sigma$, que descompone la especificación en:
1. **Correlación:** prior LKJ sobre la correlación $\rho$ entre parámetros
2. **Escala:** prior sobre las desviaciones estándar $\sigma_0, \sigma_1$
3. **Regularización:** penaliza correlaciones extremas

Esta descomposición es más estable numéricamente que especificar $\Sigma$ directamente.

### Predicción en modelos jerárquicos

El capítulo distingue dos escenarios de predicción con implicaciones muy distintas:

#### Corredor conocido (in-sample)

- Se usa el posterior de $\beta_{0j}$ y $\beta_{1j}$ del corredor específico
- El intervalo de predicción es **más estrecho** — tenemos información del corredor
- Fórmula: $\tilde{Y} \mid \beta_{0j}, \beta_{1j}, \text{age} \sim \mathcal{N}(\beta_{0j} + \beta_{1j} \cdot \text{age}, \sigma_y^2)$

#### Corredor nuevo (out-of-sample)

- Se muestrea primero un nuevo $(\beta_{0,\text{new}}, \beta_{1,\text{new}})$ de la distribución poblacional
- Luego se predice la carrera condicionada a esos parámetros nuevos
- El intervalo de predicción es **más ancho** — hay incertidumbre extra sobre quién es el corredor
- Esta honestidad sobre la incertidumbre es una de las ventajas del enfoque bayesiano jerárquico

### Comparación de modelos con LOO-CV

El libro usa **Leave-One-Out Cross-Validation** (LOO-CV) implementado en el paquete `loo` (ArviZ en Python):

- **ELPD** (Expected Log Predictive Density): métrica principal — más alto es mejor
- Se compara la diferencia de ELPD entre modelos y su error estándar
- Si la diferencia es mayor que 2 errores estándar, el modelo superior es significativamente mejor

Resultado típico con estos datos:
- El modelo pooled tiene ELPD significativamente peor
- Random intercepts y random slopes tienen ELPD similar, con leve ventaja del segundo
- Conclusión: los corredores difieren más en velocidad base que en tasa de envejecimiento

### Evaluación del modelo

El libro recomienda la siguiente secuencia de diagnósticos antes de interpretar resultados:

1. **Trace plots** (`mcmc_trace`): verificar que las cadenas se mezclan sin tendencias ni atascos
2. **R̂ (Gelman-Rubin)**: debe ser < 1.01 para todos los parámetros
3. **ESS (Effective Sample Size)**: debe ser > 400 (idealmente > 1000) para estimaciones estables
4. **Posterior Predictive Check** (`pp_check`): los datos simulados deben parecerse a los reales

### Herramientas R para el capítulo 17

| Función | Paquete | Uso |
|---------|---------|-----|
| `stan_glmer()` | rstanarm | Ajustar modelos jerárquicos con Stan |
| `add_fitted_draws()` | tidybayes | Muestras de la línea de regresión posterior |
| `add_predicted_draws()` | tidybayes | Muestras de predicción incluyendo σ_y |
| `spread_draws()` | tidybayes | Extraer muestras de cualquier parámetro |
| `mcmc_dens_overlay()` | bayesplot | Densidades del posterior por cadena |
| `loo_compare()` | loo | Comparar modelos con LOO-CV |

---

## Conexión entre los tres capítulos

```
Cap. 15 — MOTIVACIÓN
"¿Por qué no alcanza con una sola ecuación?"
    ↓ muestra que complete pooling y no pooling tienen problemas sistemáticos
    ↓ introduce el concepto de partial pooling y shrinkage

Cap. 16 — ESTRUCTURA BÁSICA
"¿Cómo construyo el modelo más simple?"
    ↓ formaliza el modelo jerárquico de dos niveles sin predictores
    ↓ introduce σ_μ, σ_y, correlación intragrupo, diagnósticos MCMC

Cap. 17 — CON PREDICTORES
"¿Y si quiero agregar variables explicativas?"
    ↓ extiende a random intercepts y random slopes
    ↓ introduce la Normal bivariada, la correlación ρ, y la predicción fuera de muestra
```

### La idea que une todo

El modelo jerárquico resuelve una tensión fundamental en estadística:

> **¿Cómo aprendo de los datos de un grupo específico sin desperdiciar la información que los otros grupos contienen sobre él?**

La respuesta: tratando los parámetros de grupo como variables aleatorias que comparten una distribución común. Esa distribución es la que permite el intercambio de información — y esa es la esencia del enfoque bayesiano jerárquico.

---

## Setup técnico del libro (Prefacio)

**Lenguaje:** R  
**Paquetes principales:**

| Paquete | Función principal |
|---------|------------------|
| `rstan` / `rstanarm` | Ajustar modelos bayesianos con Stan |
| `bayesrules` | Datasets del libro (spotify, running, etc.) |
| `tidyverse` | Manipulación y visualización de datos |
| `bayesplot` | Visualizaciones de posteriors y diagnósticos MCMC |
| `tidybayes` | Integración de posteriors con tidyverse |
| `broom.mixed` | Tablas de coeficientes para modelos mixtos |

**Conocimientos previos requeridos:**
- Estadística introductoria (distribuciones, hipótesis, regresión)
- Algo de cálculo y probabilidad
- R básico (tidyverse)
