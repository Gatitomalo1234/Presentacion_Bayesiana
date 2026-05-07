# GUION — RPG BAYESIANO

### Modelos Jerarquicos con Estadistica Bayesiana

**Duracion estimada:** 1h 15min

---

## Mapa de la presentacion

| Seccion | Tema | Tiempo |
|---|---|---|
| Apertura | Contexto + click-to-start | 3 min |
| Hub | Bienvenida + mapa del viaje | 4 min |
| Nivel 1 | El Problema — por que no alcanza una sola ecuacion | 14 min |
| Nivel 2 | Pooling — mezclar todo vs separar todo | 14 min |
| Nivel 3 | Modelo Jerarquico — conectar grupos | 14 min |
| Nivel 4 | Shrinkage — compartir informacion | 12 min |
| Nivel 5 | Inferencia + MCMC — como se calcula | 12 min |
| Sala del Dragon | Cierre — derrotar el overfitting | 5 min |

---

## Idea fuerza del guion

La presentacion entera responde una sola pregunta:

> **Como aprendemos de un grupo sin desperdiciar lo que los otros grupos nos dicen sobre el?**

El hilo que conviene cuidar en vivo es:

1. Los datos tienen estructura de grupos.
2. `Complete pooling` y `no pooling` son extremos.
3. `Partial pooling` conecta grupos mediante una distribucion comun.
4. Esa conexion produce `shrinkage`.
5. En Bayes, la inferencia se hace via posterior + MCMC.

Eso es justamente lo que el `SUMMER` explica bien: primero la arquitectura, luego la comparacion entre estrategias, y despues la intuicion del modelo jerarquico.

---

## ⏱ APERTURA (3 min)

> *Se muestra la pantalla de inicio con los tres personajes.*

Buenos dias / Buenas tardes. Bienvenidos a esta presentacion.

Hoy vamos a hablar de modelos jerarquicos bayesianos. Suena tecnico, pero la intuicion central es muy natural: cuando los datos vienen agrupados, ignorar esa estructura nos lleva a decisiones malas.

Para hacerlo mas llevadero, lo vamos a presentar como un juego de rol. Cada nivel del juego corresponde a una idea clave. Pero debajo de la estetica del juego hay una pregunta estadistica muy concreta:

> **Como aprendemos de un grupo sin perder la informacion que los otros grupos contienen sobre el?**

> *Click en la pantalla. Arranca la animacion del juego.*

---

## ⏱ HUB — Sala de los Sabios (4 min)

> *Se muestra el hub con las 5 puertas.*

Esta es la Sala de los Sabios. Desde aca vemos los cinco temas del viaje.

Las puertas corresponden a:

- La **azul**: el problema
- La **morada**: pooling
- La **verde**: modelo jerarquico
- La **amarilla**: shrinkage
- La **roja**: inferencia

Todo lo vamos a explicar con un ejemplo que nos va a acompanar casi toda la presentacion: turistas en tres ciudades colombianas — Cartagena, Medellin y Bogota. Queremos predecir cuanto gasta un turista segun cuantos dias se queda.

Ese ejemplo tiene exactamente la estructura que necesitamos:

- individuos: turistas
- grupos: ciudades
- poblacion: Colombia

Y con esa estructura vamos a comparar tres maneras de modelar:

- mezclar todo
- separar todo
- conectar grupos

Con ese mapa en la cabeza, entramos al primer nivel.

---

## ⏱ NIVEL 1 — El Problema (14 min)

> *El personaje entra por la puerta azul.*

Primer nivel: **el problema**.

Cuando los datos tienen estructura de grupos, los modelos estandar fallan de maneras bastante predecibles.

En nuestro ejemplo, tenemos turistas en Cartagena, Medellin y Bogota. La pregunta es simple:

> **Como predecimos cuanto va a gastar un turista?**

### La primera tentacion

Lo mas natural seria juntar todos los datos y ajustar una sola regresion:

`dias -> gasto`

Una sola recta para todos.

Eso suena razonable, pero oculta algo importante: las ciudades no son iguales. Un turista en Cartagena puede gastar distinto a uno en Bogota, incluso quedandose el mismo numero de dias.

