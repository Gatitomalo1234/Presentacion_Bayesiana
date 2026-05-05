# Modelos Jerárquicos Bayesianos — Presentación

**Curso:** Estadística Bayesiana · Semestre 4, 2026  
**Universidad:** Externado de Colombia · Ciencia de Datos  
**Equipo:** Nicolás Cárdenas Díaz · Miguel Ángel Camargo Mora · Brayan Camilo Hernández Silva  
**Fuente teórica:** *Bayes Rules!* — Johnson, Ott & Dogucu (2022), capítulos 15, 16 y 17

---

## ¿Qué estamos haciendo?

Creamos una presentación de ~1:30 h que explica **modelos jerárquicos bayesianos desde cero** para una audiencia de compañeros de clase con conocimiento estadístico similar. El objetivo es explicar un tema difícil con palabras sencillas y exactas, usando dos ejemplos concretos del libro:

- **Spotify** (cap. 16): popularidad de canciones agrupadas por artista — ejemplo sin predictores
- **Running** (cap. 17): tiempo de carrera vs. edad, agrupado por corredor — ejemplo con predictores

La presentación es completamente autocontenida (un solo archivo HTML) y viene acompañada de un cuaderno Python con todos los modelos ejecutables. Los dos archivos son independientes entre sí — el notebook no exporta figuras al HTML.

---

## Archivos del proyecto

```
PRESENTACION BAYESIANA/
├── presentacion.html     ← Slides interactivas (abrir en el navegador)
├── analisis.ipynb        ← Notebook Python con los modelos en PyMC
├── README.md             ← Este archivo
└── NOTAS_LIBRO.md        ← Resumen detallado de los capítulos 15, 16 y 17
```

---

## `presentacion.html`

**Cómo abrirlo:** doble clic → se abre en cualquier navegador. No necesita internet después de la primera carga (MathJax se carga desde CDN la primera vez).

