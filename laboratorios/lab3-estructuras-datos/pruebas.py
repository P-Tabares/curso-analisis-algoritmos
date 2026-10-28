"""Pruebas de estructuras.py: casos base, colisiones y colecciones aleatorias."""
import random

from estructuras import ListaEnlazada, TablaHash

ESTADOS = ("en bodega", "en reparto", "entregado", "en transito")

# 1. Caso de la situacion problema:
#    busquedas exitosas e infructuosas en la lista y en la tabla
envios_ejemplo = [
    (1000000010, "en bodega"),
    (1000000024, "en reparto"),
    (1000000017, "en bodega"),
    (1000000005, "entregado"),
]

lista_ejemplo = ListaEnlazada()
tabla_ejemplo = TablaHash(11)

# Verificar estructuras vacias antes de insertar
assert lista_ejemplo.tamano == 0
assert lista_ejemplo.buscar(1000000010) is None
assert tabla_ejemplo.tamano == 0
assert tabla_ejemplo.buscar(1000000010) is None
assert tabla_ejemplo.factor_carga() == 0.0

for guia, estado in envios_ejemplo:
    lista_ejemplo.insertar(guia, estado)
    tabla_ejemplo.insertar(guia, estado)

assert lista_ejemplo.tamano == 4
assert tabla_ejemplo.tamano == 4

# Busquedas exitosas en ambas estructuras
for guia, estado_esperado in envios_ejemplo:
    assert lista_ejemplo.buscar(guia) == estado_esperado
    assert tabla_ejemplo.buscar(guia) == estado_esperado

# Busquedas infructuosas (guias que no existen)
for guia_inexistente in (1000000000, 1000000099, 9999999999):
    assert lista_ejemplo.buscar(guia_inexistente) is None
    assert tabla_ejemplo.buscar(guia_inexistente) is None

# 2. Colision forzada: con m = 7, las guias 10, 24 y 17 caen en la casilla 3
tabla = TablaHash(7)
for guia in (10, 24, 17):
    assert tabla.hash(guia) == 3
    tabla.insertar(guia, "en bodega")

assert tabla.casillas[3].tamano == 3
assert tabla.buscar(10) == "en bodega"
assert tabla.buscar(24) == "en bodega"
assert tabla.buscar(17) == "en bodega"
assert tabla.buscar(99) is None
assert tabla.buscar(3) is None
assert tabla.factor_carga() == 3 / 7

# 3. colecciones aleatorias: lista y tabla responden igual
#    tanto para guias existentes como para guias inexistentes
generador = random.Random(42)

for _ in range(30):
    n = generador.randint(10, 300)
    m = generador.choice([7, 13, 31, 61, 127])
    lista = ListaEnlazada()
    tabla_aleatoria = TablaHash(m)

    guias_universo = generador.sample(
        range(1_000_000_000, 2_000_000_000), n * 2
    )
    guias_existentes = guias_universo[:n]
    guias_inexistentes = guias_universo[n:]

    esperados: list[tuple[int, str]] = []
    for guia in guias_existentes:
        estado = generador.choice(ESTADOS)
        lista.insertar(guia, estado)
        tabla_aleatoria.insertar(guia, estado)
        esperados.append((guia, estado))

    assert lista.tamano == n
    assert tabla_aleatoria.tamano == n
    assert tabla_aleatoria.factor_carga() == n / m

    for guia, estado_esperado in esperados:
        res_lista = lista.buscar(guia)
        res_tabla = tabla_aleatoria.buscar(guia)
        assert res_lista == estado_esperado
        assert res_tabla == res_lista

    for guia_no_existe in guias_inexistentes:
        res_lista = lista.buscar(guia_no_existe)
        res_tabla = tabla_aleatoria.buscar(guia_no_existe)
        assert res_lista is None
        assert res_tabla == res_lista

print("Todas las pruebas pasaron.")