Entonces esa recta unica termina siendo una recta promedio: estable, si, pero ciega a las diferencias reales entre ciudades.

### La segunda tentacion

La reaccion opuesta es decir: entonces hagamos una recta por ciudad.

Cartagena tiene su modelo. Medellin tiene el suyo. Bogota el suyo.

Ahora el problema cambia: con muy pocos turistas por ciudad, cada recta se vuelve inestable. Un dato raro puede mover mucho la estimacion.

Y aparece un segundo limite: si llega una ciudad nueva, por ejemplo Cali, ese enfoque no tiene como arrancar porque nunca estimo parametros para Cali.

### La pregunta correcta

La pregunta de fondo no es "una recta o muchas rectas". La pregunta correcta es:

> **Como aprendo de los datos de una ciudad sin ignorar lo que las otras ciudades me dicen sobre ella?**

Eso es lo que motiva todo lo que sigue.

### Intercambiabilidad

Hay una idea tecnica detras de esto: **intercambiabilidad**.

La forma mas simple de decirlo es esta: si dentro de un grupo puedo permutar observaciones sin cambiar sustancialmente lo que aprendo, entonces esas observaciones comparten una estructura comun.

Eso no significa que sean identicas. Significa que tiene sentido modelarlas como realizaciones de un mismo proceso de grupo.

Y si los grupos tambien comparten una estructura comun, entonces aparece la posibilidad de aprender entre grupos.

> *El personaje abre el cofre brillante.*

**Concepto del cofre:** Intercambiabilidad. Los datos dentro de un grupo comparten estructura, y eso es lo que nos permite construir modelos que aprenden entre grupos.

---

## ⏱ NIVEL 2 — Pooling (14 min)

> *El personaje vuelve al hub y entra por la puerta morada.*

Segundo nivel: **pooling**.

Pooling, en esencia, significa: cuanto compartimos informacion entre grupos.

Vamos a ver dos estrategias extremas. Esto es importante porque el `SUMMER` justamente organiza la historia asi: primero `complete pooling`, despues `no pooling`, y recien ahi aparece `partial pooling`.

### Estrategia 1 — Complete Pooling

`Complete pooling` significa: un solo modelo para todas las ciudades.

En nuestro ejemplo:

```text
gasto_i = mu + beta * dias_i + error_i
```

Hay un solo intercepto y una sola pendiente.

**Que gana este enfoque?**

- estabilidad
- simplicidad

**Que pierde?**

- diferencias reales entre ciudades

Si Cartagena, Medellin y Bogota tienen patrones distintos, una sola recta no representa bien a ninguna en particular.

Entonces el problema de `complete pooling` no es que "este mal hecho". El problema es que es **demasiado rigido** para datos agrupados.

### Estrategia 2 — No Pooling

`No pooling` significa: un modelo separado por ciudad.

```text
gasto_ij = mu_j + beta_j * dias_ij + error_ij
```

Cada ciudad tiene su intercepto y su pendiente. Los grupos no comparten nada.

**Que gana este enfoque?**

- flexibilidad local

**Que pierde?**

- estabilidad
- capacidad de generalizar

Con pocos datos por ciudad, las estimaciones se vuelven muy variables. Ademas, si aparece Cali, el modelo no tiene parametros para Cali. Y lo mas importante: estamos desperdiciando informacion que si podria compartirse entre ciudades.

Entonces:

- `complete pooling` es estable pero borra heterogeneidad
- `no pooling` captura heterogeneidad pero con alta varianza

### Resumen del nivel

| Estrategia | Nombre tecnico | Problema principal |
|---|---|---|
| Mezclar todo | Complete Pooling | sesgo por exceso de homogeneidad |
| Separar todo | No Pooling | alta varianza por fragmentacion |

Necesitamos algo intermedio:

> **una forma de permitir diferencias entre grupos sin romper la posibilidad de compartir informacion**

> *El personaje abre el cofre.*

**Concepto del cofre:** Pooling. Ni mezclar todo ni separar todo es suficiente. La solucion esta en el balance.

---

## ⏱ NIVEL 3 — El Modelo Jerarquico (14 min)

> *El personaje entra por la puerta verde.*

Tercer nivel: la solucion. El **modelo jerarquico**, o si usamos el lenguaje de comparacion de estrategias, **partial pooling**.

