class Planta:
    def __init__(self, posicion, ciclos_regeneracion):
        self.posicion = posicion
        self.ciclos_para_regenerar = ciclos_regeneracion
        self.activa = True

    def regenerar(self):
        if not self.activa:
            self.ciclos_para_regenerar -= 1
            if self.ciclos_para_regenerar <= 0:
                self.activa = True
                self.ciclos_para_regenerar = 0  # Resetea el contador

