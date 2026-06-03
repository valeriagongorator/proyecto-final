# Word Hunt Game

## Project Description

**Word Hunt Game** is an interactive Python application developed as the final project for Code in Place 2026 by **Valeria Estefanía Góngora Torres**. The objective of the game is to discover hidden words in a randomly generated grid while managing time, lives, and score points through different difficulty levels.

The game was developed as a desktop application using **PyQt5**, providing an engaging graphical interface and an enjoyable user experience.

---

## Author

**Valeria Estefanía Góngora Torres**

---

## What the Game Is About

The game includes:

- A hidden word search board generated randomly
- Selection of letters in straight lines: horizontal, vertical, or diagonal
- Word validation and scoring
- Lives and timer management
- Bonus points for correct words and level progression

---

## Course Connection

This project applies several topics covered in Code in Place:

- Week 3: Variables, numbers, `random`, and libraries
  - `random` is used to generate the board and place words randomly.
- Week 4: `if`, `elif`, `else`, `for`, and `while`
  - Conditional logic checks found words, lives, time, and outcomes.
  - Loops are used to traverse the matrix and update the word list.
- Week 5: Graphics
  - The interface is built with PyQt5 using buttons, grids, screens, cards, and timers.
- Week 6: Data
  - Lists such as `hidden_words`, `found_words`, and `board_buttons` are used.
  - A dictionary named `NIVELES` stores difficulty, time, hints, and points.
  - A dictionary named `found_words_status` tracks which words have already been found.

This project demonstrates not only a working game, but also the use of core programming concepts learned during the course.

---

## Technologies Used

- Python 3
- PyQt5 for the graphical interface
- Standard Python modules:
  - `random`
  - `os`
  - `string`

---

## Project Structure

```text
proyecto-final/
├── main.py
├── src/
│   └── main_qt.py
├── tests/
│   └── test_selection_validation.py
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/valeriagongorator/proyecto-final.git
```

### 2. Enter the project folder

```bash
cd proyecto-final
```

### 3. Optional: create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Dependencies

Install the required dependency:

```bash
pip install PyQt5
```

---

## How to Run

```bash
python3 main.py
```

---

## How to Play

1. Start the program.
2. Select a level.
3. Find hidden words by selecting letters in a straight line.
4. Confirm the word to earn points and time bonuses.
5. Avoid incorrect selections, because each wrong attempt costs a life.

---

## Main Features

- Graphical interface with PyQt5
- Word search gameplay
- Levels of difficulty
- Score, combo, lives, and timer system
- Hint system and sound effects
- Educational Python project structure

---

## Notes

- Developed as a Code in Place final project
- Focused on practicing Python and GUI development
- Designed to be clear, interactive, and easy to extend

---

## Possible Future Improvements

- More levels and additional word categories
- Better animations and visual effects
- Sound volume controls
- Local score history or save system

---

## Credits

Developed by:

**Valeria Estefanía Góngora Torres**
