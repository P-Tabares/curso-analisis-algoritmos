"""Pruebas de subarreglo.py: casos conocidos y listas aleatorias."""
import random

from subarreglo import (
    subarreglo_fuerza_bruta,
    subarreglo_maximo,
    suma_cruzada,
)


def verificar(serie: list[float], esperada: float) -> None:
    """Verifica ambas funciones contra una suma conocida."""
    copia = list(serie)

    inicio_b, fin_b, suma_b = subarreglo_fuerza_bruta(serie)
    inicio_d, fin_d, suma_d = subarreglo_maximo(serie, 0, len(serie) - 1)

    assert suma_b == esperada, f"Fuerza bruta: {suma_b} != {esperada}"
    assert suma_d == esperada, f"Divide y venceras: {suma_d} != {esperada}"

    assert 0 <= inicio_b <= fin_b < len(serie)
    assert 0 <= inicio_d <= fin_d < len(serie)
    assert sum(serie[inicio_b:fin_b + 1]) == suma_b
    assert sum(serie[inicio_d:fin_d + 1]) == suma_d

    assert serie == copia, "La lista de entrada fue modificada"


# Serie de ocho dias de la situacion problema (racha del dia 2 al 7).
serie_ocho = [-3, 5, -2, 8, -6, 3, 9, -4]
verificar(serie_ocho, 17)
assert subarreglo_fuerza_bruta(serie_ocho)[:2] == (1, 6)
assert subarreglo_maximo(serie_ocho, 0, 7)[:2] == (1, 6)

# Un solo elemento (positivo, negativo y cero).
verificar([7], 7)
verificar([-7], -7)
verificar([0], 0)

# Todos negativos: el mejor tramo es el elemento menos negativo.
verificar([-8, -3, -6, -2, -9], -2)

# Todos positivos: el mejor tramo es la serie completa.
verificar([4, 1, 7, 3, 2], 17)
assert subarreglo_maximo([4, 1, 7, 3, 2], 0, 4)[:2] == (0, 4)

# El mejor tramo cruza el punto medio (indices 3 y 4 en una serie de 8).
serie_cruzada = [-2, 1, -3, 4, 5, -1, 2, -6]
verificar(serie_cruzada, 10)
assert suma_cruzada(serie_cruzada, 0, 3, 7) == (3, 6, 10)
assert subarreglo_maximo(serie_cruzada, 0, 7)[:2] == (3, 6)

# Valores decimales (variaciones en miles de pesos).
verificar([1.5, -0.5, 2.0, -4.0, 3.0], 3.0)

# Listas aleatorias: ambas funciones deben dar la misma suma.
random.seed(42)
for _ in range(50):
    tamano = random.randint(1, 200)
    serie_aleatoria = [random.randint(-100, 100) for _ in range(tamano)]
    suma_b = subarreglo_fuerza_bruta(serie_aleatoria)[2]
    suma_d = subarreglo_maximo(serie_aleatoria, 0, tamano - 1)[2]
    assert suma_b == suma_d, (
        f"Discrepancia en {serie_aleatoria}: {suma_b} != {suma_d}"
    )

print("Todas las pruebas pasaron.")