La idea central es esta:

> los grupos son distintos, pero provienen de una misma poblacion

Esa poblacion comun no borra las diferencias. Las organiza.

### La arquitectura en capas

En este ejemplo conviene pensarlo en **tres niveles**.

**Nivel 1 — datos observados**

```text
gasto_ij = mu_j + beta_j * dias_ij + error_ij
```

Cada ciudad tiene su propia recta. Hasta aca, se parece a `no pooling`.

**Nivel 2 — parametros de ciudad**

```text
mu_j   ~ N(mu_0, sigma_mu^2)
beta_j ~ N(beta_0, sigma_beta^2)
```

Los parametros de cada ciudad no se estiman como islas separadas. Vienen de una distribucion comun.

**Nivel 3 — hiperparametros**

- `mu_0` y `beta_0`: tendencia global
- `sigma_mu` y `sigma_beta`: cuanta variacion hay entre ciudades

Eso es exactamente la jerarquia que hemos venido mostrando en slides:

```text
Colombia -> ciudades -> turistas
```

### La intuicion

Una buena intuicion es pensar en una familia. Los hermanos no son iguales, pero si comparten origen. Cada uno tiene rasgos propios, pero esos rasgos no aparecen de la nada.

En nuestro modelo, las ciudades son como esos hermanos:

- cada ciudad tiene sus propios parametros
- esos parametros vienen de una distribucion comun

Por eso, si Cartagena tiene pocos datos, no queda sola. Puede aprender del conjunto, sin ser forzada a ser igual a Medellin o Bogota.

### La ventaja para ciudades nuevas

Si aparece Cali:

- `complete pooling`: la trata como si fuera el promedio de todos
- `no pooling`: no tiene nada para decir
- `partial pooling`: usa la distribucion poblacional para proponer parametros razonables para Cali

Esa es una ventaja clave: **generalizar a grupos nuevos**.

### El mensaje clave del nivel

El modelo jerarquico no dice "todas las ciudades son iguales".

Dice algo mas interesante:

> **las ciudades son diferentes, pero esas diferencias tienen estructura**

> *El personaje abre el cofre.*

**Concepto del cofre:** Modelo jerarquico. Datos en nivel 1, parametros de grupo en nivel 2, hiperparametros en nivel 3. La jerarquia permite compartir informacion sin forzar igualdad.

---

## ⏱ NIVEL 4 — Shrinkage (12 min)

> *El personaje entra por la puerta amarilla.*

Cuarto nivel: **shrinkage**.

Si el modelo jerarquico es la estructura, shrinkage es el efecto visible de esa estructura.

### Que es shrinkage

Las estimaciones de grupos pequenos se mueven hacia el promedio global.

No porque el modelo "desconfie" de esos grupos por capricho, sino porque con pocos datos es estadisticamente razonable prestar mas atencion a la informacion colectiva.

### Forma intuitiva

En el caso mas simple, una estimacion jerarquica puede leerse asi:

```text
estimacion_j = lambda_j * evidencia_local + (1 - lambda_j) * promedio_global
```

La lectura es:

- si `lambda_j` es grande, manda el grupo
- si `lambda_j` es chico, pesa mas el promedio global

### De que depende la fuerza del shrinkage

1. Del tamano del grupo: grupos pequenos -> mas shrinkage.
2. De la variacion entre grupos: si los grupos son muy parecidos, mas shrinkage.
3. Del ruido en los datos: mas ruido -> mas shrinkage.

### Como leer el grafico

En el dumbbell plot, un punto muestra la estimacion local y el otro la estimacion jerarquica. La linea entre ambos muestra cuanto se movio el grupo.

La lectura importante no es solo "todos se acercan al centro".

La lectura importante es:

- los grupos pequenos se corrigen mas
- los grupos grandes se corrigen menos

Es decir: el modelo no regulariza a todos por igual. Regulariza segun la informacion disponible.

### Por que esto es bueno

Porque cambia un poco de sesgo por una reduccion importante de varianza. Y en grupos con pocos datos, ese intercambio mejora mucho la estabilidad y la prediccion.

Eso es justamente lo que hace que el modelo jerarquico combata el sobreajuste.

