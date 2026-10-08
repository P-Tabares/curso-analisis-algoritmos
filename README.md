# Curso de Análisis de Algoritmos

Repositorio de ejercicios, laboratorios y mediciones de rendimiento del curso de Análisis de Algoritmos.

**Estudiante:** Pablo Tabares Cardona

## Estructura del repositorio

- `benchmarks/`: contiene pruebas y mediciones para comparar el rendimiento de algoritmos.
- `ejercicios-clase/`: reúne los ejercicios desarrollados durante las sesiones de clase.
- `laboratorios/`: almacena prácticas experimentales y actividades de laboratorio.

## Instalación y ejecución

Desde la raíz del proyecto, crea y activa un entorno virtual e instala las dependencias:

```bash
# Windows PowerShell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Para ejecutar el clasificador de años:

```bash
# Windows
python ejercicios-clase/semana-02/clasificador_anios.py
```

```bash
# macOS / Linux
python3 ejercicios-clase/semana-02/clasificador_anios.py
```
