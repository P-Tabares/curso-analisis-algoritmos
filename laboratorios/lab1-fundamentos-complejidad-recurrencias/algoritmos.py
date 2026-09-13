"""Algoritmos de ordenamiento instrumentados para el Laboratorio 1."""

def insertion_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de insercion.
    
    No modifica la lista recibida: trabaja sobre una copia.
    
    Args:
        datos: lista de indices de riesgo a ordenar.
        
    Returns:
        Una tupla con la lista ordenada de mayor a menor y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    # Se crea una copia
    arr = list(datos)
    n = len(arr)
    comparaciones = 0
    
    # Se itera desde el segundo elemento hasta el final
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        while j >= 0:
            comparaciones += 1
            if arr[j] < key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
                
        arr[j + 1] = key
        
    return arr, comparaciones


def merge_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de mezcla.
    
    No modifica la lista recibida: trabaja sobre una copia.
    
    Args:
        datos: lista de indices de riesgo a ordenar.
        
    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    # Caso base
    if len(datos) <= 1:
        return list(datos), 0
        
    # DIVIDIR
    medio = len(datos) // 2
    
    # CONQUISTAR
    mitad_izq, comps_izq = merge_sort(datos[:medio])
    mitad_der, comps_der = merge_sort(datos[medio:])
    
    # COMBINAR
    lista_mezclada, comps_mezcla = _mezclar(mitad_izq, mitad_der)
    

    comps_totales = comps_izq + comps_der + comps_mezcla
    
    return lista_mezclada, comps_totales


def _mezclar(izq: list[int], der: list[int]) -> tuple[list[int], int]:
    """Mezcla dos sublistas ordenadas de mayor a menor."""
    resultado = []
    comparaciones = 0
    i = 0
    j = 0
    
    # Comparar elementos de ambas listas
    while i < len(izq) and j < len(der):
        comparaciones += 1
        # Orden descendente
        if izq[i] >= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
            
    #elementos sobrantes
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    
    return resultado, comparaciones