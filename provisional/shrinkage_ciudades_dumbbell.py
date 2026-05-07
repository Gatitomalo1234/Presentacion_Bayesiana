#!/usr/bin/env python3
"""
Shrinkage (Partial Pooling) en el ejemplo de ciudades (turismo).

Genera datos sintéticos para varias ciudades (incluye Cartagena/Medellin/Bogota),
con tamaños de muestra desbalanceados, calcula:
  - Media Observada (sin shrinkage): ybar_j
  - Estimación Jerárquica (con shrinkage): muhat_j
y grafica un dumbbell plot mostrando el encogimiento hacia la Media Global.

Uso:
  python3 shrinkage_ciudades_dumbbell.py
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

# Headless-safe backend + writable cache dir (fixes issues in restricted envs).
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def simulate_city_data(seed: int = 7) -> tuple[pd.DataFrame, float]:
    rng = np.random.default_rng(seed)

    # Ciudades (reusa el ejemplo base y agrega otras para tener contraste de n)
    cities = [
        "Cartagena",
        "Medellin",
        "Bogota",
        "Cali",
        "Barranquilla",
        "Santa Marta",
        "Bucaramanga",
        "Pereira",
        "Manizales",
        "Armenia",
    ]

    # Media global "pais" (USD) y variacion entre ciudades / dentro de ciudad
    mu0 = 520.0
    sigma_mu = 120.0   # variacion entre ciudades (poblacion)
    sigma_y = 220.0    # ruido turista-a-turista

    # Tamaños de muestra desbalanceados: algunos con n grande, otros con n chico
    n_by_city = {
        "Cartagena": 28,
        "Medellin": 22,
        "Bogota": 30,
        "Cali": 3,
        "Barranquilla": 5,
        "Santa Marta": 2,
        "Bucaramanga": 8,
        "Pereira": 4,
        "Manizales": 12,
        "Armenia": 2,
    }

    # "Verdad" por ciudad
    mu_true = {c: float(rng.normal(mu0, sigma_mu)) for c in cities}

    rows = []
    for c in cities:
        n = int(n_by_city[c])
        y = rng.normal(mu_true[c], sigma_y, size=n)
        for yi in y:
            rows.append({"Ciudad": c, "Gasto": float(yi)})

    df = pd.DataFrame(rows)
    return df, mu0


def compute_shrinkage_estimates(df: pd.DataFrame, mu0: float) -> pd.DataFrame:
    """
    Estimación jerárquica estilo Normal-Normal (ilustrativa):
      muhat_j = lam_j * ybar_j + (1-lam_j) * mu0
    donde lam_j crece con n_j, haciendo shrinkage mas fuerte cuando n_j es pequeño.

    Nota: Para la visualización no necesitamos inferencia completa; solo el patrón de encogimiento.
    """
    g = (
        df.groupby("Ciudad", as_index=False)
        .agg(n=("Gasto", "size"), ybar=("Gasto", "mean"), s=("Gasto", "std"))
    )

    # Parametros "fijos" para la demostracion (pueden ajustarse)
    sigma_mu = 120.0
    sigma_y = 220.0

    n = g["n"].to_numpy(dtype=float)
    lam = (n * (sigma_mu**2)) / (n * (sigma_mu**2) + (sigma_y**2))
    g["lambda"] = lam
    g["Media Observada"] = g["ybar"]
    g["Estimacion Jerarquica"] = lam * g["ybar"] + (1.0 - lam) * mu0
    return g


def dumbbell_plot(est: pd.DataFrame, mu0: float, outpath: str = "shrinkage_ciudades_dumbbell.png") -> None:
    sns.set_theme(style="whitegrid", context="talk")

    # Orden: mas shrinkage arriba (n menor)
    est = est.sort_values(["n", "Media Observada"], ascending=[True, False]).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12.5, 7.5))

    y = np.arange(len(est))
    x_obs = est["Media Observada"].to_numpy()
    x_h = est["Estimacion Jerarquica"].to_numpy()

    # Segmentos (encogimiento)
    for yi, xo, xh in zip(y, x_obs, x_h):
        ax.plot([xo, xh], [yi, yi], color="#94a3b8", lw=3, alpha=0.65, zorder=1)
        # flecha sutil hacia la estimacion jerarquica
        ax.annotate(
            "",
            xy=(xh, yi),
            xytext=(xo, yi),
            arrowprops=dict(arrowstyle="-|>", color="#94a3b8", lw=2, alpha=0.55),
            zorder=2,
        )

    # Puntos
    ax.scatter(x_obs, y, s=120, color="#34d399", edgecolor="white", linewidth=1.2, zorder=3, label="Media Observada")
    ax.scatter(x_h, y, s=120, color="#fb923c", edgecolor="white", linewidth=1.2, zorder=4, label="Estimación Jerárquica")

    # Media global
    ax.axvline(mu0, color="#a855f7", lw=2.5, alpha=0.85, linestyle="--", label="Media Global (mu0)")

    # Etiquetas de ciudades + n
    labels = [f"{c}  (n={n})" for c, n in zip(est["Ciudad"], est["n"])]
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    ax.set_xlabel("Gasto promedio (USD)")
    ax.set_ylabel("Ciudad")
    ax.set_title("Shrinkage (Partial Pooling): Ciudades con menos datos se acercan más a la media global")

    # Mejorar límites
    xmin = min(x_obs.min(), x_h.min(), mu0) - 80
    xmax = max(x_obs.max(), x_h.max(), mu0) + 80
    ax.set_xlim(xmin, xmax)

    # Leyenda
    ax.legend(loc="lower right", frameon=True, framealpha=0.9)

    # Nota breve: "por qué"
    ax.text(
        0.01,
        1.02,
        "Lectura: las ciudades con n pequeño muestran mayor 'encogimiento' (segmento más largo).",
        transform=ax.transAxes,
        fontsize=12,
        color="#cbd5e1",
    )

    sns.despine(ax=ax, left=False, bottom=False)
    fig.tight_layout()
    fig.savefig(outpath, dpi=180, bbox_inches="tight")
    print(f"Guardado: {outpath}")


def main() -> None:
    df, mu0 = simulate_city_data(seed=7)
    est = compute_shrinkage_estimates(df, mu0=mu0)
    dumbbell_plot(est, mu0=mu0)


if __name__ == "__main__":
    main()
