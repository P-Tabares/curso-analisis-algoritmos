"""Medicion del tiempo de busqueda en ListaEnlazada y TablaHash."""
import gc
import os
import random
import time

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from estructuras import ListaEnlazada, TablaHash

SEMILLA_DATOS = 42
SEMILLA_INEXISTENTES = 7
CANTIDAD_BUSQUEDAS = 200
MUESTRA_VERIFICACION = 50

TAMANOS_EXP_A = [100, 500, 1000, 5000, 10000, 20000, 50000]
N_FIJO_EXP_B = 20000
ALFAS_OBJETIVO_EXP_B = [0.25, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0]

ESTADOS = ("en bodega", "en reparto", "entregado", "en transito")
CARPETA_GRAFICAS = os.path.join(os.path.dirname(__file__), "graficas")


def es_primo(numero: int) -> bool:
    """Determina si un entero positivo es primo.

    Args:
        numero: entero a evaluar.

    Returns:
        True si `numero` es primo, False en caso contrario.
    """
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False
    limite = int(numero**0.5) + 1
    for divisor in range(3, limite, 2):
        if numero % divisor == 0:
            return False
    return True


def primo_cercano(objetivo: int) -> int:
    """Encuentra el numero primo mas cercano a un entero objetivo.

    Args:
        objetivo: valor entero de referencia (al menos 2).

    Returns:
        El numero primo mas proximo a `objetivo`.
    """
    candidato = max(2, objetivo)
    if es_primo(candidato):
        return candidato
    distancia = 1
    while True:
        if candidato - distancia >= 2 and es_primo(candidato - distancia):
            return candidato - distancia
        if es_primo(candidato + distancia):
            return candidato + distancia
        distancia += 1


def generar_envios(
    cantidad: int, semilla: int = SEMILLA_DATOS
) -> tuple[list[tuple[int, str]], set[int]]:
    """Genera pares (guia, estado) con guias unicas de diez digitos.

    Args:
        cantidad: numero de envios a generar.
        semilla: semilla del generador aleatorio para reproducibilidad.

    Returns:
        Una tupla (envios, conjunto_guias) con la lista de pares
        (guia, estado) y el conjunto de guias generadas.
    """
    azar = random.Random(semilla)
    envios: list[tuple[int, str]] = []
    existentes: set[int] = set()
    while len(envios) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            existentes.add(guia)
            estado = azar.choice(ESTADOS)
            envios.append((guia, estado))
    return envios, existentes


def generar_guias_inexistentes(
    existentes: set[int], cantidad: int, semilla: int = 7
) -> list[int]:
    """Genera guias de diez digitos que no estan en la coleccion.

    Args:
        existentes: guias almacenadas en las estructuras.
        cantidad: cuantas guias inexistentes generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con `cantidad` guias que no pertenecen a `existentes`.
    """
    azar = random.Random(semilla)
    inexistentes: list[int] = []
    while len(inexistentes) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            inexistentes.append(guia)
    return inexistentes


def medir_busquedas_lista(
    lista: ListaEnlazada, guias: list[int], repeticiones: int = 1
) -> float:
    """Mide el tiempo medio por busqueda en una ListaEnlazada.

    Args:
        lista: lista enlazada donde se realizan las busquedas.
        guias: lista de guias a buscar.
        repeticiones: cuantas veces repetir el lote para estabilizar.

    Returns:
        El menor tiempo medio por busqueda observado, en segundos.
    """
    mejor_lote = float("inf")
    gc_estaba_activo = gc.isenabled()
    gc.disable()
    try:
        for _ in range(repeticiones):
            inicio = time.perf_counter()
            for guia in guias:
                lista.buscar(guia)
            duracion = time.perf_counter() - inicio
            if duracion < mejor_lote:
                mejor_lote = duracion
    finally:
        if gc_estaba_activo:
            gc.enable()
    return mejor_lote / len(guias)


