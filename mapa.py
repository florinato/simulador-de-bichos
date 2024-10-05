import numpy as np
from bicho import Bicho
from planta import Planta
from redneuronalbicho import RedNeuronalBicho


class Mapa:
    def __init__(self, tamaño, num_bichos, num_plantas, num_plantas_venenosas, num_depredadores, ciclos_regeneracion_plantas, vida_recuperada_al_comer, vida_perdida_por_ciclo, vida_inicial_bichos, rango_observacion_bichos, ciclos_reproduccion):
        self.tamaño = tamaño
        self.matriz = np.zeros((tamaño, tamaño))  # Inicializa el tablero vacío
        self.ciclos_regeneracion_plantas = ciclos_regeneracion_plantas
        self.vida_recuperada_al_comer = vida_recuperada_al_comer
        self.vida_perdida_por_ciclo = vida_perdida_por_ciclo
        self.vida_inicial_bichos = vida_inicial_bichos
        self.rango_observacion_bichos = rango_observacion_bichos  # Ajustado para que se use el parámetro
        self.ciclos_reproduccion = ciclos_reproduccion

        # Inicializar bichos, plantas y depredadores
        self.bichos = self.inicializar_bichos(num_bichos)
        self.plantas = self.inicializar_plantas(num_plantas)
        self.plantas_venenosas = self.inicializar_plantas_venenosas(num_plantas_venenosas)  # Plantas venenosas
        self.depredadores = self.generar_objetos(num_depredadores, 3)

 
    def reproducir_bicho(self,bicho):
        """Clona al bicho con mayor vida y reproduce el resto basado en este bicho."""
        if not self.bichos:  # Si no hay bichos, no hacemos nada
            return

        # Encontrar el bicho con la mayor vida
        bicho_mejor = max(self.bichos, key=lambda b: b.vida)

        for bicho in self.bichos:
            if bicho.puede_reproducirse():
                fila, col = divmod(bicho.posicion, self.tamaño)

                # Buscar una celda vacía alrededor para colocar al nuevo bicho
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nueva_fila, nueva_col = fila + dx, col + dy
                        if 0 <= nueva_fila < self.tamaño and 0 <= nueva_col < self.tamaño:
                            if self.matriz[nueva_fila][nueva_col] == 0:  # Si la casilla está libre
                                nueva_pos = nueva_fila * self.tamaño + nueva_col

                                # Clonar la red neuronal del bicho con más vida
                                red_neuronal_clonada = RedNeuronalBicho()
                                red_neuronal_clonada.pesos_entrada_oculta = np.copy(bicho_mejor.red_neuronal.pesos_entrada_oculta)
                                red_neuronal_clonada.bias_oculta = np.copy(bicho_mejor.red_neuronal.bias_oculta)
                                red_neuronal_clonada.pesos_oculta_salida = np.copy(bicho_mejor.red_neuronal.pesos_oculta_salida)
                                red_neuronal_clonada.bias_salida = np.copy(bicho_mejor.red_neuronal.bias_salida)

                                # Crear un nuevo bicho con la red neuronal clonada del mejor bicho
                                nuevo_bicho = Bicho(nueva_pos, red_neuronal_clonada, vida_inicial=self.vida_inicial_bichos, ciclos_reproduccion=self.ciclos_reproduccion)
                                self.bichos.append(nuevo_bicho)
                                self.matriz[nueva_fila][nueva_col] = 2  # Colocar el nuevo bicho en el mapa
                                print(f"Nuevo bicho en posición {nueva_pos}, clonado del bicho con {bicho_mejor.vida} de vida.")
                                break



    def inicializar_bichos(self, num_bichos):
        posiciones_bichos = self.generar_objetos(num_bichos, 2)  # Bichos representados con 2 (naranja)
        bichos = []
        for posicion in posiciones_bichos:
            red_neuronal = RedNeuronalBicho()
            bicho = Bicho(posicion, red_neuronal, self.vida_inicial_bichos, self.ciclos_reproduccion)
            bichos.append(bicho)
        return bichos

    def inicializar_plantas(self, num_plantas):
        posiciones_plantas = self.generar_objetos(num_plantas, 1)  # Plantas representadas con 1 (verde)
        plantas = []
        for posicion in posiciones_plantas:
            planta = Planta(posicion, self.ciclos_regeneracion_plantas)
            plantas.append(planta)
        return plantas
    def inicializar_plantas_venenosas(self, num_plantas_venenosas):
        posiciones_plantas_venenosas = self.generar_objetos(num_plantas_venenosas, 4)  # Plantas venenosas representadas con 4 (rojo)
        plantas_venenosas = []
        for posicion in posiciones_plantas_venenosas:
            planta_venenosa = Planta(posicion, self.ciclos_regeneracion_plantas)
            plantas_venenosas.append(planta_venenosa)
        return plantas_venenosas


    def generar_objetos(self, num_objetos, valor):
        posiciones = np.random.choice(self.tamaño * self.tamaño, num_objetos, replace=False)
        for pos in posiciones:
            fila, col = divmod(pos, self.tamaño)
            self.matriz[fila][col] = valor
        return posiciones

    def actualizar_posicion(self, bicho, direccion):
        """Actualiza la posición de un bicho basado en la dirección (ahora incluye diagonales)."""
        fila, col = divmod(bicho.posicion, self.tamaño)
        nueva_fila, nueva_col = fila, col  # Mantener la posición actual por defecto

        # Determinar la nueva posición en función de la dirección
        if direccion == 0 and fila > 0:  # Norte
            nueva_fila = fila - 1
        elif direccion == 1 and fila < self.tamaño - 1:  # Sur
            nueva_fila = fila + 1
        elif direccion == 2 and col < self.tamaño - 1:  # Este
            nueva_col = col + 1
        elif direccion == 3 and col > 0:  # Oeste
            nueva_col = col - 1
        elif direccion == 4 and fila > 0 and col < self.tamaño - 1:  # Noreste
            nueva_fila = fila - 1
            nueva_col = col + 1
        elif direccion == 5 and fila < self.tamaño - 1 and col < self.tamaño - 1:  # Sureste
            nueva_fila = fila + 1
            nueva_col = col + 1
        elif direccion == 6 and fila < self.tamaño - 1 and col > 0:  # Suroeste
            nueva_fila = fila + 1
            nueva_col = col - 1
        elif direccion == 7 and fila > 0 and col > 0:  # Noroeste
            nueva_fila = fila - 1
            nueva_col = col - 1

        # Si la nueva posición es válida, no está ocupada, y no es la misma que la anterior
        if (self.matriz[nueva_fila][nueva_col] == 0 and 
            (nueva_fila != fila or nueva_col != col) and 
            bicho.posicion_anterior != nueva_fila * self.tamaño + nueva_col):
            
            # Actualizar la posición del bicho
            self.matriz[fila][col] = 0  # Vaciar la posición anterior
            self.matriz[nueva_fila][nueva_col] = 2  # Colocar el bicho en la nueva posición
            bicho.actualizar_posicion(nueva_fila * self.tamaño + nueva_col)  # Actualizar la posición del bicho
        else:
            # Evitar que el bicho quede atrapado si no puede moverse, eligiendo una dirección diferente
            direcciones_validas = []
            if fila > 0 and self.matriz[fila - 1][col] == 0 and bicho.posicion_anterior != (fila - 1) * self.tamaño + col:
                direcciones_validas.append(0)  # Norte
            if fila < self.tamaño - 1 and self.matriz[fila + 1][col] == 0 and bicho.posicion_anterior != (fila + 1) * self.tamaño + col:
                direcciones_validas.append(1)  # Sur
            if col < self.tamaño - 1 and self.matriz[fila][col + 1] == 0 and bicho.posicion_anterior != fila * self.tamaño + (col + 1):
                direcciones_validas.append(2)  # Este
            if col > 0 and self.matriz[fila][col - 1] == 0 and bicho.posicion_anterior != fila * self.tamaño + (col - 1):
                direcciones_validas.append(3)  # Oeste
            if fila > 0 and col < self.tamaño - 1 and self.matriz[fila - 1][col + 1] == 0 and bicho.posicion_anterior != (fila - 1) * self.tamaño + (col + 1):
                direcciones_validas.append(4)  # Noreste
            if fila < self.tamaño - 1 and col < self.tamaño - 1 and self.matriz[fila + 1][col + 1] == 0 and bicho.posicion_anterior != (fila + 1) * self.tamaño + (col + 1):
                direcciones_validas.append(5)  # Sureste
            if fila < self.tamaño - 1 and col > 0 and self.matriz[fila + 1][col - 1] == 0 and bicho.posicion_anterior != (fila + 1) * self.tamaño + (col - 1):
                direcciones_validas.append(6)  # Suroeste
            if fila > 0 and col > 0 and self.matriz[fila - 1][col - 1] == 0 and bicho.posicion_anterior != (fila - 1) * self.tamaño + (col - 1):
                direcciones_validas.append(7)  # Noroeste

            if direcciones_validas:
                nueva_direccion = np.random.choice(direcciones_validas)
                self.actualizar_posicion(bicho, nueva_direccion)  # Llamada recursiva solo si hay dirección válida



    def eliminar_planta(self, posicion):
        """Elimina una planta de la posición dada si está activa."""
        for planta in self.plantas:
            if planta.posicion == posicion and planta.activa:
                planta.activa = False
                fila, col = divmod(planta.posicion, self.tamaño)
                self.matriz[fila, col] = 0  # Eliminar la planta del tablero
                planta.ciclos_para_regenerar = self.ciclos_regeneracion_plantas  # Reiniciar el ciclo de regeneración
                
                break

    def regenerar_plantas(self):
        """Regenera las plantas desactivadas si su contador de regeneración llega a cero."""
        for planta in self.plantas:
            if not planta.activa:
                planta.ciclos_para_regenerar -= 1  # Disminuir los ciclos restantes
                if planta.ciclos_para_regenerar <= 0:
                    fila, col = divmod(planta.posicion, self.tamaño)
                    self.matriz[fila, col] = 1  # Restaurar la planta en el tablero
                    planta.activa = True  # Reactivar la planta
                    
    def bicho_come(self, bicho):
        """El bicho come si encuentra una planta normal y pierde vida si toca una planta venenosa."""
        fila, col = divmod(bicho.posicion, self.tamaño)
        # Verificar los 8 cuadros que rodean al bicho (incluyendo el cuadro actual)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nueva_fila, nueva_col = fila + dx, col + dy
                if 0 <= nueva_fila < self.tamaño and 0 <= nueva_col < self.tamaño:
                    if self.matriz[nueva_fila][nueva_col] == 1:  # Si hay una planta normal
                        bicho.aumentar_vida(self.vida_recuperada_al_comer)  # Aumenta la vida al comer
                        self.eliminar_planta(nueva_fila * self.tamaño + nueva_col)  # Elimina la planta
                        break  # Solo come una planta por ciclo
                    elif self.matriz[nueva_fila][nueva_col] == 4:  # Si hay una planta venenosa
                        bicho.reducir_vida(100)  # Reduce la vida en 100 al tocar una planta venenosa
                        print(f"Bicho envenenado en {nueva_fila},{nueva_col}, vida restante: {bicho.vida}")
                        break  # Solo recibe daño por una planta venenosa por ciclo

    def ejecutar_ciclo(self):
        """Ejecuta un ciclo de vida para todos los bichos."""
        for bicho in self.bichos[:]:
            bicho.reducir_vida(self.vida_perdida_por_ciclo)  # Reducir la vida de cada bicho en cada ciclo
            bicho.incrementar_contador_reproduccion()  # Incrementar el contador de reproducción

            if bicho.esta_muerto():
                # Eliminar el bicho si su vida llega a cero
                fila, col = divmod(bicho.posicion, self.tamaño)
                self.matriz[fila][col] = 0  # Eliminar el bicho del tablero
                self.bichos.remove(bicho)
                continue

            # Obtener entradas de la red neuronal y tomar decisión
            entradas = self.obtener_parametros_bicho(bicho)
            decision = bicho.red_neuronal.tomar_decision(entradas)
            direccion = np.argmax(decision)  # Obtener la dirección con la mayor probabilidad

            # Ajustar pesos con la tasa basada en la vida
            bicho.red_neuronal.ajustar_pesos_con_tasa(bicho)

            # Actualizar la posición del bicho
            self.actualizar_posicion(bicho, direccion)

            # Verificar si el bicho puede reproducirse
            if bicho.puede_reproducirse():
                self.reproducir_bicho(bicho)
                bicho.contador_reproduccion = 0  # Reiniciar el contador de reproducción

            # Verificar si el bicho puede comer
            self.bicho_come(bicho)

        # Regenerar plantas después de los ciclos
        self.regenerar_plantas()

    def obtener_parametros_bicho(self, bicho):
        """Obtiene las diferencias de olores (comida y veneno) en las 8 direcciones alrededor del bicho y su nivel de vida."""
        fila, col = divmod(bicho.posicion, self.tamaño)
        diferencias_olores = []

        # Ocho direcciones: [Norte, Noreste, Este, Sureste, Sur, Suroeste, Oeste, Noroeste]
        direcciones = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        
        # Obtener el olor (comida) y veneno en la celda actual
        olor_actual = self.calcular_olor_celda(fila, col)
        veneno_actual = self.calcular_veneno_celda(fila, col)

        for dx, dy in direcciones:
            nueva_fila, nueva_col = fila + dx, col + dy
            if 0 <= nueva_fila < self.tamaño and 0 <= nueva_col < self.tamaño:
                # Calcular las diferencias de olor (comida) y veneno con las celdas adyacentes
                olor_adyacente = self.calcular_olor_celda(nueva_fila, nueva_col)
                veneno_adyacente = self.calcular_veneno_celda(nueva_fila, nueva_col)

                diferencia_olor = olor_actual - olor_adyacente  # Comida
                diferencia_veneno = veneno_adyacente - veneno_actual  # Veneno (inverso)

                diferencias_olores.append(diferencia_olor)  # Añadir diferencia de olor (comida)
                diferencias_olores.append(diferencia_veneno)  # Añadir diferencia de veneno
            else:
                diferencias_olores.append(0)  # Si está fuera del rango del tablero
                diferencias_olores.append(0)  # Añadir valor cero para el veneno

        # Añadir la vida del bicho como una entrada adicional
        diferencias_olores.append(bicho.vida / self.vida_inicial_bichos)  # Normalizar la vida del bicho para que esté entre 0 y 1

        # Retornar las diferencias de los olores (comida, veneno) más la vida
        return np.array(diferencias_olores)

    def calcular_olor_celda(self, fila, col):
        """Calcula el valor de olor (comida) en una celda específica en función de la distancia a las plantas."""
        suma_olor = 0
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                if self.matriz[i, j] == 1:  # Si hay una planta (comida)
                    distancia = np.sqrt((fila - i) ** 2 + (col - j) ** 2) + 1  # Distancia euclidiana
                    suma_olor += 10 / distancia
        return round(suma_olor, 1)  # Redondear a 1 decimal

    def calcular_veneno_celda(self, fila, col):
        """Calcula el valor de veneno en una celda específica en función de la distancia a las plantas venenosas."""
        suma_veneno = 0
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                if self.matriz[i, j] == 2:  # Si hay una planta venenosa (valor 2)
                    distancia = np.sqrt((fila - i) ** 2 + (col - j) ** 2) + 1  # Distancia euclidiana
                    suma_veneno += 10 / distancia
        return round(suma_veneno, 1)  # Redondear a 1 decimal


