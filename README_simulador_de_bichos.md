# Simulador de Bichos 🐛

**Simulador de Bichos** es un proyecto de simulación basado en inteligencia artificial (IA) que recrea el comportamiento de pequeñas criaturas virtuales llamadas "bichos". El objetivo principal es que estos bichos sobrevivan en un ecosistema artificial, buscando comida, evitando plantas venenosas y aprendiendo a tomar decisiones eficientes para maximizar su vida y reproducirse. La simulación implementa redes neuronales simples que les permiten a los bichos tomar decisiones basadas en su entorno y en su perce...

## Características del proyecto
- **Simulación en tiempo real**: El proyecto visualiza un ecosistema donde los bichos se mueven, se alimentan y se reproducen.
- **Red neuronal adaptativa**: Los bichos usan una red neuronal básica para aprender a tomar decisiones, como moverse hacia la comida o evitar plantas venenosas.
- **Plantas venenosas**: Introducción de plantas rojas que restan vida a los bichos si entran en contacto con ellas.
- **Clonación inteligente**: Los bichos más fuertes, con más vida, tienen mayores probabilidades de ser clonados durante la reproducción.
- **Aprendizaje evolutivo**: Los bichos que sobreviven más tiempo aprenden a optimizar su comportamiento y, con el tiempo, el sistema evoluciona para que tomen decisiones más inteligentes.

## Cómo funciona
### Mapa y Ecosistema
El ecosistema está representado por una matriz que define las posiciones de los bichos, las plantas (tanto normales como venenosas) y el espacio vacío. Cada bicho puede moverse en 8 direcciones (norte, sur, este, oeste, y sus respectivas diagonales) en busca de comida. Su objetivo es consumir plantas para recuperar vida y evitar plantas venenosas.

### Percepción y Seguimiento de Rastro de Olor
Cada bicho posee un rango de visión limitado que determina el área en la que puede percibir su entorno. Dentro de este rango, los bichos calculan los gradientes de olor generados por las plantas. Estos gradientes son valores que representan la concentración de olores de comida y veneno en cada dirección relativa al bicho.

### Cálculo de Gradientes de Olor
1. **Definición del Rango de Visión**: Cada bicho tiene un rango de visión definido que determina la distancia máxima a la que puede detectar plantas. Este rango se representa como un área circular alrededor de la posición actual del bicho en el mapa.
2. **Detección de Plantas**: Dentro de este rango, cada bicho detecta la presencia de plantas normales (fuentes de alimento) y plantas venenosas (fuentes de peligro).
3. **Cálculo de Intensidad de Olores**:

   La intensidad del olor de cada planta se calcula inversamente proporcional a la distancia entre el bicho y la planta:

   `Intensidad del olor = 10 / (distancia + 1)`

   Donde "10" es una constante que define la fuerza del olor y "1" se añade para evitar la división por cero cuando la distancia es cero.

4. **Generación del Mapa de Olores**:
   - Para cada celda dentro del rango de visión, se suma la intensidad de los olores provenientes de las plantas, ponderados por la distancia.
   - El mapa de olores es una representación bidimensional que indica la concentración de olores de comida y veneno en cada celda dentro del rango de visión del bicho.
   - Este mapa permite al bicho evaluar la diferencia de olores entre su posición actual y las celdas adyacentes, facilitando la toma de decisiones sobre hacia dónde moverse.

### Seguimiento del Rastro de Olor
1. **Cálculo de Diferencias de Olores**:
   - El modelo recibe como entradas la diferencia entre la lectura de cada celda potencial en su rango de visión y la lectura de la celda en la que se encuentra actualmente:

     `Diferencia de olor = Olor de la celda potencial - Olor de la celda actual`

   - Estas diferencias indican si una celda adyacente tiene una mayor concentración de comida o veneno en comparación con la posición actual del bicho.

