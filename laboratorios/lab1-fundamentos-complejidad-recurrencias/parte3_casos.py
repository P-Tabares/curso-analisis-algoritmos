import time
import os
import matplotlib.pyplot as plt
from algoritmos import insertion_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso

def ejecutar_experimento():
    # Tamaños de entrada (n) para el experimento
    tamanos = [100, 200, 400, 800, 1600, 3200, 6400]
    
    # Listas para almacenar métricas
    comps_a, comps_b, comps_c = [], [], []
    tiempos_a, tiempos_b, tiempos_c = [], [], []
    
    print("Iniciando experimento...")
    
    for n in tamanos:
        print(f"Procesando tamaño n = {n}")
        lote_a = generar_aleatorio(n)
        lote_b = generar_casi_ordenado(n)
        lote_c = generar_inverso(n)
        
        #Escenario A: Aleatorio
        t0 = time.perf_counter()
        _, c_a = insertion_sort(lote_a)
        t1 = time.perf_counter()
        comps_a.append(c_a)
        tiempos_a.append(t1 - t0)
        
        #Escenario B: Casi Ordenado
        t0 = time.perf_counter()
        _, c_b = insertion_sort(lote_b)
        t1 = time.perf_counter()
        comps_b.append(c_b)
        tiempos_b.append(t1 - t0)
        
        #Escenario C: Orden Inverso
        t0 = time.perf_counter()
        _, c_c = insertion_sort(lote_c)
        t1 = time.perf_counter()
        comps_c.append(c_c)
        tiempos_c.append(t1 - t0)

    os.makedirs(os.path.join(os.path.dirname(__file__), "graficas"), exist_ok=True)
    
    #Gráfica de Comparaciones
    plt.figure(figsize=(10, 6))
    plt.plot(tamanos, comps_a, label='Escenario A (Aleatorio)', marker='o')
    plt.plot(tamanos, comps_b, label='Escenario B (Casi Ordenado)', marker='s')
    plt.plot(tamanos, comps_c, label='Escenario C (Inverso)', marker='^')
    plt.title('Insertion Sort: Comparaciones vs Tamaño de Entrada')
    plt.xlabel('Tamaño de entrada (n)')
    plt.ylabel('Número de comparaciones')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(os.path.dirname(__file__), "graficas", "parte3_comparaciones.png"))
    plt.close()
    
    #Gráfica de Tiempo
    plt.figure(figsize=(10, 6))
    plt.plot(tamanos, tiempos_a, label='Escenario A (Aleatorio)', marker='o')
    plt.plot(tamanos, tiempos_b, label='Escenario B (Casi Ordenado)', marker='s')
    plt.plot(tamanos, tiempos_c, label='Escenario C (Inverso)', marker='^')
    plt.title('Insertion Sort: Tiempo de Ejecución vs Tamaño de Entrada')
    plt.xlabel('Tamaño de entrada (n)')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(os.path.dirname(__file__), "graficas", "parte3_tiempo.png"))
    plt.close()
    
    print("Experimento finalizado. Revisa la carpeta 'graficas/' para ver los resultados.")

if __name__ == "__main__":
    ejecutar_experimento()