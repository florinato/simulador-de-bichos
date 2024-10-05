
# Simulador de Bichos 🐛

**Simulador de Bichos** es un proyecto de simulación basado en inteligencia artificial (IA) que recrea el comportamiento de pequeñas criaturas virtuales llamadas "bichos". El objetivo principal es que estos bichos sobrevivan en un ecosistema artificial, buscando comida, evitando plantas venenosas y aprendiendo a tomar decisiones eficientes para maximizar su vida y reproducirse. La simulación implementa redes neuronales simples que les permiten a los bichos tomar decisiones basadas en su entorno y en su e...

## Características del proyecto

- **Simulación en tiempo real**: El proyecto visualiza un ecosistema donde los bichos se mueven, se alimentan y se reproducen.
- **Red neuronal adaptativa**: Los bichos usan una red neuronal básica para aprender a tomar decisiones, como moverse hacia la comida o evitar plantas venenosas.
- **Plantas venenosas**: Introducción de plantas rojas que restan vida a los bichos si entran en contacto con ellas.
- **Clonación inteligente**: Los bichos más fuertes, con más vida, tienen mayores probabilidades de ser clonados durante la reproducción.
- **Aprendizaje evolutivo**: Los bichos que sobreviven más tiempo aprenden a optimizar su comportamiento y, con el tiempo, el sistema evoluciona para que se tomen decisiones más inteligentes.

## Cómo funciona

### Mapa y Ecosistema

El ecosistema está representado por una matriz que define las posiciones de los bichos, las plantas (tanto normales como venenosas) y el espacio vacío. Cada bicho puede moverse en 8 direcciones (norte, sur, este, oeste, y sus respectivas diagonales) en busca de comida. Su objetivo es consumir plantas para recuperar vida y evitar plantas venenosas.

### Redes Neuronales

Cada bicho está equipado con una red neuronal básica que tiene entradas como:

- **Gradiente de comida**: Detecta si una planta está cerca y calcula la mejor dirección hacia ella.
- **Gradiente de veneno**: Detecta si hay plantas venenosas cercanas y toma decisiones para evitarlas.
- **Nivel de vida**: Los bichos consideran su nivel de vida para tomar decisiones sobre si comer o huir.
  
Estas entradas se procesan en una capa oculta, y finalmente, la red toma una decisión sobre en qué dirección moverse.

### Reproducción y Clonación

Cuando los bichos alcanzan un cierto ciclo de vida, pueden reproducirse. El bicho con más vida dentro de la simulación tiene la mayor probabilidad de clonar su red neuronal, lo que permite que los "hijos" hereden las habilidades y comportamientos más exitosos.

## Requisitos del sistema

Este proyecto está desarrollado en Python y utiliza las siguientes bibliotecas:

- `numpy`: Para operaciones matemáticas eficientes.
- `tkinter`: Para visualización gráfica.
- `pickle`: Para guardar y cargar modelos de redes neuronales entrenadas.

## Instalación y uso

### 1. Clonar el repositorio:

```bash
git clone https://github.com/florinato/simulador-de-bichos.git
cd simulador-de-bichos
```

### 2. Instalar las dependencias:

```bash
pip install numpy
```

### 3. Ejecutar el simulador:

```bash
python src2/main.py
```

### 4. Guardar y cargar modelos

El proyecto incluye un sistema para guardar la red neuronal entrenada en un archivo `.pkl` usando la clase `ModeloManager`. El modelo se guarda automáticamente cada 1000 ciclos y se carga al iniciar la simulación si existe un modelo previamente entrenado.

## Contribuir

Este proyecto está en constante desarrollo. ¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la simulación, optimizar las redes neuronales o agregar nuevas funcionalidades, no dudes en hacer un pull request.

## Licencia

Este proyecto está licenciado bajo la MIT License.

---

## Ideas futuras

Algunas ideas para futuras mejoras:

- **Depredadores**: Añadir criaturas depredadoras que cazan a los bichos para aumentar la dificultad.
- **Sensores adicionales**: Incluir otros estímulos como la temperatura o el nivel de hambre para tomar decisiones más complejas.
- **Mutación genética**: Implementar mutaciones aleatorias en las redes neuronales durante la reproducción para simular la evolución.
