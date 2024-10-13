class Planta:
    def __init__(self, posicion, ciclos_regeneracion):
        self.posicion = posicion
        self.ciclos_para_regenerar = ciclos_regeneracion
        self.activa = True

    def regenerar(self, mapa):
        if not self.activa:
            self.ciclos_para_regenerar -= 1
            if self.ciclos_para_regenerar <= 0:
                self.activa = True
                fila, col = divmod(self.posicion, mapa.tamaño)
                mapa.matriz[fila, col] = 1  # Restaurar la planta en el mapa
                self.ciclos_para_regenerar = mapa.ciclos_regeneracion_plantas

    def eliminar(self, mapa):
        """Desactiva la planta y la elimina del mapa."""
        if self.activa:
            self.activa = False
            fila, col = divmod(self.posicion, mapa.tamaño)
            mapa.matriz[fila, col] = 0
            self.ciclos_para_regenerar = mapa.ciclos_regeneracion_plantas

