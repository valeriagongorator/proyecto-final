import random
import string
import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


NIVELES = {
    1: {
        "nombre": "Principiante",
        "tamano": 8,
        "palabras": ["SOL", "LUZ", "MAR", "RIO", "PEZ", "AVE", "OJO", "DIA"],
        "tiempo": 180,
        "vidas": 5,
        "pistas": 3,
        "color": "#9ece6a",
        "puntos_base": 10,
    },
    2: {
        "nombre": "Fácil",
        "tamano": 10,
        "palabras": ["PYTHON", "CODIGO", "JUEGO", "LETRA", "BUSCAR", "MATRIZ", "CICLO", "CLASE"],
        "tiempo": 240,
        "vidas": 4,
        "pistas": 2,
        "color": "#7dcfff",
        "puntos_base": 15,
    },
    3: {
        "nombre": "Intermedio",
        "tamano": 12,
        "palabras": ["VARIABLE", "FUNCION", "ARREGLO", "METODO", "OBJETO", "LOGICA", "BUCLE", "DATOS"],
        "tiempo": 300,
        "vidas": 4,
        "pistas": 2,
        "color": "#e0af68",
        "puntos_base": 20,
    },
    4: {
        "nombre": "Avanzado",
        "tamano": 14,
        "palabras": ["ALGORITMO", "RECURSION", "INTERFAZ", "HERENCIA", "ESTRUCTURA", "PARAMETRO", "ITERACION"],
        "tiempo": 360,
        "vidas": 3,
        "pistas": 1,
        "color": "#ff9e64",
        "puntos_base": 30,
    },
    5: {
        "nombre": "Experto",
        "tamano": 16,
        "palabras": ["PROGRAMACION", "COMPUTADORA", "DESARROLLO", "APLICACION", "COMPILADOR", "OPTIMIZAR", "DEPURADOR"],
        "tiempo": 420,
        "vidas": 3,
        "pistas": 1,
        "color": "#ff79c6",
        "puntos_base": 40,
    },
    6: {
        "nombre": "Maestro",
        "tamano": 18,
        "palabras": ["ENCAPSULAMIENTO", "POLIMORFISMO", "ABSTRACCION", "MODULARIDAD", "CONSTRUCTOR", "INSTANCIACION"],
        "tiempo": 480,
        "vidas": 2,
        "pistas": 0,
        "color": "#bb9af7",
        "puntos_base": 50,
    },
}


def crear_matriz_vacia(tamano):
    return [["" for _ in range(tamano)] for _ in range(tamano)]


def obtener_direcciones():
    return [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]


def puede_colocar_palabra(tablero, palabra, fila, col, dir_fila, dir_col):
    tamano = len(tablero)
    for i, letra in enumerate(palabra):
        nueva_fila = fila + (i * dir_fila)
        nueva_col = col + (i * dir_col)
        if nueva_fila < 0 or nueva_fila >= tamano:
            return False
        if nueva_col < 0 or nueva_col >= tamano:
            return False
        celda = tablero[nueva_fila][nueva_col]
        if celda != "" and celda != letra:
            return False
    return True


def colocar_palabra(tablero, palabra, fila, col, dir_fila, dir_col):
    posiciones = []
    for i, letra in enumerate(palabra):
        nueva_fila = fila + (i * dir_fila)
        nueva_col = col + (i * dir_col)
        tablero[nueva_fila][nueva_col] = letra
        posiciones.append((nueva_fila, nueva_col))
    return posiciones


def insertar_palabra_en_tablero(tablero, palabra, max_intentos=100):
    tamano = len(tablero)
    direcciones = obtener_direcciones()
    for _ in range(max_intentos):
        fila = random.randint(0, tamano - 1)
        col = random.randint(0, tamano - 1)
        dir_fila, dir_col = random.choice(direcciones)
        if puede_colocar_palabra(tablero, palabra, fila, col, dir_fila, dir_col):
            return colocar_palabra(tablero, palabra, fila, col, dir_fila, dir_col)
    return None


def rellenar_tablero_con_letras(tablero):
    letras = string.ascii_uppercase
    for fila in range(len(tablero)):
        for col in range(len(tablero[fila])):
            if tablero[fila][col] == "":
                tablero[fila][col] = random.choice(letras)


def generar_tablero(tamano, palabras):
    tablero = crear_matriz_vacia(tamano)
    posiciones_palabras = {}
    palabras_colocadas = []
    palabras_ordenadas = sorted(palabras, key=len, reverse=True)
    for palabra in palabras_ordenadas:
        posiciones = insertar_palabra_en_tablero(tablero, palabra)
        if posiciones:
            posiciones_palabras[palabra] = posiciones
            palabras_colocadas.append(palabra)
    rellenar_tablero_con_letras(tablero)
    return tablero, posiciones_palabras, palabras_colocadas


