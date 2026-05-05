# 📘 Guía Completa y Detallada: Modelos Jerárquicos en Estadística Bayesiana

------------------------------------------------------------------------

# 🎯 Objetivo de esta guía

Esta guía te permite: - Entender profundamente qué es un modelo
jerárquico - Explicarlo de forma clara en exposición o entrega - Cubrir
todos los puntos solicitados: 1. Motivación 2. Formulación 3.
Parametrización 4. Inferencia y diagnóstico

------------------------------------------------------------------------

# 🔷 1. ¿Qué es un modelo jerárquico?

Un modelo jerárquico es un modelo probabilístico donde los parámetros
también son variables aleatorias y están organizados en múltiples
niveles.

## 💡 Idea clave

No solo modelamos los datos, sino también cómo se generan los
parámetros.

## 🧠 Intuición

Estructura en capas: - Nivel 1: datos - Nivel 2: parámetros de grupo -
Nivel 3: parámetros globales

## 📌 Ejemplo

Notas por curso: - Cada curso tiene una media - Pero todas las medias
vienen de una distribución común

------------------------------------------------------------------------

# 🔷 2. Motivación

## ⚠️ Problema clásico

### No pooling

-   Cada grupo independiente
-   Alta varianza

### Pooling completo

-   Todos iguales
-   Alto sesgo

## ✅ Solución: Pooling parcial

Los modelos jerárquicos combinan lo mejor de ambos mundos.

## 🔥 Concepto clave: Shrinkage

Los grupos con pocos datos se acercan al promedio global.

------------------------------------------------------------------------

# 🔷 3. Formulación del modelo

## Nivel 1 (datos)

y_ij \~ Normal(θ_j, σ²)

## Nivel 2 (parámetros)

θ_j \~ Normal(μ, τ²)

## Nivel 3 (hiperparámetros)

μ, τ \~ priors

## 🎯 Interpretación

-   θ_j: parámetro de grupo
-   μ: promedio global
-   τ: variabilidad entre grupos

------------------------------------------------------------------------

# 🔷 4. Parametrización

## 🔹 Centrada

θ_j \~ Normal(μ, τ²)

## 🔹 No centrada

θ_j = μ + τ \* η_j\
η_j \~ Normal(0,1)

## 💡 Intuición

Separar componentes mejora la eficiencia del muestreo.

## 📊 Cuándo usar cada una

-   Muchos datos → centrada
-   Pocos datos → no centrada

------------------------------------------------------------------------

# 🔷 5. Inferencia

## 🔧 Métodos

-   Gibbs Sampling
-   Metropolis-Hastings
-   HMC

## 🎯 Idea

Simular muestras de la distribución posterior.

------------------------------------------------------------------------

# 🔷 6. Diagnóstico

## R-hat

Debe ser cercano a 1.

## ESS

Número de muestras efectivas.

## Trace plots

Deben verse como ruido estable.

## Otros

-   Autocorrelación
-   Divergencias

------------------------------------------------------------------------

# 🔷 7. Conclusión

Los modelos jerárquicos permiten: - Compartir información - Reducir
varianza - Mejorar inferencia

------------------------------------------------------------------------

# 🎤 GUÍA PARA DIAPOSITIVAS

## Diapositiva 1: Definición

📊 Imagen: - Diagrama de niveles (capas)

## Diapositiva 2: Motivación

📊 Gráfico: - No pooling vs pooling vs parcial

## Diapositiva 3: Shrinkage

📊 Gráfico: - Puntos moviéndose hacia la media

## Diapositiva 4: Modelo

📊 Diagrama de placas

## Diapositiva 5: Parametrización

📊 Neal funnel (centrada vs no centrada)

## Diapositiva 6: Inferencia

📊 Cadenas MCMC

## Diapositiva 7: Diagnóstico

📊 Trace plots y R-hat

## Diapositiva 8: Conclusión

📊 Flujo del modelo
