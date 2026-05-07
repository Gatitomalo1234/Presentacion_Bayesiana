# Plan: Presentación Bayesiana — Reestructuración completa

## Contexto

La presentación tiene estructura rota (slides duplicados s8–s12), narrativa desconectada, y aún no incorpora la metodología de SUMMER.pdf. Se hace una reescritura completa de `presentacion.html` con:
- Nuevo orden de slides siguiendo la narrativa de `estructura_presentacion.md`
- Ejemplo base: turismo colombiano (Cartagena, Medellín, Bogotá) tomado de SUMMER.pdf
- Shrinkage mucho más visual (panel de ciudades con flechas, ligado al ejemplo del turismo)
- Slides de pooling movidas antes del modelo formal
- Nueva slide de comparación gráfica de los tres modelos (tipo SUMMER: tres regresiones separadas)
- Modelo jerárquico explicado en dos partes: primero conceptual/esquemático, luego fórmulas Normal-Normal
- Parametrización centrada y no centrada: fórmula lado a lado usando el modelo de regresión del turismo, con cada parte de la fórmula anotada

**Archivo a modificar:** `presentacion.html`

---

## Datos del ejemplo base (SUMMER.pdf)

- **Ciudades:** Cartagena, Medellín, Bogotá (j = 1, 2, 3)
- **Turistas por ciudad:** 5 por ciudad = 15 obs totales
- **Variable respuesta:** gasto total (USD)
- **Predictor:** días de estadía (`days`)
- **Ecuación base:** `Y_ij = α_j + β_j · days_ij + ε_ij`
- Valores sintéticos coherentes con SUMMER:
  - Cartagena: α ≈ 280, β ≈ 80/día, n = 5
  - Medellín: α ≈ 180, β ≈ 100/día, n = 5
  - Bogotá: α ≈ 230, β ≈ 90/día, n = 5
  - Media global: μ_α ≈ 230, μ_β ≈ 90

---

## Estructura final — 13 slides

### S1 — Portada (mantener, sin cambios)
- Título, subtítulo, nombres
- Nexttip: "No vamos a empezar con la definición — vamos a empezar con el problema."

---

### S2 — El problema: datos con estructura de grupos
**Tiempo estimado:** 5 min

**Contenido:**
- Introducir el dataset de turismo colombiano (SUMMER):
  - 15 turistas, 3 ciudades, miden gasto total y días de estadía
  - Tabla visual: Ciudad | N | Días promedio | Gasto promedio
- Chart.js scatter plot (`ch-scatter`): gasto vs días, coloreado por ciudad
  - Cartagena: OR (naranja), Medellín: BL (azul), Bogotá: GR (verde)
  - Datos sintéticos de SUMMER (5 pts por ciudad)
- Pregunta visible en pantalla: "¿Son estas 15 observaciones independientes?"
- Respuesta: No — turistas de la misma ciudad comparten contexto (precios, atracciones, temporada)
- Concepto de **Intercambiabilidad parcial** (De Finetti): dentro de ciudad = intercambiables; entre ciudades = no

**Nexttip:** "Entonces, ¿cómo han intentado resolver esto? Hay dos respuestas clásicas. Y las dos están mal."

---

### S3 — Las dos respuestas clásicas (y por qué fallan)
**Tiempo estimado:** 8 min

**Contenido — 3 columnas de cards:**

**Columna 1: Complete Pooling** (color magenta PK)
- Fórmula: `Y_i = α + β · days_i + ε_i`
- SVG inline: única recta de regresión sobre todos los puntos mezclados
- Problema: sesgo, ignora diferencias entre ciudades

**Columna 2: No Pooling** (color naranja OR)
- Fórmula: `Y_ij = α_j + β_j · days_ij + ε_ij`
- SVG inline: 3 rectas completamente independientes
- Problema: varianza alta con n=5, no predice ciudades nuevas

**Columna 3: Partial Pooling ✓** (color verde GR, borde destacado)
- Fórmulas:
  ```
  Y_ij = α_j + β_j · days_ij + ε_ij
  α_j ~ N(μ_α, σ²_α)
  β_j ~ N(μ_β, σ²_β)
  ```
