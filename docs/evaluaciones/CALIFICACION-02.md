# Retroalimentación — Laboratorio 2: Dividir y vencer

**Estudiante:** Pablo Andrés Tabares Cardona · **Laboratorio:** Laboratorio evaluativo 02 — Dividir y vencer
**Fecha límite:** 2026-10-21 23:59 · **Versión revisada:** commit `4cc7e1e`

Muy buen trabajo: el laboratorio está completo, ordenado y bien explicado.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 19 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 23 / 25 |
| Calidad del análisis de las gráficas | 23 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **95 / 100** |
| **Nota (0–5)** | **4.75** |

## 1. Corrección conceptual (19 / 20)
**Lo que hizo bien:**
- Identificó que entre 10 y 50 días divide y vencerás empieza a ganar y explicó por qué: dividir tiene un costo fijo que pesa en listas cortas.
- Comparó con el máximo de un arreglo: dividir no mejora porque sigue siendo `Θ(n)` y suma el costo de las llamadas.
- Recomendó un algoritmo y declaró la cifra para 1.000.000 de registros como estimación, con un razonamiento que no es una regla de tres lineal.

**Lo que puede mejorar:**
- Explique con más cuidado que el tiempo estimado sale de extrapolar sus mediciones y que el computador real puede variar.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Planteó `T(n) = 2T(n/2) + Θ(n)` explicando de dónde sale cada término.
- Resolvió con el método maestro y verificó la condición del caso 2.
- Justificó bien por qué la fuerza bruta es `Θ(n²)`.

## 3. Corrección de la implementación (23 / 25)
**Lo que hizo bien:**
- Las tres funciones dan la suma correcta en todos los casos pedidos y en 50 listas aleatorias.
- `subarreglo_maximo` resuelve los tres casos sin usar la fuerza bruta y ninguna función cambia la lista recibida.
- Las pruebas son completas y verifican también que los índices sean coherentes.

**Lo que puede mejorar:**
- En `subarreglo.py` falta separar con dos líneas en blanco la descripción inicial del archivo y la primera función.
- Algunos docstrings tienen detalles: falta una línea en blanco antes de `Returns` en `subarreglo_fuerza_bruta`, y en `repeticiones` el nombre del parámetro en el docstring no coincide con el del código.

## 4. Calidad del análisis de las gráficas (23 / 25)
**Lo que hizo bien:**
- La gráfica tiene ambas curvas en los mismos ejes, título, ejes rotulados y leyenda, con 9 tamaños.
- Calculó los factores de crecimiento al duplicar `n` (×4,1 y ×2,0) y los comparó con `Θ(n²)` y `Θ(n log n)`.

**Lo que puede mejorar:**
- Las cifras del texto no coinciden del todo con la gráfica publicada: el texto habla de unos 600 ms con 4.000 días, y en la imagen la fuerza bruta está cerca de 500 ms; con 8.000 días la imagen muestra cerca de 2.000 ms y con 16.000 cerca de 8.050 ms, mientras la tabla dice 2.251 y 8.807. Procure que la tabla y la gráfica vengan de la misma corrida.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- Usó la ubicación acordada (`laboratorios/lab2-divide-y-vencer/`), con todos los archivos pedidos.
- El informe sigue el orden pedido, la gráfica se ve, enlaza su código en cada parte y trae instrucciones de reproducción.
- Hay seis commits con mensajes descriptivos.

## ¿El código funciona?
Sí. Las pruebas pasan, la medición corre sin errores, verifica que ambos algoritmos den la misma suma y genera la gráfica.

## Para el próximo laboratorio
- Genere la tabla y la gráfica en la misma corrida y cite los valores tal como se ven en la imagen.
- Revise el estilo (líneas en blanco entre funciones) y que los docstrings coincidan con los parámetros reales.
- Deje claro en las estimaciones qué supuestos hace.
