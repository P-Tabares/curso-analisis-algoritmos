def calcular_promedio(lista_numeros: list[int]) -> float:
    """Calcula el promedio de una lista de números.

    Recibe una lista de números enteros y retorna su promedio como un número
    decimal.
    """
    suma_numeros = 0

    for numero in lista_numeros:
        suma_numeros = suma_numeros + numero

    return suma_numeros / len(lista_numeros)


def main() -> None:
    """Calcula y muestra el promedio de la lista de ejemplo."""
    lista_numeros = [1, 2, 3, 4, 5]
    print(calcular_promedio(lista_numeros))


if __name__ == "__main__":
    main()