> *El personaje abre el cofre.*

**Concepto del cofre:** Shrinkage. Los grupos pequenos se acercan mas al promedio global. No es un defecto del modelo; es una de sus ventajas principales.

---

## ⏱ NIVEL 5 — Inferencia y MCMC (12 min)

> *El personaje entra por la puerta roja.*

Quinto nivel: **inferencia**.

Ya construimos el modelo. Ahora viene la pregunta practica:

> **como obtenemos la posterior?**

En modelos jerarquicos reales, esa posterior no suele tener forma cerrada. Entonces la aproximamos por simulacion. Y ahi aparece MCMC.

### Que es MCMC

MCMC significa `Markov Chain Monte Carlo`.

- `Monte Carlo`: aproximar por simulacion
- `Markov Chain`: generar una secuencia donde cada paso depende del estado actual

La idea es producir muestras que, al cabo de suficientes iteraciones, se distribuyan como la posterior que nos interesa.

### HMC y por que importa

El algoritmo que usa Stan es `Hamiltonian Monte Carlo`.

La intuicion corta es esta: en vez de moverse a ciegas, usa informacion de la geometria local de la posterior para explorarla de forma mucho mas eficiente.

### El problema geometrico: el Embudo de Neal

En modelos jerarquicos puede aparecer una geometria dificil. Cuando una varianza de grupo es muy pequena, los parametros locales quedan muy apretados alrededor del promedio global. Eso genera una forma tipo embudo.

Ese embudo no cambia el significado estadistico del modelo, pero si dificulta la exploracion:

- peor mezcla
- mas autocorrelacion
- posibles divergencias

### La solucion: parametrizacion no centrada

La idea es reescribir el modelo.

**Centrada:**

```text
mu_j ~ Normal(mu_0, sigma_mu^2)
```

**No centrada:**

```text
mu_j = mu_0 + sigma_mu * eta_j
eta_j ~ Normal(0, 1)
```

Matematicamente representan lo mismo, pero computacionalmente no se comportan igual. La version no centrada suele ayudar mucho cuando hay pocos datos por grupo o cuando la geometria se parece a un embudo.

### Diagnosticos: el orden importa

Antes de interpretar la posterior, conviene revisar tres cosas y en este orden:

**1. Trace plots**

Las cadenas deben verse como ruido estable: mezcladas, cruzandose y sin tendencias.

**2. R-hat**

Debe ser cercano a 1. Regla practica: menor que `1.01`.

**3. ESS**

Cantidad de muestras efectivas despues de descontar autocorrelacion. Regla practica: al menos `400`, idealmente mas de `1000`.

Si estas tres piezas se ven bien, entonces si podemos confiar en las estimaciones.

> *El personaje abre el cofre.*

**Concepto del cofre:** Geometria del MCMC. La calidad de la inferencia depende tanto del modelo estadistico como de la forma en que lo parametrizamos.

---

## ⏱ SALA DEL DRAGON — Conclusion (5 min)

> *El personaje llega a la Sala del Dragon.*

Llegamos al jefe final: el Dragon del Overfitting.

En este contexto, el overfitting aparece con facilidad cuando tratamos a grupos pequenos como si sus datos fueran suficientes para sostener parametros completamente independientes.

El modelo jerarquico lo combate porque el shrinkage funciona como una regularizacion natural.

Resumen de la logica completa:

- **El Problema:** los datos vienen agrupados; una sola ecuacion no alcanza.
- **Pooling:** `complete pooling` sesga; `no pooling` varia demasiado.
- **Modelo Jerarquico:** `partial pooling` conecta grupos mediante una distribucion comun.
- **Shrinkage:** los grupos pequenos se corrigen mas; los grandes conservan mas informacion propia.
- **Inferencia:** HMC y una buena parametrizacion nos permiten calcular la posterior de forma confiable.

Entonces, si quisieramos resumir toda la presentacion en una sola idea, seria esta:

> **Modelar grupos no es elegir entre ignorar diferencias o exagerarlas. Es construir una estructura donde las diferencias existan, pero tambien puedan aprender unas de otras.**

Esa es la esencia de los modelos jerarquicos bayesianos.

Muchas gracias. Si tienen preguntas, estamos aqui.
