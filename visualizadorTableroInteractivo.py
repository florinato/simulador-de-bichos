import tkinter as tk

import numpy as np


class VisualizadorTableroInteractivo:
    def __init__(self, tamaño, frame_size):
        self.tamaño = tamaño
        self.frame_size = frame_size  # Tamaño total del frame en píxeles
        self.matriz = np.zeros((tamaño, tamaño))  # Inicializar tablero vacío (sin plantas)
        self.root = tk.Tk()  # Crear ventana de Tkinter
        self.root.title("Tablero Interactivo de Plantas")

        # Configurar el canvas con el tamaño exacto
        self.canvas = tk.Canvas(self.root, width=self.frame_size, height=self.frame_size)
        self.canvas.pack()

        # Vincular el evento de clic con la función de colocar planta
        self.canvas.bind("<Button-1>", self.colocar_planta)

        # Dibujar el tablero inicial
        self.dibujar()

    def colocar_planta(self, event):
        # Obtener la posición del clic en el canvas
        cell_width = self.frame_size // self.tamaño
        cell_height = self.frame_size // self.tamaño

        col = event.x // cell_width
        fila = event.y // cell_height

        # Colocar planta en esa posición (valor 1) y recalcular olores
        self.matriz[fila, col] = 1  # Plantas representadas con 1 (verde)

        # Recalcular el mapa de olores
        mapa_olor = self.calcular_olor()
        print(f"Mapa de olores:\n{mapa_olor}")

        # Redibujar el tablero con la planta
        self.dibujar(mapa_olor)

    def calcular_olor(self):
        """Calcula el mapa de olores basados en la posición de las plantas y la distancia euclidiana."""
        mapa_olor = np.zeros((self.tamaño, self.tamaño))
        for fila in range(self.tamaño):
            for col in range(self.tamaño):
                # Calcular el olor basado en la distancia euclidiana a todas las plantas
                suma_olor = 0
                for i in range(self.tamaño):
                    for j in range(self.tamaño):
                        if self.matriz[i, j] == 1:  # Si hay una planta
                            distancia = np.sqrt((fila - i) ** 2 + (col - j) ** 2) + 1  # Distancia euclidiana
                            suma_olor += 10 / distancia
                mapa_olor[fila, col] = round(suma_olor, 1)  # Redondear a 1 decimal
        return mapa_olor

    def dibujar(self, mapa_olor=None):
        # Obtener el tamaño de cada celda basado en el tamaño de la matriz
        cell_width = self.frame_size // self.tamaño
        cell_height = self.frame_size // self.tamaño

        # Limpiar el canvas antes de dibujar la nueva matriz
        self.canvas.delete("all")

        # Dibujar las celdas
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                x1 = j * cell_width
                y1 = i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                # Determinar el color: verde claro para plantas, blanco para celdas vacías
                if self.matriz[i][j] == 1:  # Si es una planta
                    color = '#90EE90'  # Verde claro
                else:
                    color = 'white'  # Blanco para celdas vacías

                # Dibujar el rectángulo en la celda correspondiente
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Si tenemos un mapa de olor, mostrar el valor redondeado
                if mapa_olor is not None:
                    olor = mapa_olor[i][j]
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{olor:.1f}", fill="black")

        # Actualizar el canvas
        self.root.update()

# Ejecutar la aplicación
visualizador = VisualizadorTableroInteractivo(tamaño=40, frame_size=800)
visualizador.root.mainloop()
