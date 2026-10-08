"""Medicion del tiempo de subarreglo_fuerza_bruta y subarreglo_maximo."""
import os
import random
import time
from typing import Callable

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo

SEMILLA = 42
TAMANOS = [10, 50, 100, 500, 1000, 2000, 4000, 8000, 16000]
CARPETA_GRAFICAS = os.path.join(os.path.dirname(__file__), "graficas")


def generar_datos(tamano: int, generador: random.Random) -> list[int]:
    """Genera una serie de variaciones enteras entre -100 y 100.

    Args:
        tamano: cantidad de dias de la serie.
        generador: generador aleatorio con semilla fija.

    Returns:
        Lista de `tamano` enteros en el rango [-100, 100].
    """
    return [generador.randint(-100, 100) for _ in range(tamano)]


def repeticiones(tamano: int) -> int:
    """Define cuantas veces se repite la medicion segun el tamaño.

    Args:
        tamaño: tamaño de la entrada.

    Returns:
        Numero de repeticiones: mas para entradas pequeñas.
    """
    if tamano <= 1000:
        return 5
    if tamano <= 4000:
        return 3
    return 1


def cronometrar(
    algoritmo: Callable[[], tuple[int, int, float]], reps: int
) -> tuple[float, float]:
    """Mide el tiempo de una llamada al algoritmo.

    Args:
        algoritmo: funcion sin argumentos que ejecuta el algoritmo.
        reps: numero de repeticiones de la medicion.

    Returns:
        Una tupla (mejor_tiempo, suma): el menor tiempo observado en
        segundos y la suma maxima que devolvio el algoritmo.
    """
    mejor_tiempo = float("inf")
    suma = 0.0
    for _ in range(reps):
        inicio = time.perf_counter()
        resultado = algoritmo()
        tiempo = time.perf_counter() - inicio
        if tiempo < mejor_tiempo:
            mejor_tiempo = tiempo
        suma = resultado[2]
    return mejor_tiempo, suma


def ejecutar_experimento(
    tamanos: list[int], semilla: int
) -> tuple[list[float], list[float]]:
    """Mide ambos algoritmos para cada tamaño con la misma lista.

    Args:
        tamanos: tamaños de entrada a medir.
        semilla: semilla del generador de datos.

    Returns:
        Una tupla (tiempos_fuerza_bruta, tiempos_divide_venceras), ambas
        listas en segundos y en el mismo orden que `tamanos`.
    """
    generador = random.Random(semilla)
    tiempos_fb: list[float] = []
    tiempos_dv: list[float] = []

    for tamano in tamanos:
        valores = generar_datos(tamano, generador)
        reps = repeticiones(tamano)

        tiempo_fb, suma_fb = cronometrar(
            lambda: subarreglo_fuerza_bruta(valores), reps
        )
        tiempo_dv, suma_dv = cronometrar(
            lambda: subarreglo_maximo(valores, 0, tamano - 1), reps
        )

        assert suma_fb == suma_dv, (
            f"Sumas distintas para n={tamano}: {suma_fb} != {suma_dv}"
        )
        tiempos_fb.append(tiempo_fb)
        tiempos_dv.append(tiempo_dv)

    return tiempos_fb, tiempos_dv


def graficar(
    tamanos: list[int],
    tiempos_fb: list[float],
    tiempos_dv: list[float],
    ruta: str,
    escala_log: bool = False,
) -> None:
    """Grafica tiempo vs. tamano de entrada y la guarda como imagen.

    Args:
        tamanos: tamaños de entrada medidos.
        tiempos_fb: tiempos de fuerza bruta, en segundos.
        tiempos_dv: tiempos de divide y venceras, en segundos.
        ruta: ruta del archivo PNG de salida.
        escala_log: si es True, usa escala logaritmica en ambos ejes.
    """
    ms_fb = [t * 1000 for t in tiempos_fb]
    ms_dv = [t * 1000 for t in tiempos_dv]

    plt.figure(figsize=(9, 5.5))
    plt.plot(tamanos, ms_fb, marker="o", label="Fuerza bruta")
    plt.plot(tamanos, ms_dv, marker="s", label="Divide y venceras")

    if escala_log:
        plt.xscale("log")
        plt.yscale("log")
        titulo = "Tiempo de ejecucion vs. tamano de entrada (escala log-log)"
    else:
        titulo = "Tiempo de ejecucion vs. tamano de entrada"

    plt.title(titulo)
    plt.xlabel("Tamano de entrada n (numero de dias)")
    plt.ylabel("Tiempo de ejecucion (milisegundos)")
    plt.grid(True, which="both", alpha=0.3)
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=12, prune=None))
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()


def imprimir_tabla(
    tamanos: list[int], tiempos_fb: list[float], tiempos_dv: list[float]
) -> None:
    """Imprime los tiempos medidos y cuanto crecio cada uno entre tamaños.

    Args:
        tamanos: tamaños de entrada medidos.
        tiempos_fb: tiempos de fuerza bruta, en segundos.
        tiempos_dv: tiempos de divide y venceras, en segundos.
    """
    print(
        f"{'n':>7} {'FB (ms)':>12} {'DV (ms)':>12} {'FB/DV':>8} "
        f"{'x n':>6} {'x FB':>8} {'x DV':>8}"
    )
    for k, tamano in enumerate(tamanos):
        fb_ms = tiempos_fb[k] * 1000
        dv_ms = tiempos_dv[k] * 1000
        if k == 0:
            crecimiento = f"{'-':>6} {'-':>8} {'-':>8}"
        else:
            crecimiento = (
                f"{tamano / tamanos[k - 1]:>6.1f} "
                f"{tiempos_fb[k] / tiempos_fb[k - 1]:>8.1f} "
                f"{tiempos_dv[k] / tiempos_dv[k - 1]:>8.1f}"
            )
        print(
            f"{tamano:>7} {fb_ms:>12.4f} {dv_ms:>12.4f} "
            f"{fb_ms / dv_ms:>8.2f} {crecimiento}"
        )


def main() -> None:
    """Ejecuta el experimento, imprime la tabla y guarda las graficas."""
    tiempos_fb, tiempos_dv = ejecutar_experimento(TAMANOS, SEMILLA)
    imprimir_tabla(TAMANOS, tiempos_fb, tiempos_dv)

    os.makedirs(CARPETA_GRAFICAS, exist_ok=True)
    graficar(
        TAMANOS,
        tiempos_fb,
        tiempos_dv,
        os.path.join(CARPETA_GRAFICAS, "tiempo_vs_n.png"),
    )
    print(f"Graficas guardadas en '{CARPETA_GRAFICAS}/'.")


if __name__ == "__main__":
    main()