- SVG inline: 3 rectas "jaladas" hacia una central
- Resultado: balance óptimo

**Tabla al pie:**
| Estrategia | Ecuación | Problema |
|------------|----------|----------|
| Complete Pooling | α + β·x | Ignora grupos |
| No Pooling | α_j + β_j·x | No comparte info |
| Partial Pooling | α_j + β_j·x, α_j~N(μ,σ²) | **Balance óptimo** |

**Nexttip:** "Lo que necesitamos está en el medio. Así se construye formalmente el modelo jerárquico."

---

### S4 — Nueva slide: Comparación gráfica de los tres modelos ← NUEVA
**Tiempo estimado:** 7 min

Inspirada en SUMMER pp. 8–12 (visualización de regresiones superpuestas).

**Layout: panel de 3 columnas, cada una con Chart.js scatter + línea(s)**

**Columna 1 — Complete Pooling:**
- Chart (`ch-pool-comp-1`): 15 puntos (3 colores), una sola línea magenta
- Título: "Una recta para todos"

**Columna 2 — No Pooling:**
- Chart (`ch-pool-comp-2`): 15 puntos, 3 líneas independientes (mismo color que puntos)
- Título: "Tres rectas completamente libres"

**Columna 3 — Partial Pooling:**
- Chart (`ch-pool-comp-3`): 15 puntos, 3 líneas jaladas entre sí
- Título: "Tres rectas que aprenden unas de otras"

**Implementación técnica:**
- Todos inicializados en `idx === 3` dentro de `initChart()`
- Líneas calculadas con datos sintéticos del turismo
  - Complete: α=230, β=90 para todos
  - No pool: α_j y β_j propios de cada ciudad
  - Partial: α_j y β_j shrinkageados hacia (μ_α, μ_β) con λ (n=5)

**Nexttip:** "Una vez calculado el modelo jerárquico, las estimaciones sufren un fenómeno fascinante: el shrinkage."

---

### S5 — ¿Qué es un modelo jerárquico? — Conceptual
**Tiempo estimado:** 6 min

**Layout: 2 columnas**

**Columna izquierda — Diagrama de placas SVG:**
- Nodo morado: `μ_α, σ_α, μ_β, σ_β` — hiperparámetros (latente)
- Nodo azul: `α_j, β_j` — parámetros de ciudad j (latente)
- Nodo verde relleno: `Y_ij` — observado
- Placa exterior: "j = 1..J ciudades"
- Placa interior: "i = 1..n_j turistas"
- Flechas entre nodos indicando dependencia

**Columna derecha — Los 3 niveles:**
1. **Nivel 3 — Hiperpriors (morado):**
   `μ_α ~ N(230, 100²)`, `σ_α ~ Exp(0.01)`, `μ_β ~ N(90, 50²)`, `σ_β ~ Exp(0.1)`
2. **Nivel 2 — Parámetros de ciudad (azul):**
   `α_j | μ_α, σ_α ~ N(μ_α, σ²_α)`, `β_j | μ_β, σ_β ~ N(μ_β, σ²_β)`
3. **Nivel 1 — Observaciones (verde):**
   `Y_ij | α_j, β_j ~ N(α_j + β_j · days_ij, σ²_y)`

**Nexttip:** "Con esta arquitectura en mente, veamos cómo se escribe esto en matemáticas formales."

---

### S6 — Modelo Normal-Normal: especificación formal ← NUEVA
**Tiempo estimado:** 8 min

**Layout: 2 columnas**

**Columna izquierda — Proceso generativo (cascada con línea conectora gradiente):**

Paso 1 — Población (ícono globo):
- `μ_α ~ N(230, 100²)`, `μ_β ~ N(90, 50²)`, `σ_α ~ Exp(0.01)`, `σ_β ~ Exp(0.1)`

Paso 2 — Ciudad j (ícono mapa):
- `α_j | μ_α, σ_α ~ N(μ_α, σ²_α)`
- `β_j | μ_β, σ_β ~ N(μ_β, σ²_β)`

Paso 3 — Turista ij (ícono usuario):
- `Y_ij | α_j, β_j, σ_y ~ N(α_j + β_j · days_ij, σ²_y)`

