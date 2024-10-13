import numpy as np


class Bicho:
    def __init__(self, posicion, red_neuronal, vida_inicial, ciclos_reproduccion):
        self.posicion = posicion
        self.posicion_anterior = None  # Guardar la posición anterior
        self.red_neuronal = red_neuronal
        self.vida = vida_inicial
        self.ciclos_reproduccion = ciclos_reproduccion
        self.contador_reproduccion = 0
        self.olor_anterior = None

    def reducir_vida(self, cantidad):
        self.vida -= cantidad

    def aumentar_vida(self, cantidad):
        self.vida += cantidad

    def esta_muerto(self):
        return self.vida <= 0

    def incrementar_contador_reproduccion(self):
        self.contador_reproduccion += 1

    def puede_reproducirse(self):
        return self.contador_reproduccion >= self.ciclos_reproduccion

    def actualizar_posicion(self, nueva_posicion):
        self.posicion_anterior = self.posicion
        self.posicion = nueva_posicion

    def actualizar_olor_anterior(self, olor_actual):
        self.olor_anterior = olor_actual

    def mover(self, mapa):
        """Decide a dónde moverse y actualiza su posición en el mapa."""
        entradas = self.obtener_parametros(mapa)
        decision = self.red_neuronal.tomar_decision(entradas)

        # Obtener una lista de direcciones ordenadas por la probabilidad (mayor primero)
        direcciones_sorted = np.argsort(decision)[::-1]  # Descendente

        # Mapeo de direcciones a desplazamientos (dx, dy)
        direcciones_mapping = {
            0: (-1, 0),   # Norte
            1: (1, 0),    # Sur
            2: (0, 1),    # Este
            3: (0, -1),   # Oeste
            4: (-1, 1),   # Noreste
            5: (1, 1),    # Sureste
            6: (1, -1),   # Suroeste
            7: (-1, -1)   # Noroeste
        }

        fila, col = divmod(self.posicion, mapa.tamaño)

        for direccion in direcciones_sorted:
            dx, dy = direcciones_mapping[direccion]

            # Calcular nueva posición con wrap-around
            nueva_fila = (fila + dx) % mapa.tamaño
            nueva_col = (col + dy) % mapa.tamaño
            nueva_posicion = nueva_fila * mapa.tamaño + nueva_col

            # Verificar si la nueva posición está libre y no es la posición anterior
            if (mapa.matriz[nueva_fila][nueva_col] == 0 and
                self.posicion_anterior != nueva_posicion):

                # Actualizar el mapa
                mapa.matriz[fila][col] = 0  # Vaciar la posición anterior
                mapa.matriz[nueva_fila][nueva_col] = 2  # Colocar el bicho en la nueva posición

                # Actualizar la posición del bicho
                self.actualizar_posicion(nueva_posicion)

                
                break  # Movimiento realizado, salir del loop
        else:
            # Si no se pudo mover a ninguna dirección, el bicho se queda en su lugar
            print("Bicho no pudo moverse, se queda en su posición")



    def comer(self, mapa):
        """El bicho come si encuentra comida cercana."""
        fila, col = divmod(self.posicion, mapa.tamaño)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nueva_fila, nueva_col = fila + dx, col + dy
                if 0 <= nueva_fila < mapa.tamaño and 0 <= nueva_col < mapa.tamaño:
                    if mapa.matriz[nueva_fila][nueva_col] == 1:  # Planta normal
                        self.aumentar_vida(mapa.vida_recuperada_al_comer)
                        mapa.eliminar_planta(nueva_fila * mapa.tamaño + nueva_col)
                        break
                    elif mapa.matriz[nueva_fila][nueva_col] == 4:  # Planta venenosa
                        self.reducir_vida(mapa.vida_perdida_por_veneno)  # Usar el parámetro
                        print(f"Bicho envenenado en {nueva_fila},{nueva_col}, vida restante: {self.vida}")
                        break

    def reproducirse(self, mapa):
        """El bicho se reproduce si se cumplen las condiciones."""
        if self.puede_reproducirse():
            fila, col = divmod(self.posicion, mapa.tamaño)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nueva_fila, nueva_col = fila + dx, col + dy
                    if 0 <= nueva_fila < mapa.tamaño and 0 <= nueva_col < mapa.tamaño:
                        if mapa.matriz[nueva_fila][nueva_col] == 0:
                            nueva_pos = nueva_fila * mapa.tamaño + nueva_col
                            red_neuronal_clonada = self.red_neuronal.clonar()
                            nuevo_bicho = Bicho(nueva_pos, red_neuronal_clonada,
                                                vida_inicial=mapa.vida_inicial_bichos,
                                                ciclos_reproduccion=mapa.ciclos_reproduccion)
                            mapa.bichos.append(nuevo_bicho)
                            mapa.matriz[nueva_fila][nueva_col] = 2
                            print(f"Nuevo bicho en posición {nueva_pos}, clonado del bicho con {self.vida} de vida.")
                            self.contador_reproduccion = 0  # Reiniciar el contador
                            break

    def obtener_parametros(self, mapa):
        """Obtiene los parámetros para la toma de decisiones con mapa toroidal."""
        fila, col = divmod(self.posicion, mapa.tamaño)
        diferencias_olores = []
        direcciones = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                    (1, 0), (1, -1), (0, -1), (-1, -1)]
        olor_actual = mapa.calcular_olor_celda(fila, col)
        veneno_actual = mapa.calcular_veneno_celda(fila, col)

        for dx, dy in direcciones:
            nueva_fila = (fila + dx) % mapa.tamaño
            nueva_col = (col + dy) % mapa.tamaño
            olor_adyacente = mapa.calcular_olor_celda(nueva_fila, nueva_col)
            veneno_adyacente = mapa.calcular_veneno_celda(nueva_fila, nueva_col)
            diferencia_olor = olor_actual - olor_adyacente
            diferencia_veneno = veneno_adyacente - veneno_actual
            diferencias_olores.extend([diferencia_olor, diferencia_veneno])
        
        diferencias_olores.append(self.vida / mapa.vida_inicial_bichos)
        return np.array(diferencias_olores)

