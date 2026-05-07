# Modelos Jerárquicos Bayesianos — Presentación

**Curso:** Estadística Bayesiana · Semestre 4, 2026  
**Universidad:** Externado de Colombia · Ciencia de Datos  
**Equipo:** Nicolás Cárdenas Díaz · Miguel Ángel Camargo Mora · Brayan Camilo Hernández Silva

---

## ¿Qué contiene este proyecto?

Este repo contiene una presentación autocontenida sobre **modelos jerárquicos bayesianos**. La versión actual de `presentacion.html` implementa la reestructuración descrita en `PLAN_PRESENTACION.md`, con slides conceptuales recuperadas/adaptadas del backup para abrir la explicación relacional y motivar por qué necesitamos jerarquías. La narrativa actual tiene 14 slides y usa un ejemplo de **turismo colombiano** inspirado en `SUMMER .pdf`.

La idea central de la presentación es:

> ¿Cómo aprendemos de un grupo sin ignorar lo que los demás grupos nos dicen sobre él?

El ejemplo base usa 15 turistas en 3 ciudades:

- Cartagena
- Medellín
- Bogotá

Cada observación tiene:

- días de estadía (`days`)
- gasto total en USD (`Y_ij`)
- ciudad/grupo (`j`)

---

## Archivos principales

```text
PRESENTACION BAYESIANA/
├── presentacion.html
├── analisis.ipynb
├── PLAN_PRESENTACION.md
├── estructura_presentacion.md
├── presentacion_backup_tecnica.html
├── Apoyos bibliograficos/
│   ├── SUMMER .pdf
│   ├── RESUMEN_SUMMER.md
│   ├── NOTAS_LIBRO.md
│   └── guia_modelos_jerarquicos_detallada.md
└── README.md
```

### `presentacion.html`

Presentación final interactiva. Se abre directamente en el navegador con doble clic.

Usa:

- Tailwind CSS desde CDN
- Chart.js 4.4.0 desde CDN
- Lucide Icons desde CDN
- MathJax 3 desde CDN
- Google Fonts

Necesita internet para cargar esas librerías si no están cacheadas.

### `PLAN_PRESENTACION.md`

Fuente de verdad de la reestructuración actual. Define la narrativa, los datos sintéticos, los charts esperados y las verificaciones.

### `analisis.ipynb`

Notebook Python independiente con modelos PyMC basados en los ejemplos Spotify y Running de *Bayes Rules!* capítulos 15, 16 y 17. No exporta figuras al HTML.

### `Apoyos bibliograficos/`

Material teórico y de apoyo:

- `SUMMER .pdf`: referencia metodológica para el ejemplo de turismo.
- `RESUMEN_SUMMER.md`: resumen operativo del PDF para guiar narrativa y diseño.
- `NOTAS_LIBRO.md`: resumen de *Bayes Rules!* caps. 15-17.
- `guia_modelos_jerarquicos_detallada.md`: guía conceptual general.

---

## Estructura de la presentación

La presentación actual tiene exactamente **14 slides**:

| # | Tema | Elemento principal |
|---|------|--------------------|
| 1 | Portada | Título y equipo |
| 2 | Modelo relacional | Individuo → grupo → población |
| 3 | ¿Por qué jerarquías? | Mundo anidado + préstamo de información |
| 4 | Datos agrupados | Turismo colombiano + scatter plot |
| 5 | Esquema general | Turismo + ejemplo paralelo de Spotify |
| 6 | Modelo SUMMER | Regresión lineal jerárquica de turismo |
| 7 | Modelo Normal-Normal | Proceso generativo + Bayes |
| 8 | Shrinkage | Fórmula, lambda e interceptos encogidos |
| 9 | Clásico vs Bayesiano | Comparación filosófica |
| 10 | Regresión jerárquica | Pooled, random intercepts, random slopes |
| 11 | Predicción | Ciudad conocida vs ciudad nueva |
| 12 | Parametrización | Centrada vs no centrada |
| 13 | LOO-CV | Comparación por ELPD_LOO |
| 14 | Resumen | Radar chart y criterios de uso |

---

## Navegación

En `presentacion.html` se puede navegar con:

- Flechas izquierda/derecha
- Flechas arriba/abajo
- Barra espaciadora
- Botones de navegación
- Puntos inferiores
- Swipe en móvil/tablet

Los gráficos Chart.js se inicializan de forma lazy al llegar a cada slide. Al hacer clic sobre un gráfico se abre en modal fullscreen; `Escape` o clic por fuera lo cierra.

---

## Datos sintéticos del ejemplo de turismo

```javascript
Cartagena: days = [3,5,4,6,7], gasto = [520,680,590,760,850]
Medellín:  days = [2,4,3,5,6], gasto = [380,560,440,680,780]
Bogotá:    days = [1,3,5,7,4], gasto = [320,500,680,860,590]
```

Parámetros conceptuales usados en la narrativa:

- Cartagena: `alpha ≈ 280`, `beta ≈ 80`
- Medellín: `alpha ≈ 180`, `beta ≈ 100`
- Bogotá: `alpha ≈ 230`, `beta ≈ 90`
- Media global: `mu_alpha ≈ 230`, `mu_beta ≈ 90`

---

## Ejecutar el notebook

El notebook no es necesario para abrir la presentación. Si quieres correr los modelos PyMC:

```bash
pip install pymc arviz pandas numpy matplotlib scipy
jupyter notebook analisis.ipynb
```

El notebook genera datos sintéticos internamente. Ejecutarlo completo puede tomar varios minutos porque ajusta modelos MCMC.

---

## Verificación rápida

Comandos útiles:

```bash
rg -o 'class="slide' presentacion.html | wc -l
node --check /private/tmp/presentacion_scripts.js
```

El primer comando debe retornar `14`. Para el segundo, primero se puede extraer el JavaScript embebido:

```bash
perl -0777 -ne 'while(/<script>(.*?)<\/script>/gs){print $1,"\n"}' presentacion.html > /private/tmp/presentacion_scripts.js
```

---

## Estado actual

- `presentacion.html` implementa una narrativa de 14 slides con mapa general y modelo lineal jerárquico de SUMMER.
- `README.md` está alineado con la nueva narrativa.
- `presentacion_backup_tecnica.html` conserva una versión técnica previa.
- `analisis.ipynb` se mantiene como apoyo ejecutable independiente basado en Spotify/Running.