**Diseño:** fondo oscuro (#080c12) con grid animado de 44px y partículas flotantes con líneas de conexión (Canvas API). Texto en blanco sobre fondo oscuro. Fórmulas LaTeX renderizadas con MathJax. Gráficos interactivos con Chart.js (inicialización lazy por slide). Iconos Lucide con stroke-width 1.5.

**Sistema de componentes CSS:**

| Clase | Uso |
|-------|-----|
| `.def-block` | Definiciones formales con borde azul izquierdo |
| `.thm` | Bloques de fórmulas / teoremas |
| `.ex-tag` | Chip verde que marca mini-ejemplos (Spotify / Running) |
| `.callout` | Notas interpretativas (variantes: `.ok`, `.warn`) |
| `.card` | Tarjeta glass con hover sutil |
| `.stag` | Etiqueta de sección en la esquina superior |
| `.badge` | Badges de color (`.badge-b`, `.badge-g`, `.badge-r`, `.badge-y`) |

**Navegación:**
- Flechas `←` `→` del teclado (también `↑`/`↓` y espacio)
- Botones en pantalla
- Clic en los puntos de progreso (parte inferior)
- Swipe táctil en móvil/tablet

**Estructura de las 11 slides:**

| # | ID | Título | Contenido principal |
|---|----|--------|---------------------|
| 1 | s1 | Portada | Título, subtítulo, nombres del equipo |
| 2 | s2 | Intercambiabilidad parcial | Definición formal, teorema de De Finetti, problema en datos agrupados |
| 3 | s3 | Tres estrategias de pooling | Complete / No / Partial Pooling — fórmulas + gráfico comparativo |
| 4 | s4 | Especificación del modelo jerárquico | Niveles 1-2-3, posterior conjunta, tabla de parámetros, descomposición de varianza |
| 5 | s5 | Shrinkage bayesiano | Estimador posterior λⱼ, ICC ρ, gráfico λⱼ vs nⱼ, shrinkage plot Spotify |
| 6 | s6 | Diagnósticos MCMC | R̂ (Gelman-Rubin), PPC, p-valor bayesiano, trace plot, densidad Y_obs vs Y_rep |
| 7 | s7 | Regresión jerárquica | Pooled / Random Intercepts / Random Slopes — fórmulas + líneas de regresión |
| 8 | s8 | Estructura de covarianza | Matriz Σ, prior LKJ, elipse de confianza bivariada, posterior de ρ |
| 9 | s9 | Predicción bayesiana | Grupo conocido vs. nuevo — integrales predictivas, distribuciones superpuestas |
| 10 | s10 | LOO-CV | ELPD, PSIS-LOO, tabla de comparación, gráfico de barras horizontales |
| 11 | s11 | Resumen | Radar chart multidimensional, criterios de uso, 3 propiedades clave |

**Gráficos interactivos por slide:**

| Slide | Canvas ID | Tipo | Contenido |
|-------|-----------|------|-----------|
| s2 | `ch-interch` | scatter | Popularidad por artista — 7 grupos de colores |
| s3 | `ch-3models` | bar+line | Estimaciones μⱼ: pooling / no pooling / jerárquico |
| s4 | `ch-vardecomp` | doughnut | σμ² vs σy² (38% / 62%) |
| s5 | `ch-lambda` | line | λⱼ en función de nⱼ (curva cóncava) |
| s5 | `ch-shrink` | bar | Shrinkage no-pooling vs. jerárquico — 12 artistas |
| s6 | `ch-trace` | line | Trace plot — 3 cadenas, μ global |
| s6 | `ch-ppc` | line | Densidades Y_obs vs 2 réplicas Y_rep |
| s7 | `ch-reglines` | line | 14 líneas por modelo superpuestas |
| s8 | `ch-rhopost` | line | Posterior de ρ ~ N(-0.25, 0.18) |
| s9 | `ch-pred` | line | Distribuciones predictivas: corredor conocido (σ=5) vs nuevo (σ=14.5) |
| s10 | `ch-loo` | bar horizontal | ELPD_LOO: Pooled=-820, RI=-745, RS=-735 |
| s11 | `ch-radar` | radar | 5 dimensiones: Simplicidad, Flexibilidad, Grupos pequeños, Pred. nuevos, Calibración |

---

## `analisis.ipynb`

**Cómo ejecutarlo:**

```bash
pip install pymc arviz pandas numpy matplotlib scipy
jupyter notebook analisis.ipynb
```

Usar "Run All" para ejecutar todas las celdas en orden. El notebook genera datos sintéticos internamente — no se necesitan archivos externos. No exporta figuras a la presentación (son archivos independientes).

**Advertencia de tiempo:** Los modelos PyMC con MCMC toman entre 2 y 8 minutos cada uno dependiendo del hardware. En total, ejecutar el notebook completo toma ~20–30 minutos la primera vez.

**Estructura del notebook:**

### Parte 1 — Spotify (Capítulo 16)

| Celda | Contenido |
|-------|-----------|
| Setup | Imports, semilla aleatoria, estilo visual |
| Datos | 44 artistas, ~350 canciones sintéticas, popularidad 0–100 |
| Exploración | Histograma global + medias por artista |
| Modelo 1 | Complete Pooling en PyMC — un solo μ para todos |
| Modelo 2 | No Pooling en PyMC — μⱼ independientes |
| Modelo 3 | Jerárquico en PyMC — μⱼ ~ N(μ, σ²_μ) |
| Diagnósticos | R̂, ESS, trace plots de hiperparámetros |
| Shrinkage plot | Visualización de cómo las estimaciones se contraen hacia la media global |
| Correlación ρ | Distribución posterior de σ²_μ / (σ²_μ + σ²_y) |

### Parte 2 — Running (Capítulo 17)

| Celda | Contenido |
|-------|-----------|
| Datos | 36 corredores, 252 obs, edad vs. tiempo neto |
| Exploración | Scatter edad-tiempo coloreado por corredor |
| Modelo A | Pooled Regression — una sola recta |
| Modelo B | Random Intercepts — intercept por corredor, pendiente global |
| Modelo C | Random Intercepts + Slopes — intercepto y pendiente por corredor |
| Comparación | LOO-CV con ArviZ, tabla de ELPD por modelo |
| Predicción | Distribuciones de predicción: corredor conocido vs. nuevo |

---

## Dependencias

**HTML:** solo necesita un navegador moderno (Chrome, Firefox, Safari, Edge). Librerías cargadas desde CDN:

| Librería | CDN | Uso |
|----------|-----|-----|
| Tailwind CSS | cdn.tailwindcss.com | Utilidades de estilo |
| Chart.js 4.4.0 | jsdelivr | Gráficos interactivos |
| Lucide | unpkg | Iconos (stroke-width 1.5) |
| MathJax 3 | jsdelivr | Renderizado LaTeX |

**Python:**

| Librería | Versión recomendada | Uso |
|----------|---------------------|-----|
| pymc | ≥ 5.0 | Modelos bayesianos con MCMC |
| arviz | ≥ 0.17 | Diagnósticos y LOO-CV |
| numpy | ≥ 1.24 | Álgebra y generación de datos |
| pandas | ≥ 2.0 | Manejo de datos |
| matplotlib | ≥ 3.7 | Visualizaciones |
| scipy | ≥ 1.10 | Estadísticas auxiliares |

---

## Flujo conceptual de la presentación

```
Intercambiabilidad         Tres enfoques          Modelo formal
(Slide 2)          →       (Slide 3)       →      (Slide 4–5)
                                                        ↓
Resumen                    LOO-CV                 Con predictores
(Slide 11)         ←       (Slide 10)      ←      (Slides 7–9)
                                                        ↑
                                             Diagnósticos (Slide 6)
```

---

## Historial de cambios relevantes

| Fecha | Cambio |
|-------|--------|
| 2026-05-02 | Creación inicial — diseño con blobs gradient animados (CSS) |
| 2026-05-02 | Rediseño — fondo Canvas API (grid 44px + partículas), contenido más técnico |
| 2026-05-02 | Portada: eliminadas referencias al libro y a los capítulos, solo título y nombres |
| 2026-05-02 | Bugs corregidos: `</div>` → `</h2>` en slide 3, paréntesis extra en tooltip LOO |
| 2026-05-02 | Section tags: eliminados prefijos "Cap. 15/16/17 ·", reemplazados por temas descriptivos |