**Columna derecha — Actualización bayesiana:**
1. Prior: `p(α_j | μ_α, σ_α)` — lo que asumimos de la ciudad según Colombia
2. Likelihood: `p(Y | α_j, β_j, σ_y)` — evidencia de los datos de la ciudad
3. ─── Bayes ───
4. Posterior: `p(α_j | Y, μ_α, σ_α) ∝ Likelihood × Prior`

**Nexttip:** "El modelo tiene una propiedad fascinante: las estimaciones αⱼ no quedan libres — son atraídas hacia μ_α. Eso se llama shrinkage."

---

### S7 — Shrinkage: muy visual, ligado al turismo ← REDISEÑAR COMPLETAMENTE
**Tiempo estimado:** 10 min

**(Reservado)**



















**Nexttip:** "Ya entendemos cómo aprende el modelo. ¿Qué pasa cuando queremos hacer predicciones?"

---

### S8 — Clásico vs Bayesiano
**Tiempo estimado:** 5 min

**2 columnas + tabla comparativa:**

Frecuentista (borde rojo): θ fijo, IC = propiedad del procedimiento, sin mecanismo grupos nuevos

Bayesiano (borde verde): θ = variable aleatoria, `p(θ|Y) ∝ p(Y|θ) × p(θ)`, IC credible = prob directa, grupos nuevos = muestrear prior

Tabla comparativa (5 filas): ¿Qué es θ? / Resultado / Prior / IC / Grupos nuevos

**Nexttip:** "Con esta filosofía, los parámetros de grupo también son variables aleatorias — y por eso pueden tener priors que los conecten."

---

### S9 — Parametrización: qué es y por qué importa (SUMMER + guía)
**Tiempo estimado:** 6 min

Objetivo: instalar la idea de que *el mismo modelo* puede escribirse de varias formas y eso afecta la eficiencia de MCMC.

Modelo base (Normal-Normal, para explicar la idea):
- Datos: `y_ij | θ_j, σ_y ~ N(θ_j, σ²_y)`
- Grupos: `θ_j | μ, τ ~ N(μ, τ²)`

Slide: 2 tarjetas
- Izquierda: modelo base + definición de variables
- Derecha: “centrada vs no centrada” como dos escrituras del mismo nivel 2

**Nexttip:** "Veamos la versión centrada primero, desde la fórmula."

---

### S10 — Parametrización centrada (despiece de fórmula)
**Tiempo estimado:** 6 min

Mostrar y explicar partes:
- `y_ij | θ_j, σ_y ~ N(θ_j, σ²_y)`
- `θ_j | μ, τ ~ N(μ, τ²)`

Mensajes:
- Cuando hay mucha evidencia por grupo, centrada suele mezclar bien
- Cuando hay pocos datos o `τ → 0`, crece la dependencia y aparece el “funnel”

**Nexttip:** "Ahora reescribimos el mismo modelo en forma no centrada."

---

### S11 — Parametrización no centrada (despiece de fórmula)
**Tiempo estimado:** 6 min

Reescritura:
- `η_j ~ N(0,1)`
- `θ_j = μ + τ · η_j`
- `y_ij | θ_j, σ_y ~ N(θ_j, σ²_y)`

Mensajes:
- Separa “nivel” y “escala”
- Ayuda cuando hay pocos datos por grupo o cuando `τ` es pequeño

**Nexttip:** "¿Por qué cambia tanto? La intuición es Neal funnel."

---

### S12 — Neal funnel: intuición y regla de uso
**Tiempo estimado:** 5 min

Mensaje simple:
- Con `τ` pequeño, `θ_j` debe estar pegado a `μ` → cuello angosto (geometría difícil)
- No centrada reduce dependencia y facilita exploración

Regla práctica (en voz):
- pocos datos / señal débil → no centrada
- mucha información / señal fuerte → centrada
- si dudas: probar ambas y mirar diagnósticos

**Nexttip:** "Ok: ya muestreamos. Ahora lo verificamos."

---

### S13 — Diagnóstico: R-hat y ESS (SSE)
**Tiempo estimado:** 5 min

