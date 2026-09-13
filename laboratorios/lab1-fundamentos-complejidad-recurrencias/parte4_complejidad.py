import time
import os
import matplotlib.pyplot as plt
from algoritmos import insertion_sort, merge_sort
from datos import generar_aleatorio

def ejecutar_comparativa():
    tamanos = [100, 200, 400, 800, 1600, 3200, 6400]
    
    tiempos_insertion = []
    tiempos_merge = []
    
    print("Iniciando medición comparativa sobre Escenario A (Aleatorio)...")
    
    for n in tamanos:
        print(f"Midiendo para n = {n}")
        # Generar un único lote aleatorio para que ambos algoritmos compitan en igualdad
        lote = generar_aleatorio(n)
        
        # Medición de Insertion Sort
        t0 = time.perf_counter()
        insertion_sort(lote)
        t1 = time.perf_counter()
        tiempos_insertion.append(t1 - t0)
        
        # Medición de Merge Sort
        t0 = time.perf_counter()
        merge_sort(lote)
        t1 = time.perf_counter()
        tiempos_merge.append(t1 - t0)

    os.makedirs(os.path.join(os.path.dirname(__file__), "graficas"), exist_ok=True)
    
    # Generar la gráfica comparativa
    plt.figure(figsize=(10, 6))
    plt.plot(tamanos, tiempos_insertion, label='Insertion Sort', marker='o', color='red')
    plt.plot(tamanos, tiempos_merge, label='Merge Sort', marker='s', color='blue')
    
    plt.title('Comparativa de Tiempo de Ejecución: Insertion Sort vs. Merge Sort (Escenario Aleatorio)')
    plt.xlabel('Tamaño de entrada (n)')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig(os.path.join(os.path.dirname(__file__), "graficas", "parte4_tiempo.png"), bbox_inches='tight')
    plt.close()
    
    print("Medición completada. Gráfica guardada en 'graficas/parte4_tiempo.png'.")

if __name__ == "__main__":
    ejecutar_comparativa()