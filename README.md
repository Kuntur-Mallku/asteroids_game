# Asteroids Game 🚀

Un juego de Asteroids desarrollado en Python con Pygame, con mecánicas de progresión de dificultad y sistema de puntuación avanzado.

## 🎮 Características del Juego

- **Sistema completo de menús** con pantalla de inicio y game over
- **Movimiento realista de nave espacial** con rotación y propulsión
- **Rocas con física realista** - diferentes tamaños, rotación continua y spawning aleatorio
- **Sistema de progresión de dificultad** - velocidad de rocas aumenta con el tiempo
- **Sistema de puntuación avanzado** con estadísticas detalladas
- **Colisiones precisas** entre balas, rocas y nave
- **Estados de juego** - Start, Playing, Game Over
- **UI informativa** con estadísticas en tiempo real
- **Botones interactivos** para iniciar y reiniciar el juego

## 🎯 Controles

- **Click en PLAY**: Iniciar/Reiniciar juego
- **P**: Iniciar/Reiniciar juego (teclado)
- **Flechas Izquierda/Derecha**: Rotar la nave
- **Flecha Arriba**: Propulsión hacia adelante
- **Flecha Abajo**: Propulsión hacia atrás
- **Barra Espaciadora**: Disparar (solo durante el juego)
- **Q**: Salir del juego

## 📁 Estructura del Proyecto

```
asteroids/
├── asteroids.py        # Archivo principal del juego
├── settings.py         # Configuraciones del juego
├── ship.py            # Clase de la nave espacial
├── bullet.py          # Clase de las balas
├── rock.py            # Clase de las rocas/asteroides
├── game_stats.py      # Manejo de estadísticas del juego
├── scoreboard.py      # UI y visualización de puntuaciones
├── button.py          # Sistema de botones y pantallas
├── images/            # Recursos gráficos
│   ├── fighter.png    # Imagen de la nave
│   ├── rock1.png      # Imagen de roca tipo 1
│   └── rock2.png      # Imagen de roca tipo 2
└── README.md          # Este archivo
```

## 🛠️ Instalación y Ejecución

1. **Requisitos previos:**
   ```bash
   pip install pygame
   ```

2. **Ejecutar el juego:**
   ```bash
   python asteroids.py
   ```

## 🎮 Mecánicas del Juego

### Estados del Juego
- **Pantalla de Inicio**: Muestra título, instrucciones y botón PLAY
- **Juego Activo**: Nave se mueve, rocas aparecen, colisiones detectadas
- **Game Over**: Muestra estadísticas finales y botón PLAY AGAIN

### Sistema de Colisiones
- **Balas vs Rocas**: Destruye rocas y suma puntos
- **Nave vs Rocas**: Termina el juego y muestra estadísticas finales

### Sistema de Dificultad
- Cada 30 segundos aumenta el nivel de dificultad
- Las rocas se mueven más rápido en niveles superiores
- Más puntos por roca destruida en niveles altos

### Sistema de Puntuación
- **Puntos base**: 10 puntos por roca
- **Multiplicador**: Puntos × (Nivel de dificultad)
- **Estadísticas**: Precisión, balas disparadas, tiempo de supervivencia

### Características de las Rocas
- **Spawning aleatorio**: Aparecen desde cualquier borde de la pantalla
- **Tamaños variables**: 60%-140% para rock1, 40%-80% para rock2
- **Rotación realista**: Giran mientras se mueven por el espacio
- **Direcciones inteligentes**: Se dirigen hacia el centro de la pantalla

## 🔧 Configuración

Las configuraciones del juego se pueden modificar en `settings.py`:

```python
# Velocidad de rocas
base_rock_speed_min = 0.5
base_rock_speed_max = 2.0

# Progresión de dificultad
difficulty_increase_time = 1800  # 30 segundos
speed_multiplier_per_level = 0.3  # 30% más rápido por nivel

# Tamaños de rocas
rock1_scale_min = 0.6  # Rock1 normal
rock1_scale_max = 1.4
rock2_scale_min = 0.4  # Rock2 más pequeña
rock2_scale_max = 0.8
```

## 🏆 Estadísticas Rastreadas

- **Puntuación total**
- **Rocas destruidas**
- **Tiempo de supervivencia**
- **Nivel de dificultad alcanzado**
- **Precisión de disparo** (% de balas que impactan)
- **Total de balas disparadas**

## 🚀 Características Técnicas

- **Arquitectura modular** con separación de responsabilidades
- **Sistema de sprites** de Pygame para colisiones eficientes
- **Manejo de eventos** optimizado
- **Rendering en tiempo real** con rotación y escalado de imágenes
- **Sistema de estadísticas** centralizado

## 📊 Próximas Características

- [ ] Efectos de sonido
- [ ] Efectos visuales de explosión
- [ ] Sistema de vidas
- [ ] Pantalla de Game Over
- [ ] Guardado de récords
- [ ] Power-ups

## 🐛 Reportar Problemas

Si encuentras algún bug o tienes sugerencias, por favor crea un issue en el repositorio.

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