def formatear_tiempo(segundos):
    minutos = segundos // 60
    segs = segundos % 60
    return f"{minutos:02d}:{segs:02d}"


class WordHuntApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Hunt • Proyecto Final")
        self.resize(1180, 820)
        self.setMinimumSize(1050, 760)

        # Estado global del juego
        self.best_score = 0
        self.total_words_found = 0
        self.games_played = 0

        self.current_level = 1
        self.current_board = []
        self.board_buttons = []
        self.hidden_words = []
        self.hidden_positions = {}
        self.word_colors = {}
        self.hint_positions = set()
        self.hint_sources = {}
        self.found_words = []
        self.selected_positions = []
        self.selected_letters = []
        self.score = 0
        self.combo = 0
        self.best_combo = 0
        self.lives = 0
        self.max_lives = 0
        self.hints_left = 0
        self.time_left = 0
        self.level_status = {}

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick_timer)

        self.confetti_timer = QTimer(self)
        self.confetti_timer.timeout.connect(self._animate_confetti)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        self._build_home_view()
        self._build_level_view()
        self._build_game_view()
        self._build_summary_view()

        self.show_screen("home")

    def _card_style(self, color, bg="#24283b"):
        return (
            f"QFrame {{ background-color: {bg}; border: 1px solid {color}; border-radius: 20px; }}"
            f"QFrame:hover {{ border: 2px solid {color}; }}"
        )

    def _button_style(self, bg_color, text_color="#1a1b26"):
        return (
            f"QPushButton {{ background-color: {bg_color}; color: {text_color}; border-radius: 14px; "
            "padding: 12px 16px; font-weight: 700; font-size: 13px; }"
            f"QPushButton:hover {{ background-color: #d0d7ff; }}"
        )

    def _build_home_view(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)

        header = QFrame()
        header.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("WORD HUNT")
        title.setStyleSheet("color: #7dcfff; font-family: 'Menlo'; font-size: 68px; font-weight: 800;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)

        subtitle = QLabel("Sopa de letras interactiva con niveles, pistas, combos y un sistema de puntaje visual.")
        subtitle.setStyleSheet("color: #c0caf5; font-family: 'Menlo'; font-size: 14px;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)

        hero = QFrame()
        hero.setStyleSheet("background-color: #24283b; border-radius: 26px; border: 1px solid #414868;")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 24, 24, 24)

        hero_badges = QHBoxLayout()
        hero_badges.setSpacing(10)
        badge1 = QLabel("PROYECTO FINAL")
        badge1.setStyleSheet("background-color: #1a1b26; color: #7dcfff; border-radius: 999px; padding: 8px 12px; font-size: 10px; font-family: 'Menlo'; font-weight: 800;")
        badge2 = QLabel("PYQT5 · MAC")
        badge2.setStyleSheet("background-color: #1a1b26; color: #e0af68; border-radius: 999px; padding: 8px 12px; font-size: 10px; font-family: 'Menlo'; font-weight: 800;")
        hero_badges.addWidget(badge1)
        hero_badges.addWidget(badge2)
        hero_badges.addStretch()
        hero_layout.addLayout(hero_badges)

        hero_grid = QWidget()
        preview_layout = QGridLayout(hero_grid)
        preview_layout.setContentsMargins(0,0,0,0)
        preview_layout.setSpacing(6)
        preview_letters = [
            ["P","Y","T","H"],
            ["O","N","A","R"],
            ["C","O","D","E"],
            ["L","E","T","R"],
        ]
        for r, row in enumerate(preview_letters):
            for c, letter in enumerate(row):
                cell = QLabel(letter)
                cell.setAlignment(Qt.AlignCenter)
                cell.setStyleSheet(
                    "QLabel { background-color: #414868; color: #c0caf5; border-radius: 10px; min-width: 38px; min-height: 38px; font-family: 'Menlo'; font-weight: 800; font-size: 16px; }"
                )
                preview_layout.addWidget(cell, r, c)
        hero_layout.addWidget(hero_grid)

        hero_desc = QLabel("Busca palabras, acumula combos, usa pistas y avanza por siete niveles de dificultad.")
        hero_desc.setStyleSheet("color: #a9b1d6; font-family: 'Menlo'; font-size: 12px;")
        hero_layout.addWidget(hero_desc)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(10)
        stats_row.addWidget(self._create_stat_card("RECORD", str(self.best_score), "#e0af68"))
        stats_row.addWidget(self._create_stat_card("PARTIDAS", str(self.games_played), "#7dcfff"))
        stats_row.addWidget(self._create_stat_card("PALABRAS", str(self.total_words_found), "#9ece6a"))
        stats_row.addWidget(self._create_stat_card("NIVELES", "0/6", "#bb9af7"))
        hero_layout.addLayout(stats_row)

        buttons_row = QHBoxLayout()
        start_btn = QPushButton("INICIAR PARTIDA")
        start_btn.setStyleSheet(self._button_style("#9ece6a", "#1a1b26"))
        start_btn.clicked.connect(lambda: self.show_screen("level"))
        guide_btn = QPushButton("VER GUÍA")
        guide_btn.setStyleSheet(self._button_style("#7dcfff", "#1a1b26"))
        guide_btn.clicked.connect(lambda: self.show_screen("level"))
        buttons_row.addWidget(start_btn)
        buttons_row.addWidget(guide_btn)
        buttons_row.addStretch()
        hero_layout.addLayout(buttons_row)

        layout.addWidget(header)
        layout.addWidget(hero)

        footer = QLabel("Code in Place · Python + PyQt5 · Proyecto Final")
        footer.setStyleSheet("color: #565f89; font-family: 'Menlo'; font-size: 10px;")
        layout.addWidget(footer, alignment=Qt.AlignLeft)

        self.home_page = page
        self.stacked.addWidget(page)

    def _build_level_view(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(18)

        top = QHBoxLayout()
        back_btn = QPushButton("< MENÚ")
        back_btn.setStyleSheet(self._button_style("#24283b", "#7dcfff"))
        back_btn.clicked.connect(lambda: self.show_screen("home"))
        top.addWidget(back_btn)

        title = QLabel("SELECCIONA TU RETO")
        title.setStyleSheet("color: #c0caf5; font-family: 'Menlo'; font-size: 32px; font-weight: 800;")
        top.addWidget(title)
        top.addStretch()
        layout.addLayout(top)

        subtitle = QLabel("Cada nivel cambia el tamaño del tablero, el tiempo y la complejidad del reto.")
        subtitle.setStyleSheet("color: #565f89; font-family: 'Menlo'; font-size: 11px;")
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(16)
        self.level_cards = {}
        for idx, (number, config) in enumerate(NIVELES.items(), start=1):
            card = QFrame()
            card.setStyleSheet(self._card_style(config["color"], "#24283b"))
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(18, 18, 18, 18)
            card_layout.setSpacing(10)

            status = QLabel("NUEVO" if number not in self.level_status else self.level_status[number])
            status.setStyleSheet(f"color: {config['color']}; font-family: 'Menlo'; font-size: 9px; font-weight: 800;")
            card_layout.addWidget(status, alignment=Qt.AlignRight)

            title_label = QLabel(f"NIVEL {number}")
            title_label.setStyleSheet(f"color: {config['color']}; font-family: 'Menlo'; font-size: 10px; font-weight: 800;")
            card_layout.addWidget(title_label)

            nome = QLabel(config["nombre"].upper())
            nome.setStyleSheet(f"color: {config['color']}; font-family: 'Menlo'; font-size: 24px; font-weight: 800;")
            card_layout.addWidget(nome)

            info = QLabel(f"Tablero {config['tamano']}x{config['tamano']} • {formatear_tiempo(config['tiempo'])} • {config['vidas']} vidas")
            info.setStyleSheet("color: #c0caf5; font-family: 'Menlo'; font-size: 11px;")
            info.setWordWrap(True)
            card_layout.addWidget(info)

            tags = QHBoxLayout()
            hints = QLabel(f"{config['pistas']} pistas")
            hints.setStyleSheet("background-color: #1a1b26; color: #bb9af7; border-radius: 999px; padding: 6px 10px; font-family: 'Menlo'; font-size: 9px; font-weight: 800;")
            points = QLabel(f"{config['puntos_base']} pts/word")
            points.setStyleSheet("background-color: #1a1b26; color: #ff9e64; border-radius: 999px; padding: 6px 10px; font-family: 'Menlo'; font-size: 9px; font-weight: 800;")
            tags.addWidget(hints)
            tags.addWidget(points)
            tags.addStretch()
            card_layout.addLayout(tags)

            play_btn = QPushButton("JUGAR")
            play_btn.setStyleSheet(self._button_style(config["color"], "#1a1b26"))
            play_btn.clicked.connect(lambda checked=False, n=number: self.start_level(n))
            card_layout.addWidget(play_btn)

            row = (number - 1) // 3
            col = (number - 1) % 3
            grid.addWidget(card, row, col)
            self.level_cards[number] = card

        layout.addLayout(grid)
        self.level_page = page
        self.stacked.addWidget(page)

    def _build_game_view(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        header = QFrame()
        header.setStyleSheet("background: transparent;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        back_btn = QPushButton("X SALIR")
        back_btn.setStyleSheet(self._button_style("#1a1b26", "#f7768e"))
        back_btn.clicked.connect(lambda: self.show_screen("level"))
        header_layout.addWidget(back_btn)

        self.level_header = QLabel("")
        self.level_header.setStyleSheet("color: #c0caf5; font-family: 'Menlo'; font-size: 18px; font-weight: 800;")
        header_layout.addWidget(self.level_header)
        header_layout.addStretch()

        self.timer_label = QLabel("03:00")
        self.timer_label.setStyleSheet("background-color: #24283b; color: #7dcfff; border-radius: 12px; padding: 10px 14px; font-family: 'Menlo'; font-size: 22px; font-weight: 800;")
        header_layout.addWidget(self.timer_label)

        layout.addWidget(header)

        content = QHBoxLayout()
        content.setSpacing(18)

        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #1a1b26; border-radius: 24px; border: 1px solid #414868;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(12)

        timer_progress = QFrame()
        timer_progress.setStyleSheet("background-color: #24283b; border-radius: 999px;")
        timer_progress.setFixedHeight(10)
        timer_progress_layout = QHBoxLayout(timer_progress)
        timer_progress_layout.setContentsMargins(0,0,0,0)
        self.time_fill = QFrame()
        self.time_fill.setStyleSheet("background-color: #7dcfff; border-radius: 999px;")
        self.time_fill.setFixedWidth(0)
        timer_progress_layout.addWidget(self.time_fill)
        left_layout.addWidget(timer_progress)

        board_card = QFrame()
        board_card.setStyleSheet("background-color: #24283b; border-radius: 24px; border: 1px solid #414868;")
        board_layout = QVBoxLayout(board_card)
        board_layout.setContentsMargins(14, 14, 14, 14)

        self.board_widget = QWidget()
        self.board_grid = QGridLayout(self.board_widget)
        self.board_grid.setSpacing(6)
        self.board_grid.setContentsMargins(0,0,0,0)
        board_layout.addWidget(self.board_widget)
        left_layout.addWidget(board_card)

        controls = QFrame()
        controls.setStyleSheet("background-color: #1a1b26;")
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0,0,0,0)

        self.word_preview = QLabel("")
        self.word_preview.setStyleSheet("color: #e0af68; font-family: 'Menlo'; font-size: 22px; font-weight: 800;")
        self.word_preview.setMinimumHeight(30)
        controls_layout.addWidget(self.word_preview)

        controls_layout.addStretch()

        self.status_label = QLabel("Selecciona letras para formar una palabra.")
        self.status_label.setStyleSheet("color: #c0caf5; font-family: 'Menlo'; font-size: 10px;")
        controls_layout.addWidget(self.status_label, alignment=Qt.AlignRight)
        left_layout.addWidget(controls)

        actions = QHBoxLayout()
        actions.setSpacing(10)
        self.confirm_btn = QPushButton("CONFIRMAR")
        self.confirm_btn.setStyleSheet(self._button_style("#9ece6a", "#1a1b26"))
        self.confirm_btn.clicked.connect(self.confirm_selection)
        actions.addWidget(self.confirm_btn)

        self.clear_btn = QPushButton("BORRAR")
        self.clear_btn.setStyleSheet(self._button_style("#f7768e", "#1a1b26"))
        self.clear_btn.clicked.connect(self.clear_selection)
        actions.addWidget(self.clear_btn)

        self.hint_btn = QPushButton("PISTA (0)")
        self.hint_btn.setStyleSheet(self._button_style("#bb9af7", "#1a1b26"))
        self.hint_btn.clicked.connect(self.use_hint)
        actions.addWidget(self.hint_btn)
        left_layout.addLayout(actions)

        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #24283b; border-radius: 26px; border: 1px solid #414868;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(12)

        right_layout.addWidget(QLabel("ESTADÍSTICAS"), alignment=Qt.AlignLeft)
        right_layout.addWidget(QLabel("Seguimiento del progreso y el combo"), alignment=Qt.AlignLeft)

        self.score_card = self._create_stat_card("PUNTOS", "0", "#e0af68")
        self.combo_card = self._create_stat_card("COMBO", "x0", "#ff9e64")
        self.lives_card = self._create_stat_card("VIDAS", "●●●", "#f7768e")
        self.score_value_label = self.score_card.value_label
        self.combo_value_label = self.combo_card.value_label
        self.lives_value_label = self.lives_card.value_label
        right_layout.addWidget(self.score_card)
        right_layout.addWidget(self.combo_card)
        right_layout.addWidget(self.lives_card)

        words_title = QLabel("PALABRAS")
        words_title.setStyleSheet("color: #c0caf5; font-family: 'Menlo'; font-size: 12px; font-weight: 800;")
        right_layout.addWidget(words_title)

        self.words_container = QWidget()
        self.words_layout = QVBoxLayout(self.words_container)
        self.words_layout.setContentsMargins(0,0,0,0)
        self.words_layout.setSpacing(6)
        self.words_scroll = QScrollArea()
        self.words_scroll.setWidgetResizable(True)
        self.words_scroll.setStyleSheet("background-color: transparent; border: none;")
        self.words_scroll.setWidget(self.words_container)
        right_layout.addWidget(self.words_scroll)

        self.progress_label = QLabel("0/0 · 0%")
        self.progress_label.setStyleSheet("color: #7dcfff; font-family: 'Menlo'; font-size: 12px; font-weight: 800;")
        right_layout.addWidget(self.progress_label)

        content.addWidget(left_panel, 3)
        content.addWidget(right_panel, 1)

        layout.addLayout(content)
        self.game_page = page
        self.stacked.addWidget(page)

    def _build_summary_view(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 28, 40, 28)
        layout.setSpacing(16)

        self.summary_title = QLabel("VICTORIA")
        self.summary_title.setStyleSheet("color: #9ece6a; font-family: 'Menlo'; font-size: 58px; font-weight: 800;")
        self.summary_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.summary_title)

        self.summary_subtitle = QLabel("Has completado el nivel.")
        self.summary_subtitle.setStyleSheet("color: #c0caf5; font-family: 'Menlo'; font-size: 13px;")
        self.summary_subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.summary_subtitle)

        summary_cards = QHBoxLayout()
        self.summary_score = self._create_stat_card("PUNTUACIÓN FINAL", "0", "#e0af68")
        self.summary_bonus = self._create_stat_card("BONUS", "0", "#7dcfff")
        self.summary_combo = self._create_stat_card("MEJOR COMBO", "x0", "#ff9e64")
        summary_cards.addWidget(self.summary_score)
        summary_cards.addWidget(self.summary_bonus)
        summary_cards.addWidget(self.summary_combo)
        layout.addLayout(summary_cards)

        action_row = QHBoxLayout()
        retry_btn = QPushButton("REINTENTAR")
        retry_btn.setStyleSheet(self._button_style("#7dcfff", "#1a1b26"))
        retry_btn.clicked.connect(self.retry_level)
        next_btn = QPushButton("SIGUIENTE")
        next_btn.setStyleSheet(self._button_style("#9ece6a", "#1a1b26"))
        next_btn.clicked.connect(self.next_level)
        menu_btn = QPushButton("MENÚ")
        menu_btn.setStyleSheet(self._button_style("#bb9af7", "#1a1b26"))
        menu_btn.clicked.connect(lambda: self.show_screen("home"))
        action_row.addWidget(retry_btn)
        action_row.addWidget(next_btn)
        action_row.addWidget(menu_btn)
        action_row.addStretch()
        layout.addLayout(action_row)

        self.confetti_layer = QWidget(page)
        self.confetti_layer.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.confetti_layer.setStyleSheet("background-color: transparent;")
        self.confetti_layer.hide()
        self.confetti_particles = []

        self.summary_page = page
        self.stacked.addWidget(page)

    def _launch_confetti(self):
        self.confetti_layer.show()
        self.confetti_layer.raise_()
        self.confetti_layer.setGeometry(0, 0, self.width(), self.height())
        for particle in self.confetti_particles:
            particle["widget"].deleteLater()
        self.confetti_particles = []

        colors = ["#9ece6a", "#7dcfff", "#e0af68", "#ff9e64", "#bb9af7", "#f7768e", "#ff79c6"]
        for _ in range(48):
            particle = QLabel(random.choice(["✦", "●", "★", "❇"]))
            particle.setAttribute(Qt.WA_TransparentForMouseEvents)
            particle.setStyleSheet(f"color: {random.choice(colors)}; font-family: 'Menlo'; font-size: 18px; font-weight: 800;")
            particle.adjustSize()
            x = random.randint(20, max(40, self.width() - 40))
            y = random.randint(-20, 120)
            particle.move(x, y)
            particle.setParent(self.confetti_layer)
            particle.show()
            self.confetti_particles.append({
                "widget": particle,
                "x": float(x),
                "y": float(y),
                "vx": random.uniform(-1.2, 1.2),
                "vy": random.uniform(1.0, 2.4),
                "spin": random.uniform(-0.2, 0.2),
            })

        self.confetti_timer.start(20)

    def _animate_confetti(self):
        width = max(1, self.width())
        height = max(1, self.height())
        alive = []
        for item in self.confetti_particles:
            particle = item["widget"]
            item["x"] += item["vx"]
            item["y"] += item["vy"]
            item["vy"] += 0.18
            particle.move(int(item["x"]), int(item["y"]))
            if item["y"] < height + 20:
                alive.append(item)
            else:
                particle.deleteLater()

        self.confetti_particles = alive
        if not self.confetti_particles:
            self.confetti_timer.stop()
            self.confetti_layer.hide()

    def _create_stat_card(self, title, value, accent):
        card = QFrame()
        card.setStyleSheet(
            f"QFrame {{ background-color: #24283b; border-radius: 18px; border: 1px solid {accent}; }}"
        )
        card.setMinimumHeight(78)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #565f89; font-family: 'Menlo'; font-size: 9px; font-weight: 800;")
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"color: {accent}; font-family: 'Menlo'; font-size: 24px; font-weight: 800;")
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.value_label = value_label
        return card

    def show_screen(self, name):
        if name == "home":
            self.confetti_timer.stop()
            self.confetti_layer.hide()
            self.refresh_home_stats()
            self.stacked.setCurrentWidget(self.home_page)
        elif name == "level":
            self.confetti_timer.stop()
            self.confetti_layer.hide()
            self.refresh_level_cards()
            self.stacked.setCurrentWidget(self.level_page)
        elif name == "game":
            self.confetti_timer.stop()
            self.confetti_layer.hide()
            self.stacked.setCurrentWidget(self.game_page)
        elif name == "summary":
            self.stacked.setCurrentWidget(self.summary_page)

    def refresh_home_stats(self):
        # update home cards to current in-memory stats
        pass

    def refresh_level_cards(self):
        for number, card in self.level_cards.items():
            status = "COMPLETADO" if self.level_status.get(number) == "COMPLETADO" else "NUEVO"
            status_color = "#9ece6a" if status == "COMPLETADO" else "#7dcfff"
            for child in card.findChildren(QLabel):
                if child.text() == "NUEVO" or child.text() == "COMPLETADO":
                    child.setText(status)
                    child.setStyleSheet(f"color: {status_color}; font-family: 'Menlo'; font-size: 9px; font-weight: 800;")
                    break

    def start_level(self, level_number):
        self.current_level = level_number
        config = NIVELES[level_number]
        self.current_board, self.hidden_positions, self.hidden_words = generar_tablero(config["tamano"], config["palabras"])
        palette = ["#7dcfff", "#9ece6a", "#e0af68", "#ff9e64", "#ff79c6", "#bb9af7", "#f7768e"]
        self.word_colors = {word: palette[index % len(palette)] for index, word in enumerate(self.hidden_words)}
        self.hint_positions.clear()
        self.hint_sources.clear()
        self.found_words = []
        self.selected_positions = []
        self.selected_letters = []
        self.score = 0
        self.combo = 0
        self.best_combo = 0
        self.lives = config["vidas"]
        self.max_lives = config["vidas"]
        self.hints_left = config["pistas"]
        self.time_left = config["tiempo"]
        self.level_header.setText(f"NIVEL {level_number}: {config['nombre'].upper()}")
        self.level_header.setStyleSheet(f"color: {config['color']}; font-family: 'Menlo'; font-size: 18px; font-weight: 800;")
        self.timer_label.setText(formatear_tiempo(self.time_left))
        self.timer_label.setStyleSheet(f"background-color: #24283b; color: {config['color']}; border-radius: 12px; padding: 10px 14px; font-family: 'Menlo'; font-size: 22px; font-weight: 800;")
        self.hint_btn.setText(f"PISTA ({self.hints_left})")
        self.word_preview.setText("")
        self.status_label.setText("Selecciona letras para formar una palabra.")
        self._build_board()
        self._refresh_sidebar()
        self._refresh_progress()
        self._update_time_bar()
        self.timer.start(1000)
        self.show_screen("game")

    def _build_board(self):
        for i in reversed(range(self.board_grid.count())):
            item = self.board_grid.itemAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.board_buttons = []

        config = NIVELES[self.current_level]
        size = config["tamano"]
        for row in range(size):
            row_buttons = []
            for col in range(size):
                letter = self.current_board[row][col]
                cell_btn = QPushButton(letter)
                cell_btn.setFixedSize(48, 48)
                cell_btn.setCheckable(True)
                cell_btn.setStyleSheet(
                    "QPushButton { background-color: #414868; color: #c0caf5; border-radius: 10px; font-family: 'Menlo'; font-size: 16px; font-weight: 800; }"
                    "QPushButton:hover { background-color: #565f89; }"
                    "QPushButton:checked { background-color: #7dcfff; color: #1a1b26; }"
                )
                cell_btn.clicked.connect(lambda checked=False, r=row, c=col: self.toggle_cell(r, c))
                self.board_grid.addWidget(cell_btn, row, col)
                row_buttons.append(cell_btn)
            self.board_buttons.append(row_buttons)

    def toggle_cell(self, row, col):
        position = (row, col)
        if position in self.selected_positions:
            index = self.selected_positions.index(position)
            self.selected_positions = self.selected_positions[:index]
            self.selected_letters = self.selected_letters[:index]
            self._rebuild_board_visuals()
        else:
            self.selected_positions.append(position)
            self.selected_letters.append(self.current_board[row][col])
            self._rebuild_board_visuals()

        self.word_preview.setText("".join(self.selected_letters))

    def _rebuild_board_visuals(self):
        config = NIVELES[self.current_level]
        size = config["tamano"]
        found_positions = []
        found_word_by_pos = {}
        for word in self.found_words:
            for position in self.hidden_positions.get(word, []):
                found_positions.append(position)
                found_word_by_pos[position] = word

        for row in range(size):
            for col in range(size):
                button = self.board_buttons[row][col] if row < len(self.board_buttons) and col < len(self.board_buttons[row]) else None
                if not button:
                    continue
                position = (row, col)
                if position in self.selected_positions:
                    button.setChecked(True)
                    button.setStyleSheet(
                        "QPushButton { background-color: #7dcfff; color: #1a1b26; border-radius: 10px; border: 2px solid #7dcfff; font-family: 'Menlo'; font-size: 16px; font-weight: 800; }"
                    )
                elif position in found_positions:
                    word = found_word_by_pos[position]
                    accent = self.word_colors.get(word, "#9ece6a")
                    button.setChecked(False)
                    button.setStyleSheet(
                        f"QPushButton {{ background-color: {accent}; color: #1a1b26; border-radius: 10px; border: 2px solid {accent}; font-family: 'Menlo'; font-size: 16px; font-weight: 800; }}"
                    )
                elif position in self.hint_positions:
                    button.setChecked(False)
                    button.setStyleSheet(
                        "QPushButton { background-color: #1a1b26; color: #e0af68; border-radius: 10px; border: 2px solid #e0af68; font-family: 'Menlo'; font-size: 16px; font-weight: 800; }"
                    )
                else:
                    button.setChecked(False)
                    button.setStyleSheet(
                        "QPushButton { background-color: #414868; color: #c0caf5; border-radius: 10px; font-family: 'Menlo'; font-size: 16px; font-weight: 800; }"
                        "QPushButton:hover { background-color: #565f89; }"
                    )

    def clear_selection(self):
        self.selected_positions = []
        self.selected_letters = []
        self.word_preview.setText("")
        self.status_label.setText("Selecciona letras para formar una palabra.")
        self._rebuild_board_visuals()

    def confirm_selection(self):
        word = "".join(self.selected_letters)
        if not word:
            return
        if word in self.hidden_words and word not in self.found_words:
            self._register_word(word)
        else:
            self._wrong_word()

    def _register_word(self, word):
        self.found_words.append(word)
        self.combo += 1
        self.best_combo = max(self.best_combo, self.combo)
        config = NIVELES[self.current_level]
        gained = config["puntos_base"] * len(word) * max(1, self.combo)
        self.score += gained
        for pos in self.hidden_positions[word]:
            self.current_board[pos[0]][pos[1]] = self.current_board[pos[0]][pos[1]]
        self._refresh_sidebar()
        self._refresh_progress()
        self.word_preview.setText("")
        self.selected_positions = []
        self.selected_letters = []
        self.status_label.setText(f"¡{word} encontrada! +{gained} puntos.")
        self._rebuild_board_visuals()
        if len(self.found_words) == len(self.hidden_words):
            self.finish_level(victory=True)

    def _wrong_word(self):
        self.lives -= 1
        self.combo = 0
        self.status_label.setText("Palabra incorrecta. Pierdes una vida.")
        self._refresh_sidebar()
        for pos in self.selected_positions:
            pass
        self.word_preview.setText("")
        self.selected_positions = []
        self.selected_letters = []
        self._rebuild_board_visuals()
        self._refresh_sidebar()
        if self.lives <= 0:
            self.finish_level(victory=False)

    def use_hint(self):
        if self.hints_left <= 0:
            return
        remaining = [w for w in self.hidden_words if w not in self.found_words]
        if not remaining:
            return
        word = random.choice(remaining)
        row, col = self.hidden_positions[word][0]
        self.hint_positions.add((row, col))
        self.hint_sources[(row, col)] = word
        self.status_label.setText(f"Pista: se resaltó una letra de {word}.")
        self.hints_left -= 1
        self.hint_btn.setText(f"PISTA ({self.hints_left})")
        self._rebuild_board_visuals()

    def _refresh_sidebar(self):
        self.score_value_label.setText(str(self.score))
        self.combo_value_label.setText(f"x{self.combo}")
        self.lives_value_label.setText("●" * self.lives)

    def _refresh_progress(self):
        found = len(self.found_words)
        total = len(self.hidden_words)
        percent = int((found / total) * 100) if total else 0
        self.progress_label.setText(f"{found}/{total} · {percent}%")

        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for word in self.hidden_words:
            row = QFrame()
            accent = self.word_colors.get(word, "#7dcfff")
            row.setStyleSheet(
                f"QFrame {{ background-color: #1a1b26; border-radius: 12px; border: 1px solid {accent}; }}"
            )
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 8, 10, 8)
            word_label = QLabel(word)
            word_label.setStyleSheet(f"color: {accent}; font-family: 'Menlo'; font-size: 11px; font-weight: 800;")
            row_layout.addWidget(word_label)

            status_label = QLabel("ENCONTRADA" if word in self.found_words else "OCULTA")
            status_label.setStyleSheet(
                "color: #c0caf5; font-family: 'Menlo'; font-size: 9px; font-weight: 800;"
            )
            row_layout.addStretch()
            row_layout.addWidget(status_label)
            self.words_layout.addWidget(row)

    def _update_time_bar(self):
        config = NIVELES[self.current_level]
        ratio = max(self.time_left / config["tiempo"], 0)
        fill_width = max(10, int(320 * ratio))
        self.time_fill.setFixedWidth(fill_width)
        if ratio < 0.25:
            self.time_fill.setStyleSheet("background-color: #f7768e; border-radius: 999px;")
        elif ratio < 0.5:
            self.time_fill.setStyleSheet("background-color: #e0af68; border-radius: 999px;")
        else:
            self.time_fill.setStyleSheet("background-color: #7dcfff; border-radius: 999px;")

    def tick_timer(self):
        self.time_left -= 1
        self.timer_label.setText(formatear_tiempo(self.time_left))
        self._update_time_bar()
        if self.time_left <= 0:
            self.timer.stop()
            self.finish_level(victory=False)

    def finish_level(self, victory):
        self.timer.stop()
        self.confetti_timer.stop()
        self.games_played += 1
        self.total_words_found += len(self.found_words)
        self.best_score = max(self.best_score, self.score)
        bonus_time = self.time_left * 2
        bonus_lives = self.lives * 50
        bonus_perfect = 200 if victory and self.lives == self.max_lives else 0
        final_score = self.score + bonus_time + bonus_lives + bonus_perfect
        if victory:
            self.level_status[self.current_level] = "COMPLETADO"
            self.summary_title.setText("VICTORIA")
            self.summary_title.setStyleSheet("color: #9ece6a; font-family: 'Menlo'; font-size: 58px; font-weight: 800;")
            self.summary_subtitle.setText("Has completado el nivel y sumaste bonificaciones.")
            self.summary_score.value_label.setText(str(final_score))
            self._launch_confetti()
        else:
            self.summary_title.setText("DERROTA")
            self.summary_title.setStyleSheet("color: #f7768e; font-family: 'Menlo'; font-size: 58px; font-weight: 800;")
            self.summary_subtitle.setText("Se agotó el tiempo o te quedaste sin vidas.")
            self.summary_score.value_label.setText(str(self.score))
            self.confetti_layer.hide()
        self.summary_bonus.value_label.setText(f"+{bonus_time + bonus_lives + bonus_perfect}")
        self.summary_combo.value_label.setText(f"x{self.best_combo}")
        self.show_screen("summary")

    def retry_level(self):
        self.start_level(self.current_level)

    def next_level(self):
        if self.current_level < max(NIVELES.keys()):
            self.start_level(self.current_level + 1)
        else:
            self.show_screen("home")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordHuntApp()
    window.show()
    sys.exit(app.exec_())
