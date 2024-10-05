import pickle


class ModeloManager:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def guardar_modelo(self, bicho):
        """Guarda la red neuronal del bicho en un archivo."""
        with open(self.nombre_archivo, 'wb') as archivo:
            pickle.dump(bicho.red_neuronal, archivo)
        print(f"Modelo guardado en {self.nombre_archivo}")

    def cargar_modelo(self):
        """Carga la red neuronal desde un archivo y devuelve la red neuronal."""
        with open(self.nombre_archivo, 'rb') as archivo:
            red_neuronal = pickle.load(archivo)
        print(f"Modelo cargado desde {self.nombre_archivo}")
        return red_neuronal