def medir_busquedas_tabla(
    tabla: TablaHash, guias: list[int], repeticiones: int = 100
) -> float:
    """Mide el tiempo medio por busqueda en una TablaHash.

    Args:
        tabla: tabla hash donde se realizan las busquedas.
        guias: lista de guias a buscar.
        repeticiones: cuantas veces repetir el lote para estabilizar.

    Returns:
        El menor tiempo medio por busqueda observado, en segundos.
    """
    mejor_lote = float("inf")
    gc_estaba_activo = gc.isenabled()
    gc.disable()
    try:
        for _ in range(repeticiones):
            inicio = time.perf_counter()
            for guia in guias:
                tabla.buscar(guia)
            duracion = time.perf_counter() - inicio
            if duracion < mejor_lote:
                mejor_lote = duracion
    finally:
        if gc_estaba_activo:
            gc.enable()
    return mejor_lote / len(guias)


def ejecutar_experimento_a(
    tamanos: list[int],
) -> tuple[list[int], list[float], list[float], list[float]]:
    """Ejecuta el Experimento A: ListaEnlazada vs. TablaHash segun n.

    Args:
        tamanos: lista de valores de n (numero de guias) a evaluar.

    Returns:
        Una tupla (casillas_m, alfas, tiempos_lista, tiempos_tabla) con el
        numero de casillas m, el factor de carga y los tiempos medios por
        busqueda en segundos para cada valor de n.
    """
    casillas_m: list[int] = []
    alfas: list[float] = []
    tiempos_lista: list[float] = []
    tiempos_tabla: list[float] = []

    max_n = max(tamanos)
    todos_envios, _ = generar_envios(max_n, SEMILLA_DATOS)

    for n in tamanos:
        envios = todos_envios[:n]
        existentes = {guia for guia, _ in envios}
        inexistentes = generar_guias_inexistentes(
            existentes, CANTIDAD_BUSQUEDAS, SEMILLA_INEXISTENTES
        )

        m = primo_cercano(max(2, n // 2))
        lista = ListaEnlazada()
        tabla = TablaHash(m)

        for guia, estado in envios:
            lista.insertar(guia, estado)
            tabla.insertar(guia, estado)

        # Verificar que ambas estructuras devuelven el mismo estado
        # para una muestra de guias existentes e inexistentes.
        paso = max(1, n // MUESTRA_VERIFICACION)
        for guia, estado_esperado in envios[::paso]:
            estado_lista = lista.buscar(guia)
            estado_tabla = tabla.buscar(guia)
            assert estado_lista == estado_esperado
            assert estado_lista == estado_tabla

        for guia_no_existe in inexistentes[:10]:
            assert lista.buscar(guia_no_existe) is None
            assert tabla.buscar(guia_no_existe) is None

        reps_lista = 5 if n <= 1000 else (3 if n <= 10000 else 1)
        t_lista = medir_busquedas_lista(lista, inexistentes, reps_lista)
        t_tabla = medir_busquedas_tabla(tabla, inexistentes, 100)

        casillas_m.append(m)
        alfas.append(tabla.factor_carga())
        tiempos_lista.append(t_lista)
        tiempos_tabla.append(t_tabla)

        del lista
        del tabla
        gc.collect()

    return casillas_m, alfas, tiempos_lista, tiempos_tabla


def ejecutar_experimento_b(
    n_fijo: int, alfas_objetivo: list[float]
) -> tuple[list[int], list[float], list[float]]:
    """Ejecuta el Experimento B: tiempo de busqueda en TablaHash segun alfa.

    Args:
        n_fijo: numero fijo de guias almacenadas en cada tabla.
        alfas_objetivo: factores de carga aproximados a evaluar.

    Returns:
        Una tupla (casillas_m, alfas_reales, tiempos_tabla) con el numero
        de casillas m, el factor de carga real (n / m) y el tiempo medio
        por busqueda en segundos.
    """
    envios, existentes = generar_envios(n_fijo, SEMILLA_DATOS)
    inexistentes = generar_guias_inexistentes(
        existentes, CANTIDAD_BUSQUEDAS, SEMILLA_INEXISTENTES
    )

    # Lista de referencia para verificar consistencia en la muestra.
    lista_ref = ListaEnlazada()
    for guia, estado in envios[:MUESTRA_VERIFICACION]:
        lista_ref.insertar(guia, estado)

    casillas_m: list[int] = []
    alfas_reales: list[float] = []
    tiempos_tabla: list[float] = []

    for alfa_obj in alfas_objetivo:
        m = primo_cercano(int(round(n_fijo / alfa_obj)))
        tabla = TablaHash(m)
        for guia, estado in envios:
            tabla.insertar(guia, estado)

        for guia, estado_esperado in envios[:MUESTRA_VERIFICACION]:
            assert tabla.buscar(guia) == estado_esperado
            assert tabla.buscar(guia) == lista_ref.buscar(guia)

        t_tabla = medir_busquedas_tabla(tabla, inexistentes, 100)

        casillas_m.append(m)
        alfas_reales.append(tabla.factor_carga())
        tiempos_tabla.append(t_tabla)

        del tabla
        gc.collect()

    return casillas_m, alfas_reales, tiempos_tabla


def graficar_experimento_a(
    tamanos: list[int],
    tiempos_lista: list[float],
    tiempos_tabla: list[float],
    ruta: str,
) -> None:
    """Genera y guarda la grafica de ListaEnlazada vs. TablaHash.

    Args:
        tamanos: numeros de guias (n) evaluados.
        tiempos_lista: tiempos medios de ListaEnlazada en segundos.
        tiempos_tabla: tiempos medios de TablaHash en segundos.
        ruta: ruta del archivo PNG de salida.
    """
    us_lista = [t * 1e6 for t in tiempos_lista]
    us_tabla = [t * 1e6 for t in tiempos_tabla]

    plt.figure(figsize=(9, 5.5))
    plt.plot(
        tamanos,
        us_lista,
        marker="o",
        linewidth=2,
        label="Lista enlazada — Θ(n)",
    )
    plt.plot(
        tamanos,
        us_tabla,
        marker="s",
        linewidth=2,
        label="Tabla hash (α ≈ 2) — Θ(1 + α)",
    )

    plt.title("Tiempo medio por búsqueda infructuosa vs. número de guías (n)")
    plt.xlabel("Número de guías almacenadas n (guías)")
    plt.ylabel("Tiempo medio por búsqueda (microsegundos, µs)")
    plt.grid(True, which="both", alpha=0.3)
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=12, prune=None))
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()


def graficar_experimento_b(
    alfas: list[float],
    tiempos_tabla: list[float],
    n_fijo: int,
    ruta: str,
) -> None:
    """Genera y guarda la grafica de tiempo de busqueda frente a alfa.

    Args:
        alfas: factores de carga reales (n / m) evaluados.
        tiempos_tabla: tiempos medios de TablaHash en segundos.
        n_fijo: numero fijo de guias usado en el experimento.
        ruta: ruta del archivo PNG de salida.
    """
    us_tabla = [t * 1e6 for t in tiempos_tabla]

    plt.figure(figsize=(9, 5.5))
    plt.plot(
        alfas,
        us_tabla,
        marker="o",
        color="#d95f02",
        linewidth=2,
        label=f"Tabla hash (n = {n_fijo:,} guías)",
    )

    plt.title(
        f"Tiempo medio por búsqueda infructuosa vs. factor de carga α "
        f"(n = {n_fijo:,})"
    )
    plt.xlabel("Factor de carga α = n / m (guías por casilla)")
    plt.ylabel("Tiempo medio por búsqueda (microsegundos, µs)")
    plt.grid(True, which="both", alpha=0.3)
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=12, prune=None))
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()


