"""Subarreglo maximo: fuerza bruta y divide y venceras."""
 
 
def subarreglo_fuerza_bruta(valores: list[float]) -> tuple[int, int, float]:
    """Encuentra la mejor racha probando todos los pares de dias (i, j).
 
    Args:
        valores: variacion diaria de caja, una por dia. Tiene al menos
            un elemento.
 
    Returns:
        Una tupla (inicio, fin, suma) con los indices inclusivos del
        tramo de mayor suma y el valor de esa suma.
    """
    # TODO: implemente la solucion en Θ(n²): acumule la suma dentro del
    # ciclo en vez de recalcularla desde cero para cada par.
 
 
def suma_cruzada(
    valores: list[float], inicio: int, medio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra el mejor tramo que cruza el punto medio.
 
    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango considerado (inclusive).
        medio: indice del ultimo elemento de la mitad izquierda.
        fin: indice final del rango considerado (inclusive).
 
    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo que incluye al
        menos un elemento de cada mitad.
    """
    # TODO: barrido lineal desde el punto medio hacia cada lado.
 
 
def subarreglo_maximo(
    valores: list[float], inicio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra la mejor racha por divide y venceras.
 
    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango a considerar (inclusive).
        fin: indice final del rango a considerar (inclusive).
 
    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo dentro de
        valores[inicio..fin].
    """
    # TODO: caso base, dos llamadas recursivas, caso cruzado y combinar.