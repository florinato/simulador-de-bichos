from mapa import Mapa
from visualizadormatriz import VisualizadorMatriz

# Variables configurables
tamaño_tablero = 50
num_bichos = 2
num_plantas =200
num_depredadores = 0
ciclos_regeneracion_plantas = 100 # Ciclos hasta que una planta regenera
vida_recuperada_al_comer = 150        # Vida que un bicho recupera al comer
vida_perdida_por_ciclo = 5       # Vida que un bicho pierde en cada ciclo
vida_inicial_bichos = 1000           # Vida inicial de los bichos
rango_observacion_bichos =20   # Rango de observación de los bichos
ciclos_reproduccion = 1000           # Ciclos hasta que un bicho se puede reproducir
num_plantas_venenosas=10

# Inicializar el mapa con las variables configurables
mapa = Mapa(
    tamaño=tamaño_tablero,
    num_bichos=num_bichos,
    num_plantas=num_plantas,
    num_plantas_venenosas=num_plantas_venenosas,  # Añadimos las plantas venenosas
    num_depredadores=num_depredadores,
    ciclos_regeneracion_plantas=ciclos_regeneracion_plantas,
    vida_recuperada_al_comer=vida_recuperada_al_comer,
    vida_perdida_por_ciclo=vida_perdida_por_ciclo,
    vida_inicial_bichos=vida_inicial_bichos,
    rango_observacion_bichos=rango_observacion_bichos,
    ciclos_reproduccion=ciclos_reproduccion
)


visualizador = VisualizadorMatriz(frame_size=600)

# Simulación automática
for ciclo in range(100000):
    mapa.ejecutar_ciclo()
    # Obtener la matriz actualizada del mapa
    matriz_actualizada = mapa.matriz

    # Dibujar la matriz usando el visualizador
    visualizador.dibujar(matriz_actualizada)