R-hat:
- Interpretación: entre cadenas vs dentro de cadenas
- Umbral típico: `R-hat < 1.01`

ESS (muestras efectivas; a veces escrito como “SSE” en apuntes):
- Interpretación: cuánta información independiente hay
- Señal de problema: ESS muy baja en parámetros clave

**Nexttip:** "Y el chequeo visual más importante: trazas."

---

### S14 — Diagnóstico: trazas (trace plots)
**Tiempo estimado:** 5 min

Objetivo: que la audiencia se lleve un criterio visual.

- Bien: ruido estable, cadenas mezclan y se cruzan, sin tendencias
- Mal: cadenas separadas, deriva, “pegajosidad”
- Acción: no interpretar resultados; ajustar warmup/priors o cambiar parametrización

Chart: `ch-trace` (ejemplo conceptual)

---

## Implementación técnica detallada

### Chart IDs y mapeo idx → initChart()

| idx | Slide | Chart IDs |
|-----|-------|-----------|
| 1 | S2 | `ch-scatter` |
| 2 | S3 | (SVGs inline únicamente) |
| 3 | S4 | `ch-pool-comp-1`, `ch-pool-comp-2`, `ch-pool-comp-3` |
| 4 | S5 | (SVG diagrama de placas) |
| 5 | S6 | (fórmulas y texto) |
| 6 | S7 | (reservado / en blanco por ahora) |
| 7 | S8 | (tabla HTML) |
| 8 | S9 | (fórmulas + explicación) |
| 9 | S10 | (fórmulas + explicación) |
| 10 | S11 | (fórmulas + explicación) |
| 11 | S12 | (texto + regla práctica) |
| 12 | S13 | (texto + umbrales) |
| 13 | S14 | `ch-trace` |

### Datos sintéticos (JavaScript)
```javascript
const daysCtg = [3,5,4,6,7], gastoCtg = [520,680,590,760,850]; // α≈280, β≈80
const daysMed = [2,4,3,5,6], gastoMed = [380,560,440,680,780]; // α≈180, β≈100
const daysBog = [1,3,5,7,4], gastoBog = [320,500,680,860,590]; // α≈230, β≈90
const muAlpha=230, muBeta=90, sigY=120, sigA=60;
const lam = n => (n/sigY**2)/((n/sigY**2)+(1/sigA**2));
```

### SVGs inline
- **S3:** Tres mini-SVGs (pool, no-pool, partial): 15 puntos + línea(s) de regresión
- **S5:** Diagrama de placas: `<rect>` dashed + `<circle>` nodos + `<line>` flechas
- **S7:** (reservado / en blanco por ahora)
- **S11:** Embudo (izq.) y esfera (der.) como SVGs

### CSS adicional
```css
.node{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;font-family:'JetBrains Mono',monospace;}
.node-obs{background:rgba(52,211,153,.18);border:2px solid rgba(52,211,153,.65);}
.node-lat{background:rgba(90,140,255,.1);border:2px solid rgba(90,140,255,.5);}
.node-hyp{background:rgba(160,80,255,.08);border:2px solid rgba(160,80,255,.4);}
.plate{border:2px dashed rgba(90,130,210,.3);border-radius:12px;padding:18px;position:relative;}
.plate-label{position:absolute;bottom:6px;right:10px;font-size:.58rem;color:rgba(90,130,210,.42);text-transform:uppercase;}
```

### Anotaciones en fórmulas (S11)
HTML con posición relativa + spans coloridos + flechitas CSS para cada parte. No depender de MathJax para las anotaciones de desglose.

---

## Verificación

1. Abrir `presentacion.html` en Chrome → counter muestra `1 / 13`, 13 dots en el nav
2. Navegar todas las slides con flechas → ninguna slide vacía o rota
3. Charts renderizan solo al llegar a la slide (lazy via `initChart(idx)`)
4. MathJax renderiza fórmulas al navegar (via `MathJax.typesetPromise`)
5. Click en chart → modal fullscreen abre; Escape y click exterior lo cierran
6. `grep -c 'class="slide"' presentacion.html` debe retornar exactamente 13
7. SVGs inline visibles y bien proporcionados en pantalla completa
