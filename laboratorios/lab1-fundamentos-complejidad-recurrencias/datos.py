"""Generadores de lotes de registros para los escenarios de Tamiza."""
import random

def generar_aleatorio(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote de n registros en orden aleatorio (escenario A).
    
    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio, para que el
            experimento sea reproducible.
            
    Returns:
        Lista de n indices de riesgo enteros distintos, desordenada.
    """
    random.seed(semilla)
    return random.sample(range(1, n * 10), n)

def generar_casi_ordenado(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote casi ordenado: 98% ordenado y 2% al final (escenario B).
    
    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio.
        
    Returns:
        Lista de n indices de riesgo enteros distintos, con el primer
        98% en el orden que el algoritmo produce y el 2% restante
        desordenado al final.
    """
    random.seed(semilla)
    limite = int(n * 0.98)
    
    #El 98% ordenado de mayor a menor
    parte_ordenada = list(range(n * 10, n * 10 - limite, -1))
    
    #El 2% valores aleatorios menores
    parte_desordenada = random.sample(range(1, n * 10 - limite), n - limite)
    
    return parte_ordenada + parte_desordenada

def generar_inverso(n: int) -> list[int]:
    """Genera un lote en el orden exactamente contrario (escenario C).
    
    Args:
        n: cantidad de registros del lote.
        
    Returns:
        Lista de n indices de riesgo enteros distintos, en el orden
        inverso al que el algoritmo debe producir.
    """
    return list(range(1, n + 1))