def imprimir_resultados_a(
    tamanos: list[int],
    casillas_m: list[int],
    alfas: list[float],
    tiempos_lista: list[float],
    tiempos_tabla: list[float],
) -> None:
    """Imprime en consola la tabla de resultados del Experimento A.

    Args:
        tamanos: valores de n medidos.
        casillas_m: numero de casillas m en cada medicion.
        alfas: factor de carga real en cada medicion.
        tiempos_lista: tiempos medios de ListaEnlazada en segundos.
        tiempos_tabla: tiempos medios de TablaHash en segundos.
    """
    print("=== Experimento A: Lista enlazada vs. Tabla hash (alfa ~ 2) ===")
    encabezado = (
        f"{'n':>7} {'m':>7} {'alfa':>6} {'Lista (us)':>12} "
        f"{'Tabla (us)':>12} {'Lista/Tabla':>12} {'x n':>6} "
        f"{'x Lista':>8} {'x Tabla':>8}"
    )
    print(encabezado)
    for i, n in enumerate(tamanos):
        us_l = tiempos_lista[i] * 1e6
        us_t = tiempos_tabla[i] * 1e6
        mejora = us_l / us_t if us_t > 0 else 0.0
        if i == 0:
            factores = f"{'-':>6} {'-':>8} {'-':>8}"
        else:
            factores = (
                f"{n / tamanos[i - 1]:>6.1f} "
                f"{tiempos_lista[i] / tiempos_lista[i - 1]:>8.2f} "
                f"{tiempos_tabla[i] / tiempos_tabla[i - 1]:>8.2f}"
            )
        print(
            f"{n:>7} {casillas_m[i]:>7} {alfas[i]:>6.2f} "
            f"{us_l:>12.4f} {us_t:>12.4f} {mejora:>12.1f} {factores}"
        )
    print()


