# Retroalimentación — Laboratorio 1: Fundamentos, complejidad y recurrencias

**Estudiante:** Pablo Andres Tabares Cardona · **Laboratorio:** Plataforma Tamiza, ordenamiento y recurrencias
**Fecha límite:** 2026-10-04 23:59 · **Versión revisada:** commit `5758db3`

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 21 / 25 |
| Calidad de la explicación teórica | 21 / 25 |
| Corrección de la implementación | 14 / 20 |
| Calidad del análisis de las gráficas | 16 / 20 |
| Documentación y organización del informe | 5 / 10 |
| **Total** | **77 / 100** |
| **Nota (0–5)** | **3.85** |

## 1. Corrección conceptual (21 / 25)
**Lo que hizo bien:**
- Distingue bien entre que el resultado sea correcto y que llegue a tiempo, y nombra la restricción que se incumple: las cuatro horas.
- Explica que un servidor el doble de rápido solo aplaza el problema cuando lleguen más pacientes.
- Su segundo ejemplo (el analizador de vulnerabilidades del pipeline) es propio y concreto: 5.000 dependencias, 200.000 vulnerabilidades, 45 minutos frente a un límite de 5.
- En la Parte 2 señala dos perjuicios (el paciente de alto riesgo y el operador del centro de contacto) y dice quién asume el costo de cada uno. También discute que el orden de la lista decide a quién se llama primero.

**Lo que puede mejorar:**
- La parte ambiental es general: diga cuánto más tarda el proceso y cómo eso se convierte en energía, por ejemplo horas de servidor al año.
- La frase "el algoritmo se pasa de tiempo" sería más convincente con un dato propio sobre cuánto crece el tiempo al duplicar los registros.

## 2. Calidad de la explicación teórica (21 / 25)
**Lo que hizo bien:**
- Define peor, mejor y caso promedio indicando sobre qué se toma cada uno, y justifica con claridad por qué usaría el peor caso para decidir.
- Escribe la predicción de los escenarios (A promedio, B mejor, C peor) y el experimento la confirma.
- Plantea la recurrencia de merge sort, explica cada término y la resuelve por sustitución con hipótesis, paso y condición `c >= d`.
- Hace el análisis línea a línea de insertion sort y presenta la tabla de complejidades.

**Lo que puede mejorar:**
- En la sustitución falta revisar el caso base, que es lo que cierra una demostración por inducción.
- La predicción no queda marcada como escrita antes de medir; dígalo de forma explícita.
- En la tabla línea a línea, el conteo de la línea `else: break` y de la comparación no queda del todo consistente con el código.

## 3. Corrección de la implementación (14 / 20)
**Lo que hizo bien:**
- `insertion_sort` y `merge_sort` ordenan bien de mayor a menor, no cambian la lista recibida, cuentan las comparaciones entre elementos y no usan `sorted()` ni `sort()`. `merge_sort` tiene su propia mezcla recursiva.
- Los tres generadores dan listas del tamaño pedido, sin repetidos, y el escenario B queda con el 2 % desordenado al final.

**Lo que puede mejorar:**
- Las funciones de `parte3_casos.py` y `parte4_complejidad.py` no tienen *docstring* ni *type hints*; tampoco `datos.py` ni `algoritmos.py` cuidan del todo el formato.
- Hay muchos incumplimientos de PEP 8: falta de dos líneas en blanco entre funciones y líneas muy largas.
- La función auxiliar `_mezclar` tiene un *docstring* corto, sin las secciones Args y Returns.
- Los generadores aleatorios cambian la semilla global de Python; es mejor usar un generador propio.

## 4. Calidad del análisis de las gráficas (16 / 20)
**Lo que hizo bien:**
- Las tres gráficas existen, tienen título, ejes con nombre y leyenda, y las curvas están en los mismos ejes.
- Identifica correctamente C como peor caso, B como mejor y A como intermedio, apoyándose en lo que se ve en las curvas.
- Concluye que merge sort conviene y explica por qué en tamaños pequeños puede no notarse la diferencia.
- En 4.3 recomienda un algoritmo, responde a la propuesta del servidor y declara la extrapolación como estimación.

**Lo que puede mejorar:**
- Los datos citados no coinciden con sus gráficas: dice 1.8 s para insertion sort con n=6400 en el peor caso, pero la gráfica muestra cerca de 1.5 s; dice 0.02 s para merge sort y la gráfica muestra cerca de 0.01 s. Cite lo que realmente se ve.
- Para el servidor del doble de velocidad, use el dato del escenario aleatorio de la gráfica de la Parte 4.
- Solo discute la memoria extra; sería bueno mencionar también la estabilidad o el riesgo de que el escenario B cambie.
- En la conclusión de 4.3 compare con una curva medida, no solo con la teoría.

## 5. Documentación y organización del informe (5 / 10)
**Lo que hizo bien:**
- La carpeta del laboratorio está en la ubicación acordada y tiene todos los archivos pedidos.
- El informe sigue el orden de las partes, incrusta las tres gráficas con rutas que funcionan y enlaza el código de cada parte.
- Incluye instrucciones para reproducir el experimento.

**Lo que puede mejorar:**
- Solo hay un commit que toca este laboratorio; se pedían al menos cinco commits descriptivos que muestren el avance.
- Las instrucciones de activación del entorno solo cubren Windows y Git Bash.

## ¿El código funciona?
Sí. Los dos programas corren sin errores, generan las tres gráficas y los dos algoritmos ordenan correctamente en mis pruebas con listas pequeñas, aleatorias, casi ordenadas e inversas.

## Para el próximo laboratorio
- Haga commits pequeños y frecuentes con mensajes que cuenten qué cambió.
- Agregue *docstring* y *type hints* a todas las funciones, también a los scripts de experimento, y revise el estilo PEP 8.
- Copie en el informe los números que realmente muestran sus gráficas.
- Cierre las demostraciones matemáticas con su caso base y escriba la predicción antes del experimento.
- Cuantifique la parte ambiental con horas de ejecución y energía estimada.
