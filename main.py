from mapa import Mapa
from modeloManager import ModeloManager
from visualizadormatriz import VisualizadorMatriz

# Variables configurables
tamaño_tablero = 40
num_bichos = 20
num_plantas = 500
num_plantas_venenosas = 50
num_depredadores = 2
ciclos_regeneracion_plantas = 100
vida_recuperada_al_comer = 150
vida_perdida_por_ciclo = 5
vida_inicial_bichos = 1000
rango_observacion_bichos = 10
ciclos_reproduccion = 1000
vida_perdida_por_veneno = 100



# Crear los gestores de modelos para bichos y depredadores
gestor_modelo_bicho = ModeloManager("modelo_entrenado.pkl")  # Ruta del modelo de bicho


# Cargar o entrenar desde cero para bichos
try:
    red_neuronal_bicho_cargada = gestor_modelo_bicho.cargar_modelo()
    print("Modelo de bicho cargado exitosamente.")
except FileNotFoundError:
    print("No se encontró un modelo previo de bicho. Entrenando desde cero...")
    red_neuronal_bicho_cargada = None  # Se entrena desde cero




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
    ciclos_reproduccion=ciclos_reproduccion,
    vida_perdida_por_veneno=vida_perdida_por_veneno,

)

# Crear el visualizador de la matriz
visualizador = VisualizadorMatriz(frame_size=600)

# Asignar la red neuronal cargada a todos los bichos si existe
if red_neuronal_bicho_cargada:
    for bicho in mapa.bichos:
        bicho.red_neuronal = red_neuronal_bicho_cargada



# Simulación automática
for ciclo in range(100000):
    mapa.ejecutar_ciclo()
    
    # Obtener la matriz actualizada del mapa
    matriz_actualizada = mapa.matriz
    
    # Dibujar la matriz usando el visualizador
    visualizador.dibujar(matriz_actualizada)

    # Guardar los modelos cada 1000 ciclos
    if ciclo % 1000 == 0:
        # Guardar el modelo del primer bicho
        if mapa.bichos:
            gestor_modelo_bicho.guardar_modelo(mapa.bichos[0])


# Guardar los modelos al finalizar la simulación
if mapa.bichos:
    gestor_modelo_bicho.guardar_modelo(mapa.bichos[0])

