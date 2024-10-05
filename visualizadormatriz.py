import tkinter as tk


class VisualizadorMatriz:
    def __init__(self, frame_size):
        self.frame_size = frame_size  # Tamaño total del frame en píxeles
        self.root = tk.Tk()  # Crear ventana de Tkinter
        self.root.title("Simulación de bichos")
        
        # Fijar el tamaño de la ventana para que coincida con el frame_size
        self.root.geometry(f"{self.frame_size}x{self.frame_size}")

        # Configurar el canvas con el tamaño especificado
        self.canvas = tk.Canvas(self.root, width=self.frame_size, height=self.frame_size)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Expande el canvas para ajustarse al tamaño de la ventana

        # Configurar el redimensionamiento del canvas cuando se cambia el tamaño de la ventana
        self.canvas.bind("<Configure>", self.redimensionar_canvas)

    def redimensionar_canvas(self, event):
        # Redimensionar el canvas cuando cambia el tamaño de la ventana
        self.canvas.config(width=event.width, height=event.height)
        self.frame_size = min(event.width, event.height)  # Mantener un frame cuadrado
    def dibujar(self, matriz):
        # Obtener el tamaño de la cuadrícula desde la matriz
        filas, columnas = len(matriz), len(matriz[0])
        
        # Calcular el tamaño de cada celda basado en el tamaño actual del canvas
        cell_width = self.frame_size // columnas
        cell_height = self.frame_size // filas

        # Limpiar el canvas antes de dibujar la nueva matriz
        self.canvas.delete("all")

        # Dibujar las celdas
        for i in range(filas):
            for j in range(columnas):
                x1 = j * cell_width
                y1 = i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                # Determinar el color según los valores en la matriz
                if matriz[i][j] == 1:  # Si es una planta (verde)
                    color = '#90EE90'  # Verde claro
                elif matriz[i][j] == 2:  # Si es un bicho (naranja)
                    color = '#FFA500'  # Naranja para los bichos
                elif matriz[i][j] == 4:  # Si es una planta venenosa (rojo)
                    color = '#FF4500'  # Rojo para las plantas venenosas
                else:
                    color = 'white'  # Blanco para celdas vacías
                
                # Dibujar el rectángulo en la celda correspondiente
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")


        self.root.update()



