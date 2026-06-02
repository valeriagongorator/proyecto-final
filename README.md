# 🎮 Word Hunt Game

## 📌 Descripción del proyecto

**Word Hunt Game** es un juego interactivo desarrollado en Python como proyecto final de Code in Place.  
El objetivo del jugador es descubrir palabras ocultas dentro del menor número de intentos posibles.

El juego pone a prueba la lógica, el reconocimiento de patrones y la capacidad de deducción del usuario, convirtiéndose en una experiencia sencilla pero entretenida.

Este proyecto fue creado como una aplicación de escritorio utilizando interfaz gráfica con Python.

---

## 👩‍💻 Autora

**Valeria Góngora**

---

## 🧠 ¿En qué se basa el juego?

El juego consiste en:

- Una palabra oculta seleccionada aleatoriamente  
- El jugador intenta adivinarla letra por letra  
- Se muestra el progreso de la palabra  
- Se limitan los intentos  
- El jugador gana si descubre la palabra antes de quedarse sin intentos  

## 📚 Conexión con las semanas del curso

Este proyecto aplica varios conceptos vistos en Code in Place:

- Week 3: Variables, números, `random` y uso de librerías.
  - Se usa `random` para generar el tablero y ubicar palabras de forma aleatoria.
- Week 4: `if`, `elif`, `else`, `for` y `while`.
  - Se usan condicionales para verificar palabras encontradas, vidas, tiempo y resultados.
  - Se usan bucles para recorrer la matriz y actualizar la lista de palabras.
- Week 5: Graphics.
  - La interfaz está construida con PyQt5: botones, cuadrícula, pantallas, tarjetas y temporizador.
- Week 6: Data.
  - Se usan listas como `hidden_words`, `found_words` y `board_buttons`.
  - Se usa un diccionario `NIVELES` para guardar dificultad, tiempo, pistas y puntuación.
  - También se mantiene un diccionario explícito `found_words_status` para saber qué palabras ya fueron encontradas.

Esta combinación demuestra que el proyecto no solo funciona como juego, sino que también aplica conceptos de programación vistos en el curso.

---

## 🛠️ Tecnologías utilizadas

- Python 3  
- PyQt (interfaz gráfica)  
- Módulos estándar de Python:
  - random
  - os
  - string  

---

## 📁 Estructura del proyecto

```
proyecto-final/
│
├── main.py
├── src/
│   ├── main_qt.py   # Lógica principal del juego
│
├── assets/          # Recursos (si aplica)
├── README.md
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/valeriagongorator/proyecto-final.git
```

### 2. Entrar al proyecto

```bash
cd proyecto-final
```

### 3. (Opcional) Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Dependencias

Instalar dependencias necesarias:

```bash
pip install PyQt5
```

---

## 🚀 Cómo ejecutar el proyecto

```bash
python3 main.py
```

---

## 🎮 Cómo jugar

1. Inicia el programa  
2. Observa la palabra oculta en guiones  
3. Ingresa letras para adivinarla  
4. Cada acierto revela letras  
5. Ganas si completas la palabra antes de quedarte sin intentos  

---

## 🧩 Características principales

- Interfaz gráfica con PyQt  
- Juego de adivinanza de palabras  
- Sistema de intentos limitados  
- Lógica de verificación de letras  
- Proyecto educativo en Python  

---

## 📌 Notas

- Proyecto desarrollado para Code in Place  
- Enfocado en práctica de programación en Python  
- Código estructurado para aprendizaje  

---

## 💡 Posibles mejoras futuras

- Niveles de dificultad  
- Sistema de puntuación  
- Temporizador  
- Base de datos de palabras  
- Animaciones o sonidos  

---

## 📷 Demo (opcional)

https://youtube.com/tu-video-aqui

---

## ⭐ Créditos

Desarrollado por:

**Valeria Góngora**