def imprimir_resultados_b(
    n_fijo: int,
    casillas_m: list[int],
    alfas: list[float],
    tiempos_tabla: list[float],
) -> None:
    """Imprime en consola la tabla de resultados del Experimento B.

    Args:
        n_fijo: numero fijo de guias almacenadas.
        casillas_m: numero de casillas m en cada tabla.
        alfas: factores de carga reales medidos.
        tiempos_tabla: tiempos medios de TablaHash en segundos.
    """
    print(
        f"=== Experimento B: Efecto del factor de carga alfa (n = {n_fijo}) ==="
    )
    print(
        f"{'m':>7} {'alfa':>8} {'1 + alfa':>10} "
        f"{'Tabla (us)':>12} {'x (1+alfa)':>11} {'x Tabla':>9}"
    )
    for i, m in enumerate(casillas_m):
        us_t = tiempos_tabla[i] * 1e6
        uno_mas_alfa = 1.0 + alfas[i]
        if i == 0:
            crecimiento = f"{'-':>11} {'-':>9}"
        else:
            crecimiento = (
                f"{uno_mas_alfa / (1.0 + alfas[i - 1]):>11.2f} "
                f"{tiempos_tabla[i] / tiempos_tabla[i - 1]:>9.2f}"
            )
        print(
            f"{m:>7} {alfas[i]:>8.2f} {uno_mas_alfa:>10.2f} "
            f"{us_t:>12.4f} {crecimiento}"
        )
    print()


def main() -> None:
    """Ejecuta los experimentos A y B, imprime tablas y guarda graficas."""
    casillas_a, alfas_a, t_lista_a, t_tabla_a = ejecutar_experimento_a(
        TAMANOS_EXP_A
    )
    imprimir_resultados_a(
        TAMANOS_EXP_A, casillas_a, alfas_a, t_lista_a, t_tabla_a
    )

    casillas_b, alfas_b, t_tabla_b = ejecutar_experimento_b(
        N_FIJO_EXP_B, ALFAS_OBJETIVO_EXP_B
    )
    imprimir_resultados_b(N_FIJO_EXP_B, casillas_b, alfas_b, t_tabla_b)

    os.makedirs(CARPETA_GRAFICAS, exist_ok=True)
    ruta_a = os.path.join(CARPETA_GRAFICAS, "lista_vs_tabla.png")
    ruta_b = os.path.join(CARPETA_GRAFICAS, "tiempo_vs_alfa.png")

    graficar_experimento_a(TAMANOS_EXP_A, t_lista_a, t_tabla_a, ruta_a)
    graficar_experimento_b(alfas_b, t_tabla_b, N_FIJO_EXP_B, ruta_b)
    print(f"Graficas guardadas en '{CARPETA_GRAFICAS}/'.")


if __name__ == "__main__":
    main()
