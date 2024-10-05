from mapa import Mapa
from modeloManager import ModeloManager
from visualizadormatriz import VisualizadorMatriz

# Variables configurables
tamaño_tablero = 20
num_bichos = 1
num_plantas = 75
num_depredadores = 0
ciclos_regeneracion_plantas = 100  # Ciclos hasta que una planta regenera
vida_recuperada_al_comer = 150  # Vida que un bicho recupera al comer
vida_perdida_por_ciclo = 5  # Vida que un bicho pierde en cada ciclo
vida_inicial_bichos = 1000  # Vida inicial de los bichos
rango_observacion_bichos = 20  # Rango de observación de los bichos
ciclos_reproduccion = 1000  # Ciclos hasta que un bicho se puede reproducir
num_plantas_venenosas = 4  # Número de plantas venenosas

# Crear el gestor de modelos
gestor_modelo = ModeloManager("modelo_entrenado.pkl")  # Ruta del modelo guardado

# Cargar o entrenar desde cero
try:
    red_neuronal_cargada = gestor_modelo.cargar_modelo()
    print("Modelo cargado exitosamente.")
except FileNotFoundError:
    print("No se encontró un modelo previo. Entrenando desde cero...")
    red_neuronal_cargada = None  # Se entrena desde cero

# Inicializar el mapa con las variables configurables
mapa = Mapa(
    tamaño=tamaño_tablero,
    num_bichos=num_bichos,
    num_plantas=num_plantas,
    num_plantas_venenosas=num_plantas_venenosas,
    num_depredadores=num_depredadores,
    ciclos_regeneracion_plantas=ciclos_regeneracion_plantas,
    vida_recuperada_al_comer=vida_recuperada_al_comer,
    vida_perdida_por_ciclo=vida_perdida_por_ciclo,
    vida_inicial_bichos=vida_inicial_bichos,
    rango_observacion_bichos=rango_observacion_bichos,
    ciclos_reproduccion=ciclos_reproduccion
)

# Crear el visualizador de la matriz
visualizador = VisualizadorMatriz(frame_size=600)

# Asignar la red neuronal cargada a todos los bichos si existe
if red_neuronal_cargada:
    for bicho in mapa.bichos:
        bicho.red_neuronal = red_neuronal_cargada

# Simulación automática
for ciclo in range(10000):
    mapa.ejecutar_ciclo()
    
    # Obtener la matriz actualizada del mapa
    matriz_actualizada = mapa.matriz
    
    # Dibujar la matriz usando el visualizador
    visualizador.dibujar(matriz_actualizada)

    # Guardar el modelo cada 1000 ciclos
    if ciclo % 1000 == 0:
        gestor_modelo.guardar_modelo(mapa.bichos[0])  # Guardar el modelo del primer bicho

# Guardar el modelo al finalizar la simulación
gestor_modelo.guardar_modelo(mapa.bichos[0])
print("Simulación completada y modelo guardado.")

