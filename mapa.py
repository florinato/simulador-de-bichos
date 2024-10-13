import numpy as np
from bicho import Bicho
from planta import Planta
from redneuronalbicho import RedNeuronalBicho


class Mapa:
    def __init__(self, tamaño, num_bichos, num_plantas, num_plantas_venenosas,
                 num_depredadores, ciclos_regeneracion_plantas,
                 vida_recuperada_al_comer, vida_perdida_por_ciclo,
                 vida_inicial_bichos, rango_observacion_bichos, ciclos_reproduccion,
                 vida_perdida_por_veneno):  # Agregado el nuevo parámetro
        self.tamaño = tamaño
        self.matriz = np.zeros((tamaño, tamaño))
        self.ciclos_regeneracion_plantas = ciclos_regeneracion_plantas
        self.vida_recuperada_al_comer = vida_recuperada_al_comer
        self.vida_perdida_por_ciclo = vida_perdida_por_ciclo
        self.vida_inicial_bichos = vida_inicial_bichos
        self.rango_observacion_bichos = rango_observacion_bichos
        self.ciclos_reproduccion = ciclos_reproduccion
        self.vida_perdida_por_veneno = vida_perdida_por_veneno 
        
        self.bichos = self.inicializar_bichos(num_bichos)
        self.plantas = self.inicializar_plantas(num_plantas)
        self.plantas_venenosas = self.inicializar_plantas_venenosas(num_plantas_venenosas)
        self.depredadores = self.generar_objetos(num_depredadores, 3)

    def inicializar_bichos(self, num_bichos):
        posiciones_bichos = self.generar_objetos(num_bichos, 2)
        bichos = []
        for posicion in posiciones_bichos:
            red_neuronal = RedNeuronalBicho()
            bicho = Bicho(posicion, red_neuronal, self.vida_inicial_bichos, self.ciclos_reproduccion)
            bichos.append(bicho)
        return bichos

    def inicializar_plantas(self, num_plantas):
        posiciones_plantas = self.generar_objetos(num_plantas, 1)
        plantas = []
        for posicion in posiciones_plantas:
            planta = Planta(posicion, self.ciclos_regeneracion_plantas)
            plantas.append(planta)
        return plantas

    def inicializar_plantas_venenosas(self, num_plantas_venenosas):
        posiciones_plantas_venenosas = self.generar_objetos(num_plantas_venenosas, 4)
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

    def ejecutar_ciclo(self):
        """Ejecuta un ciclo para todos los bichos."""
        for bicho in self.bichos[:]:
            bicho.reducir_vida(self.vida_perdida_por_ciclo)
            bicho.incrementar_contador_reproduccion()

            if bicho.esta_muerto():
                fila, col = divmod(bicho.posicion, self.tamaño)
                self.matriz[fila][col] = 0
                self.bichos.remove(bicho)
                continue

            bicho.mover(self)
            bicho.comer(self)
            bicho.reproducirse(self)

        # Regenerar plantas
        for planta in self.plantas:
            planta.regenerar(self)

    def eliminar_planta(self, posicion):
        """Elimina una planta en una posición dada."""
        for planta in self.plantas:
            if planta.posicion == posicion:
                planta.eliminar(self)
                break

    def calcular_olor_celda(self, fila, col):
        """Calcula el olor de comida en una celda específica."""
        suma_olor = 0
        for planta in self.plantas:
            if planta.activa:
                i, j = divmod(planta.posicion, self.tamaño)
                distancia = np.sqrt((fila - i) ** 2 + (col - j) ** 2) + 1
                suma_olor += 30 / distancia
        return round(suma_olor, 1)

    def calcular_veneno_celda(self, fila, col):
        """Calcula el veneno en una celda específica."""
        suma_veneno = 0
        for planta in self.plantas_venenosas:
            if planta.activa:
                i, j = divmod(planta.posicion, self.tamaño)
                distancia = np.sqrt((fila - i) ** 2 + (col - j) ** 2) + 1
                suma_veneno += 30 / distancia
        return round(suma_veneno, 1)