2. **Procesamiento por la Red Neuronal**:
   - Las diferencias de olores (tanto de comida como de veneno) y el nivel de vida del bicho son las entradas para la red neuronal.
   - La red neuronal procesa estas entradas y genera una salida que representa la dirección en la que el bicho debe moverse.

3. **Decisión de Movimiento**:
   - **Moverse hacia la Comida**: Si la red neuronal detecta una mayor concentración de olor de comida en una dirección específica, el bicho tenderá a moverse hacia esa dirección para encontrar alimento y recuperar vida.
   - **Evitar el Venenoso**: Si se detecta una alta concentración de olor de veneno en una dirección, el bicho tomará la decisión de evitar esa dirección para reducir el riesgo de envenenamiento.

4. **Movimiento Inteligente**:
   - Basándose en las decisiones de la red neuronal, el bicho actualiza su posición en el mapa, moviéndose hacia áreas con mayor concentración de comida y alejándose de áreas peligrosas.

## Redes Neuronales
Cada bicho está equipado con una red neuronal básica que tiene entradas como:

- **Gradiente de comida**: Detecta si una planta está cerca y calcula la mejor dirección hacia ella.
- **Gradiente de veneno**: Detecta si hay plantas venenosas cercanas y toma decisiones para evitarlas.
- **Nivel de vida**: Los bichos consideran su nivel de vida para tomar decisiones sobre si comer o huir.

Estas entradas se procesan en una capa oculta, y finalmente, la red toma una decisión sobre en qué dirección moverse.

## Reproducción y Clonación
Cuando los bichos alcanzan un cierto ciclo de vida, pueden reproducirse. El bicho con más vida dentro de la simulación tiene la mayor probabilidad de clonar su red neuronal, lo que permite que los "hijos" hereden las habilidades y comportamientos más exitosos.

## Requisitos del sistema
Este proyecto está desarrollado en Python y utiliza las siguientes bibliotecas:

- **numpy**: Para operaciones matemáticas eficientes.
- **tkinter**: Para visualización gráfica.
- **pickle**: Para guardar y cargar modelos de redes neuronales entrenadas.

## Instalación y uso
1. Clonar el repositorio:

`git clone https://github.com/florinato/simulador-de-bichos.git`

2. Instalar las dependencias:


      pip install numpy

      pip install tkinter

      pip install pickle

3. Ejecutar el simulador:


      cd simulador-de-bichos
      
      python main.py


4. Guardar y cargar modelos
- El proyecto incluye un sistema para guardar la red neuronal entrenada en un archivo .pkl usando la clase `ModeloManager`. El modelo se guarda automáticamente cada 1000 ciclos y se carga al iniciar la simulación si existe un modelo previamente entrenado.

## Contribuir
Este proyecto está en constante desarrollo. ¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la simulación, optimizar las redes neuronales o agregar nuevas funcionalidades, no dudes en hacer un pull request.

## Licencia
Este proyecto está licenciado bajo la MIT License.

## Ideas futuras
- **Depredadores**: Añadir criaturas depredadoras que cazan a los bichos para aumentar la dificultad.
- **Sensores adicionales**: Incluir otros estímulos como la temperatura o el nivel de hambre para tomar decisiones más complejas.
- **Mutación genética**: Implementar mutaciones aleatorias en las redes neuronales durante la reproducción para simular la evolución.

---

## Contacto
Para cualquier duda o sugerencia, por favor, contacta a:

- **Nombre**: Oscar Quintana
- **Email**: ranciomano@gmail.com
- **GitHub**: [GitHub](https://github.com/florinato)

## Conclusión
El Simulador de Bichos es una herramienta fascinante para explorar conceptos de inteligencia artificial, comportamiento autónomo y dinámica de ecosistemas. Al implementar gradientes de olor y permitir que los bichos sigan rastros de olor, se crea un entorno donde las criaturas virtuales pueden interactuar de manera inteligente y adaptativa, simulando procesos de supervivencia y evolución natural.
"""
