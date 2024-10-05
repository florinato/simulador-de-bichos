class Bicho:
    def __init__(self, posicion, red_neuronal, vida_inicial=10, ciclos_reproduccion=50):
        self.posicion = posicion
        self.posicion_anterior = None  # Guardar la posición anterior
        self.red_neuronal = red_neuronal
        self.vida = vida_inicial
        self.ciclos_reproduccion = ciclos_reproduccion  # Parámetro ajustable
        self.contador_reproduccion = 0  # Contador de ciclos para la reproducción
        self.olor_anterior = None  # Atributo para guardar el olor anterior

    def reducir_vida(self, cantidad):
        self.vida -= cantidad

    def aumentar_vida(self, cantidad):
        self.vida += cantidad

    def esta_muerto(self):
        return self.vida <= 0

    def incrementar_contador_reproduccion(self):
        self.contador_reproduccion += 1

    def puede_reproducirse(self):
        # Verificar si ha llegado al ciclo de reproducción
        return self.contador_reproduccion >= self.ciclos_reproduccion

    def actualizar_posicion(self, nueva_posicion):
        """Actualizar la posición del bicho y guardar la posición anterior."""
        self.posicion_anterior = self.posicion
        self.posicion = nueva_posicion

    def actualizar_olor_anterior(self, olor_actual):
        """Actualiza el valor del olor anterior con el olor actual."""
        self.olor_anterior = olor_actual

