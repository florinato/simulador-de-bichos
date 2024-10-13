import numpy as np


class RedNeuronalBicho:
    def __init__(self):
        # 9 entradas (8 para cada una de las direcciones alrededor del bicho y 1 para la vida)
        self.entradas_size = 17
        self.ocultas_size = 50 # Neuronas ocultas (ajustable)
        self.salidas_size = 8   # 8 salidas (una para cada dirección)
        
        # Inicialización de los pesos y bias
        self.pesos_entrada_oculta = np.random.randn(self.entradas_size, self.ocultas_size)
        self.bias_oculta = np.random.randn(self.ocultas_size)
        
        self.pesos_oculta_salida = np.random.randn(self.ocultas_size, self.salidas_size)
        self.bias_salida = np.random.randn(self.salidas_size)

    def tomar_decision(self, entradas):
        """Tomar una decisión basada en los olores y la vida."""
        # Capa de entrada -> capa oculta
        z_oculta = np.dot(entradas, self.pesos_entrada_oculta) + self.bias_oculta
        a_oculta = self.activacion_relu(z_oculta)
        
        # Capa oculta -> capa de salida
        z_salida = np.dot(a_oculta, self.pesos_oculta_salida) + self.bias_salida
        a_salida = self.activacion_softmax(z_salida)
        
        # Retorna las probabilidades de moverse en cada dirección
        return a_salida

    def activacion_relu(self, x):
        return np.maximum(0, x)
    
    def activacion_softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()
    def clonar(self):
            clon = RedNeuronalBicho()
            clon.pesos_entrada_oculta = np.copy(self.pesos_entrada_oculta)
            clon.bias_oculta = np.copy(self.bias_oculta)
            clon.pesos_oculta_salida = np.copy(self.pesos_oculta_salida)
            clon.bias_salida = np.copy(self.bias_salida)
            return clon