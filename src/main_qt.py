import math
import os
import random
import struct
import string
import sys
import tempfile
import wave

from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QColor
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


NIVELES = {
    1: {
        "nombre": "Beginner",
        "tamano": 8,
        "palabras": {
            "en": ["APPLE", "RIVER", "MOUNTAIN", "HOUSE", "WATER", "LIGHT", "BIRD", "SMILE"],
            "es": ["MANZANA", "RIO", "MONTANA", "CASA", "AGUA", "LUZ", "PAJARO", "SONRISA"],
        },
        "tiempo": 180,
        "vidas": 5,
        "pistas": 3,
        "color": "#9ece6a",
        "puntos_base": 10,
    },
    2: {
        "nombre": "Easy",
        "tamano": 10,
        "palabras": {
            "en": ["PYTHON", "CODE", "GAME", "LETTER", "SEARCH", "MATRIX", "LOOP", "CLASS"],
            "es": ["PYTHON", "CODIGO", "JUEGO", "LETRA", "BUSCAR", "MATRIZ", "BUCLE", "CLASE"],
        },
        "tiempo": 240,
        "vidas": 4,
        "pistas": 2,
        "color": "#7dcfff",
        "puntos_base": 15,
    },
    3: {
        "nombre": "Intermediate",
        "tamano": 12,
        "palabras": {
            "en": ["VARIABLE", "FUNCTION", "ARRAY", "METHOD", "OBJECT", "LOGIC", "LOOP", "DATA"],
            "es": ["VARIABLE", "FUNCION", "ARREGLO", "METODO", "OBJETO", "LOGICA", "BUCLE", "DATOS"],
        },
        "tiempo": 300,
        "vidas": 4,
        "pistas": 2,
        "color": "#e0af68",
        "puntos_base": 20,
    },
    4: {
        "nombre": "Advanced",
        "tamano": 14,
        "palabras": {
            "en": ["ALGORITHM", "RECURSION", "INTERFACE", "INHERITANCE", "STRUCTURE", "PARAMETER", "ITERATION"],
            "es": ["ALGORITMO", "RECURSION", "INTERFAZ", "HERENCIA", "ESTRUCTURA", "PARAMETRO", "ITERACION"],
        },
        "tiempo": 360,
        "vidas": 3,
        "pistas": 1,
        "color": "#ff9e64",
        "puntos_base": 30,
    },
    5: {
        "nombre": "Expert",
        "tamano": 16,
        "palabras": {
            "en": ["PROGRAMMING", "COMPUTER", "DEVELOPMENT", "APPLICATION", "COMPILER", "OPTIMIZE", "DEBUGGER"],
            "es": ["PROGRAMACION", "COMPUTADORA", "DESARROLLO", "APLICACION", "COMPILADOR", "OPTIMIZAR", "DEPURADOR"],
        },
        "tiempo": 420,
        "vidas": 3,
        "pistas": 1,
        "color": "#ff79c6",
        "puntos_base": 40,
    },
    6: {
        "nombre": "Master",
        "tamano": 18,
        "palabras": {
            "en": ["ENCAPSULATION", "POLYMORPHISM", "ABSTRACTION", "MODULARITY", "CONSTRUCTOR", "INSTANTIATION"],
            "es": ["ENCAPSULACION", "POLIMORFISMO", "ABSTRACCION", "MODULARIDAD", "CONSTRUCTOR", "INSTANTIACION"],
        },
        "tiempo": 480,
        "vidas": 2,
        "pistas": 0,
        "color": "#bb9af7",
        "puntos_base": 50,
    },
}

FONT_FAMILY = "'Inter', 'Helvetica Neue', Arial, sans-serif"
LETTER_FONT = FONT_FAMILY
COLORS = {
    "bg": "#0b1020",
    "surface": "#101827",
    "panel": "#172033",
    "line": "#2f3d5c",
    "muted": "#565f89",
    "text": "#d7e3ff",
    "letter": "#eef6ff",
    "soft": "#9fb4d9",
    "cyan": "#00d9ff",
    "green": "#9ece6a",
    "yellow": "#e0af68",
    "orange": "#ff9e64",
    "pink": "#ff79c6",
    "purple": "#bb9af7",
    "red": "#f7768e",
    "neon": "#3bffda",
}
EASY_TIME_BONUS_PER_WORD = 5
DEFAULT_TIME_BONUS_PER_WORD = 20
EASY_BONUS_LEVELS = {1, 2}

TRANSLATIONS = {
    "en": {
        "window_title": "Word Hunt • Final Project • Valeria Góngora",
        "home_title": "WORD HUNT",
        "home_subtitle": "Search system · combos · hints · time bonus",
        "home_badge_mission": "MISSION CONTROL",
        "home_badge_core": "PYQT5 CORE",
        "home_badge_sync": "LIVE SYNC",
        "home_hero_desc": "Explore the grid, mark correct paths, and activate time bonuses based on difficulty.",
        "home_feature_challenges": "CHALLENGES",
        "home_feature_bonus": "BONUS",
        "home_feature_goal": "GOAL",
        "home_feature_levels_value": "6 LEVELS",
        "home_feature_combo_value": "HIGH COMBO",
        "home_button_start": "START GAME",
        "home_button_guide": "CHOOSE LEVEL",
        "home_footer": "Code in Place · Python + PyQt5 · Final Project · Valeria Góngora",
        "home_stat_record": "BEST SCORE",
        "home_stat_games": "GAMES",
        "home_stat_words": "WORDS",
        "home_stat_levels": "LEVELS",
        "language_label": "🇺🇸 LANGUAGE",
        "back_to_menu": "< MENU",
        "level_card_title": "LEVEL {number}",
        "level_title": "CHOOSE YOUR CHALLENGE",
        "level_subtitle": "Each level changes the board size, time, and challenge difficulty.",
        "level_header": "LEVEL {level}: {name}",
        "level_status_new": "NEW",
        "level_status_completed": "COMPLETED",
        "level_button_play": "PLAY",
        "game_exit": "X EXIT",
        "game_select_letters": "Select letters to form a word.",
        "game_confirm": "CONFIRM",
        "game_clear": "CLEAR",
        "game_hint": "HINT ({count})",
        "game_stats_title": "STATISTICS",
        "game_stats_subtitle": "Level progress",
        "game_stats_score": "POINTS",
        "game_stats_combo": "COMBO",
        "game_stats_lives": "LIVES",
        "game_words": "WORDS",
        "game_progress": "{found}/{total} · {percent}%",
        "game_found": "FOUND",
        "game_hidden": "HIDDEN",
        "game_word_found": "{word} found! +{gained} points and +{bonus}s.",
        "game_word_wrong": "Incorrect word. You lose a life.",
        "game_hint_used": "Hint: a letter from {word} was highlighted.",
        "level_hints": "{count} hints",
        "summary_victory": "VICTORY",
        "summary_defeat": "DEFEAT",
        "summary_subtitle_victory": "You completed the level and earned bonuses.",
        "summary_subtitle_defeat": "Time ran out or you ran out of lives.",
        "summary_score": "FINAL SCORE",
        "summary_bonus": "BONUS",
        "summary_combo": "BEST COMBO",
        "summary_retry": "RETRY",
        "summary_next": "NEXT",
        "summary_menu": "MENU",
        "level_info": "Board {size}x{size} • {time} • {lives} lives",
        "level_name_1": "Beginner",
        "level_name_2": "Easy",
        "level_name_3": "Intermediate",
        "level_name_4": "Advanced",
        "level_name_5": "Expert",
        "level_name_6": "Master",
    },
    "es": {
        "window_title": "Word Hunt • Proyecto Final • Valeria Góngora",
        "home_title": "WORD HUNT",
        "home_subtitle": "Búsqueda de letras · combos · pistas · bonificación de tiempo",
        "home_badge_mission": "MISIÓN",
        "home_badge_core": "NUCLEO PYQT5",
        "home_badge_sync": "SINCRONIZACIÓN",
        "home_hero_desc": "Explora la cuadrícula, marca rutas correctas y activa bonificaciones de tiempo según la dificultad.",
        "home_feature_challenges": "DESAFÍOS",
        "home_feature_bonus": "BONOS",
        "home_feature_goal": "OBJETIVO",
        "home_feature_levels_value": "6 NIVELES",
        "home_feature_combo_value": "ALTO COMBO",
        "home_button_start": "INICIAR JUEGO",
        "home_button_guide": "ELEGIR NIVEL",
        "home_footer": "Code in Place · Python + PyQt5 · Proyecto Final · Valeria Góngora",
        "home_stat_record": "MEJOR PUNTAJE",
        "home_stat_games": "JUEGOS",
        "home_stat_words": "PALABRAS",
        "home_stat_levels": "NIVELES",
        "language_label": "🇪🇸 IDIOMA",
        "back_to_menu": "< MENÚ",
        "level_card_title": "NIVEL {number}",
        "level_title": "ELIGE TU RETO",
        "level_subtitle": "Cada nivel cambia el tamaño del tablero, el tiempo y la complejidad del reto.",
        "level_header": "NIVEL {level}: {name}",
        "level_status_new": "NUEVO",
        "level_status_completed": "COMPLETADO",
        "level_button_play": "JUGAR",
        "game_exit": "X SALIR",
        "game_select_letters": "Selecciona letras para formar una palabra.",
        "game_confirm": "CONFIRMAR",
        "game_clear": "BORRAR",
        "game_hint": "PISTA ({count})",
        "game_stats_title": "ESTADÍSTICAS",
        "game_stats_subtitle": "Progreso del nivel",
        "game_stats_score": "PUNTOS",
        "game_stats_combo": "COMBO",
        "game_stats_lives": "VIDAS",
        "game_words": "PALABRAS",
        "game_progress": "{found}/{total} · {percent}%",
        "game_found": "ENCONTRADA",
        "game_hidden": "OCULTA",
        "game_word_found": "{word} encontrada! +{gained} puntos y +{bonus}s.",
        "game_word_wrong": "Palabra incorrecta. Pierdes una vida.",
        "game_hint_used": "Pista: se resaltó una letra de {word}.",
        "summary_victory": "VICTORIA",
        "summary_defeat": "DERROTA",
        "summary_subtitle_victory": "Has completado el nivel y sumaste bonificaciones.",
        "summary_subtitle_defeat": "Se agotó el tiempo o te quedaste sin vidas.",
        "summary_score": "PUNTAJE FINAL",
        "summary_bonus": "BONO",
        "summary_combo": "MEJOR COMBO",
        "summary_retry": "REINTENTAR",
        "summary_next": "SIGUIENTE",
        "summary_menu": "MENÚ",
        "level_info": "Tablero {size}x{size} • {time} • {lives} vidas",
        "level_hints": "{count} pistas",
        "level_name_1": "Principiante",
        "level_name_2": "Fácil",
        "level_name_3": "Intermedio",
        "level_name_4": "Avanzado",
        "level_name_5": "Experto",
        "level_name_6": "Maestro",
    },
}


def _format_translation(text, **kwargs):
    try:
        return text.format(**kwargs)
    except KeyError:
        return text


def crear_matriz_vacia(tamano):
    return [["" for _ in range(tamano)] for _ in range(tamano)]


def obtener_direcciones():
    return [
        (0, 1),
        (1, 0),
        (1, 1),
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


def generar_tablero(tamano, palabras, max_reintentos=6):
    palabras_ordenadas = sorted(palabras, key=len, reverse=True)
    for intento in range(max_reintentos):
        tablero = crear_matriz_vacia(tamano)
        posiciones_palabras = {}
        palabras_colocadas = []
        correcto = True
        for palabra in palabras_ordenadas:
            posiciones = insertar_palabra_en_tablero(tablero, palabra, max_intentos=200)
            if posiciones is None:
                correcto = False
                break
            posiciones_palabras[palabra] = posiciones
            palabras_colocadas.append(palabra)
        if correcto:
            rellenar_tablero_con_letras(tablero)
            return tablero, posiciones_palabras, palabras_colocadas
    # Fallback: place as many as possible, but keep allowed directions
    tablero = crear_matriz_vacia(tamano)
    posiciones_palabras = {}
    palabras_colocadas = []
    for palabra in palabras_ordenadas:
        posiciones = insertar_palabra_en_tablero(tablero, palabra, max_intentos=300)
        if posiciones:
            posiciones_palabras[palabra] = posiciones
            palabras_colocadas.append(palabra)
    rellenar_tablero_con_letras(tablero)
    return tablero, posiciones_palabras, palabras_colocadas


def formatear_tiempo(segundos):
    minutos = segundos // 60
    segs = segundos % 60
    return f"{minutos:02d}:{segs:02d}"


def normalizar_paso(valor):
    if valor == 0:
        return 0
    return 1 if valor > 0 else -1


def obtener_palabras_del_nivel(level_number, language="en"):
    config = NIVELES.get(level_number, {})
    palabras = config.get("palabras", [])
    if isinstance(palabras, dict):
        return palabras.get(language, palabras.get("en", []))
    return palabras


class WordHuntApp(QMainWindow):
    def t(self, key, **kwargs):
        language = getattr(self, "current_language", "en")
        text = TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)
        return _format_translation(text, **kwargs)

    def set_language(self, language):
        language = language if language in TRANSLATIONS else "en"
        self.current_language = language
        if hasattr(self, "language_selector"):
            self.language_selector.blockSignals(True)
            self.language_selector.setCurrentIndex(0 if language == "en" else 1)
            self.language_selector.blockSignals(False)
        self.retranslate_ui()
        if getattr(self, "stacked", None) is not None and getattr(self, "game_page", None) is not None:
            if self.stacked.currentWidget() == self.game_page and getattr(self, "current_level", None):
                self.start_level(self.current_level)

    def on_language_selected(self, index):
        language = self.language_selector.itemData(index)
        self.set_language(language)

    def _level_name(self, level_number):
        return self.t(f"level_name_{level_number}")

    def retranslate_ui(self):
        self.setWindowTitle(self.t("window_title"))

        if hasattr(self, "home_title"):
            self.home_title.setText(self.t("home_title"))
        if hasattr(self, "home_subtitle"):
            self.home_subtitle.setText(self.t("home_subtitle"))
        if hasattr(self, "home_badge_labels"):
            for badge, key in zip(self.home_badge_labels, ("home_badge_mission", "home_badge_core", "home_badge_sync")):
                badge.setText(self.t(key))
        if hasattr(self, "home_hero_desc"):
            self.home_hero_desc.setText(self.t("home_hero_desc"))
        if hasattr(self, "home_start_btn"):
            self.home_start_btn.setText(self.t("home_button_start"))
        if hasattr(self, "home_guide_btn"):
            self.home_guide_btn.setText(self.t("home_button_guide"))
        if hasattr(self, "home_footer"):
            self.home_footer.setText(self.t("home_footer"))

        if hasattr(self, "home_score_card"):
            self.home_score_card.title_label.setText(self.t("home_stat_record"))
        if hasattr(self, "home_games_card"):
            self.home_games_card.title_label.setText(self.t("home_stat_games"))
        if hasattr(self, "home_words_card"):
            self.home_words_card.title_label.setText(self.t("home_stat_words"))
        if hasattr(self, "home_levels_card"):
            self.home_levels_card.title_label.setText(self.t("home_stat_levels"))

        if hasattr(self, "language_label"):
            self.language_label.setText(self.t("language_label"))
        if hasattr(self, "language_selector"):
            self.language_selector.blockSignals(True)
            self.language_selector.setItemText(0, "🇺🇸 English")
            self.language_selector.setItemText(1, "🇪🇸 Español")
            self.language_selector.setCurrentIndex(0 if self.current_language == "en" else 1)
            self.language_selector.blockSignals(False)

        if hasattr(self, "level_title"):
            self.level_title.setText(self.t("level_title"))
        if hasattr(self, "level_subtitle"):
            self.level_subtitle.setText(self.t("level_subtitle"))
        if hasattr(self, "level_back_btn"):
            self.level_back_btn.setText(self.t("back_to_menu"))
        if hasattr(self, "level_cards"):
            for number, card in self.level_cards.items():
                refs = getattr(self, "level_card_refs", {}).get(number)
                if not refs:
                    continue
                refs["status"].setText(self.t("level_status_completed") if self.level_status.get(number) == "COMPLETADO" else self.t("level_status_new"))
                refs["title"].setText(self.t("level_card_title", number=number))
                status_color = COLORS["green"] if self.level_status.get(number) == "COMPLETADO" else COLORS["cyan"]
                refs["status"].setStyleSheet(f"background-color: transparent; border: none; color: {status_color}; font-family: {FONT_FAMILY}; font-size: 10px; font-weight: 900;")
                display_name = self._level_name(number)
                refs["name"].setText(display_name.upper())
                config = NIVELES[number]
                refs["info"].setText(self.t("level_info", size=config["tamano"], time=formatear_tiempo(config["tiempo"]), lives=config["vidas"]))
                refs["hints"].setText(self.t("level_hints", count=config["pistas"]))
                refs["points"].setText(f"{config['puntos_base']} pts")
                refs["bonus"].setText(f"+{self._time_bonus_for_level(number)}s")
                refs["button"].setText(self.t("level_button_play"))

        if hasattr(self, "confirm_btn"):
            self.confirm_btn.setText(self.t("game_confirm"))
        if hasattr(self, "clear_btn"):
            self.clear_btn.setText(self.t("game_clear"))
        if hasattr(self, "hint_btn"):
            self.hint_btn.setText(self.t("game_hint", count=self.hints_left))
        if hasattr(self, "status_label"):
            if self.status_label.text() in ["Selecciona letras para formar una palabra.", "Select letters to form a word."]:
                self.status_label.setText(self.t("game_select_letters"))
        if hasattr(self, "game_words_title"):
            self.game_words_title.setText(self.t("game_words"))
        if hasattr(self, "game_stats_title"):
            self.game_stats_title.setText(self.t("game_stats_title"))
        if hasattr(self, "game_stats_subtitle"):
            self.game_stats_subtitle.setText(self.t("game_stats_subtitle"))
        if hasattr(self, "progress_label"):
            self._refresh_progress()
        if hasattr(self, "score_card"):
            self.score_card.title_label.setText(self.t("game_stats_score"))
        if hasattr(self, "combo_card"):
            self.combo_card.title_label.setText(self.t("game_stats_combo"))
        if hasattr(self, "lives_card"):
            self.lives_card.title_label.setText(self.t("game_stats_lives"))

        if hasattr(self, "summary_title"):
            if self.summary_result == "victory":
                self.summary_title.setText(self.t("summary_victory"))
            else:
                self.summary_title.setText(self.t("summary_defeat"))
        if hasattr(self, "summary_subtitle"):
            if self.summary_result == "victory":
                self.summary_subtitle.setText(self.t("summary_subtitle_victory"))
            else:
                self.summary_subtitle.setText(self.t("summary_subtitle_defeat"))
        if hasattr(self, "summary_score"):
            self.summary_score.title_label.setText(self.t("summary_score"))
        if hasattr(self, "summary_bonus"):
            self.summary_bonus.title_label.setText(self.t("summary_bonus"))
        if hasattr(self, "summary_combo"):
            self.summary_combo.title_label.setText(self.t("summary_combo"))
        if hasattr(self, "summary_retry_btn"):
            self.summary_retry_btn.setText(self.t("summary_retry"))
        if hasattr(self, "summary_next_btn"):
            self.summary_next_btn.setText(self.t("summary_next"))
        if hasattr(self, "summary_menu_btn"):
            self.summary_menu_btn.setText(self.t("summary_menu"))

    def _refresh_level_card_texts(self, number):
        refs = getattr(self, "level_card_refs", {}).get(number)
        if not refs:
            return
        refs["title"].setText(self.t("level_card_title", number=number))
        status_text = self.t("level_status_completed") if self.level_status.get(number) == "COMPLETADO" else self.t("level_status_new")
        status_color = COLORS["green"] if self.level_status.get(number) == "COMPLETADO" else COLORS["cyan"]
        refs["status"].setText(status_text)
        refs["status"].setStyleSheet(f"background-color: transparent; border: none; color: {status_color}; font-family: {FONT_FAMILY}; font-size: 10px; font-weight: 900;")
        refs["name"].setText(self._level_name(number).upper())
        config = NIVELES[number]
        refs["info"].setText(self.t("level_info", size=config["tamano"], time=formatear_tiempo(config["tiempo"]), lives=config["vidas"]))
        refs["hints"].setText(self.t("level_hints", count=config["pistas"]))
        refs["points"].setText(f"{config['puntos_base']} pts")
        refs["bonus"].setText(f"+{self._time_bonus_for_level(number)}s")
        refs["button"].setText(self.t("level_button_play"))

    def _translate_level_context(self, level_number):
        return self._level_name(level_number)

    def _get_level_display_name(self, level_number):
        return self._level_name(level_number)

    def _refresh_summary_texts(self):
        if getattr(self, "summary_title", None):
            if self.summary_title.text() in ["VICTORIA", "VICTORY"]:
                self.summary_title.setText(self.t("summary_victory"))
            elif self.summary_title.text() in ["DERROTA", "DEFEAT"]:
                self.summary_title.setText(self.t("summary_defeat"))
        if getattr(self, "summary_subtitle", None):
            current_text = self.summary_subtitle.text()
            victory_texts = {self.t("summary_subtitle_victory")}
            defeat_texts = {self.t("summary_subtitle_defeat")}
            if current_text in victory_texts:
                self.summary_subtitle.setText(self.t("summary_subtitle_victory"))
            elif current_text in defeat_texts:
                self.summary_subtitle.setText(self.t("summary_subtitle_defeat"))

    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.setWindowTitle(self.t("window_title"))
        self.resize(1220, 760)
        self.setMinimumSize(1040, 720)
        self.setStyleSheet(f"QMainWindow {{ background-color: {COLORS['bg']}; }}")

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
        self.summary_result = "victory"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick_timer)

        self.confetti_timer = QTimer(self)
        self.confetti_timer.timeout.connect(self._animate_confetti)

        self._audio_temp_paths = []
        self.success_sound = self._create_sound_effect([
            (659, 120),
            (784, 120),
            (1047, 220),
        ], volume=0.18)
        self.error_sound = self._create_sound_effect([
            (220, 140),
            (196, 140),
            (174, 260),
        ], volume=0.20)
        self.level_complete_sound = self._create_sound_effect([
            (523, 100),
            (659, 100),
            (784, 120),
            (1047, 220),
            (988, 180),
            (1047, 220),
        ], volume=0.18)
        self.ui_click_sound = self._create_sound_effect([
            (698, 45),
            (784, 45),
        ], volume=0.10)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        self._build_home_view()
        self._build_level_view()
        self._build_game_view()
        self._build_summary_view()
        self.retranslate_ui()

        self.show_screen("home")

    def _card_style(self, color, bg=None):
        bg = bg or COLORS["panel"]
        return (
            f"background-color: {bg}; border: 1px solid {color}; border-radius: 10px;"
        )

    def _button_style(self, bg_color, text_color=None):
        text_color = text_color or COLORS["surface"]
        return (
            f"QPushButton {{ background-color: {bg_color}; color: {text_color}; border: 1px solid {bg_color}; border-radius: 10px; "
            f"padding: 10px 16px; min-height: 42px; font-family: {FONT_FAMILY}; font-weight: 700; font-size: 13px; }}"
            f"QPushButton:hover {{ background-color: {COLORS['cyan']}; border-color: {COLORS['cyan']}; }}"
            "QPushButton:pressed { padding-top: 11px; padding-bottom: 9px; }"
        )

    def _chip_style(self, color):
        return (
            f"background-color: {COLORS['surface']}; color: {color}; border: 1px solid {color}; "
            f"border-radius: 8px; padding: 7px 10px; font-family: {FONT_FAMILY}; font-size: 10px; font-weight: 800;"
        )

    def _page(self):
        page = QWidget()
        page.setStyleSheet(
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #090f1a, stop:0.5 {COLORS['bg']}, stop:1 #081020);"
        )
        return page

    def _label(self, text, color=None, size=12, weight=500):
        label = QLabel(text)
        label.setStyleSheet(
            f"background-color: transparent; border: none; color: {color or COLORS['text']}; "
            f"font-family: {FONT_FAMILY}; font-size: {size}px; font-weight: {weight};"
        )
        return label

    def _feature_row(self, title, value, accent):
        row = QFrame()
        row.setStyleSheet(
            f"background-color: {COLORS['surface']}; border: 1px solid {COLORS['line']}; border-radius: 8px;"
        )
        layout = QHBoxLayout(row)
        layout.setContentsMargins(12, 9, 12, 9)
        label = self._label(title, COLORS["soft"], 11, 800)
        result = self._label(value, accent, 13, 900)
        result.setStyleSheet(
            f"background-color: transparent; border: none; color: {accent}; "
            f"font-family: {LETTER_FONT}; font-size: 13px; font-weight: 900;"
        )
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(result)
        return row

    def _add_glow(self, widget, color, blur=24):
        glow = QGraphicsDropShadowEffect(widget)
        glow.setBlurRadius(blur)
        glow.setColor(QColor(color))
        glow.setOffset(0, 0)
        widget.setGraphicsEffect(glow)

    def _time_bonus_for_level(self, level_number):
        if level_number in EASY_BONUS_LEVELS:
            return EASY_TIME_BONUS_PER_WORD
        return DEFAULT_TIME_BONUS_PER_WORD

    def _build_home_view(self):
        page = self._page()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(42, 30, 42, 24)
        layout.setSpacing(16)

        header = QFrame()
        header.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.home_title = QLabel(self.t("home_title"))
        self.home_title.setStyleSheet(f"color: {COLORS['cyan']}; font-family: {FONT_FAMILY}; font-size: 56px; font-weight: 900;")
        self.home_title.setAlignment(Qt.AlignCenter)
        self._add_glow(self.home_title, COLORS["cyan"], 36)
        header_layout.addWidget(self.home_title)

        self.home_subtitle = QLabel(self.t("home_subtitle"))
        self.home_subtitle.setStyleSheet(f"color: {COLORS['soft']}; font-family: {FONT_FAMILY}; font-size: 14px; font-weight: 700;")
        self.home_subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.home_subtitle)

        hero = QFrame()
        hero.setStyleSheet(f"background-color: rgba(23, 32, 51, 235); border-radius: 12px; border: 1px solid {COLORS['cyan']};")
        hero.setMaximumHeight(610)
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 20, 24, 20)
        hero_layout.setSpacing(16)

        hero_badges = QHBoxLayout()
        hero_badges.setSpacing(10)
        self.home_badge_labels = []
        badge1 = QLabel(self.t("home_badge_mission"))
        badge1.setStyleSheet(self._chip_style(COLORS["neon"]))
        badge2 = QLabel(self.t("home_badge_core"))
        badge2.setStyleSheet(self._chip_style(COLORS["yellow"]))
        badge3 = QLabel(self.t("home_badge_sync"))
        badge3.setStyleSheet(self._chip_style(COLORS["green"]))
        self.home_badge_labels.extend([badge1, badge2, badge3])
        hero_badges.addWidget(badge1)
        hero_badges.addWidget(badge2)
        hero_badges.addWidget(badge3)

        self.language_label = QLabel(self.t("language_label"))
        self.language_label.setStyleSheet(f"background-color: {COLORS['surface']}; color: {COLORS['soft']}; border: 1px solid {COLORS['line']}; border-radius: 8px; padding: 6px 10px; font-family: {FONT_FAMILY}; font-size: 10px; font-weight: 800;")

        self.language_selector = QComboBox()
        self.language_selector.addItem("🇺🇸 English", "en")
        self.language_selector.addItem("🇪🇸 Español", "es")
        self.language_selector.setCurrentIndex(0)
        self.language_selector.setEnabled(True)
        self.language_selector.currentIndexChanged.connect(self.on_language_selected)
        self.language_selector.setStyleSheet(
            f"QComboBox {{ background-color: {COLORS['surface']}; color: {COLORS['text']}; border: 1px solid {COLORS['line']}; border-radius: 8px; padding: 5px 12px; font-family: {FONT_FAMILY}; font-size: 13px; font-weight: 800; min-width: 120px; }}"
            f"QComboBox::drop-down {{ border: none; }}"
            f"QComboBox QAbstractItemView {{ background-color: {COLORS['surface']}; color: {COLORS['text']}; selection-background-color: {COLORS['cyan']}; font-size: 13px; font-weight: 800; }}"
        )
        hero_badges.addWidget(self.language_label)
        hero_badges.addWidget(self.language_selector)
        hero_badges.addStretch()
        hero_layout.addLayout(hero_badges)

        center_row = QHBoxLayout()
        center_row.setSpacing(24)

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
                    f"background-color: {COLORS['surface']}; color: {COLORS['letter']}; border: 1px solid {COLORS['cyan']}; "
                    f"border-radius: 7px; min-width: 46px; min-height: 46px; font-family: {LETTER_FONT}; font-weight: 900; font-size: 20px;"
                )
                self._add_glow(cell, COLORS["cyan"], 12)
                preview_layout.addWidget(cell, r, c)

        intro_col = QVBoxLayout()
        intro_col.setSpacing(12)
        self.home_hero_desc = QLabel(self.t("home_hero_desc"))
        self.home_hero_desc.setWordWrap(True)
        self.home_hero_desc.setStyleSheet(
            f"background-color: transparent; border: none; color: {COLORS['text']}; "
            f"font-family: {FONT_FAMILY}; font-size: 16px; font-weight: 600; line-height: 1.5;"
        )
        intro_col.addWidget(self.home_hero_desc)
        intro_col.addWidget(self._feature_row(self.t("home_feature_challenges"), self.t("home_feature_levels_value"), COLORS["cyan"]))
        intro_col.addWidget(self._feature_row(self.t("home_feature_bonus"), "+5s / +20s", COLORS["neon"]))
        intro_col.addWidget(self._feature_row(self.t("home_feature_goal"), self.t("home_feature_combo_value"), COLORS["yellow"]))
        center_row.addWidget(hero_grid, 0, Qt.AlignLeft)
        center_row.addLayout(intro_col, 1)
        hero_layout.addLayout(center_row)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(10)
        self.home_score_card = self._create_stat_card(self.t("home_stat_record"), str(self.best_score), COLORS["yellow"])
        self.home_games_card = self._create_stat_card(self.t("home_stat_games"), str(self.games_played), COLORS["cyan"])
        self.home_words_card = self._create_stat_card(self.t("home_stat_words"), str(self.total_words_found), COLORS["green"])
        self.home_levels_card = self._create_stat_card(self.t("home_stat_levels"), "0/6", COLORS["purple"])
        stats_row.addWidget(self.home_score_card)
        stats_row.addWidget(self.home_games_card)
        stats_row.addWidget(self.home_words_card)
        stats_row.addWidget(self.home_levels_card)
        hero_layout.addLayout(stats_row)

        buttons_row = QHBoxLayout()
        self.home_start_btn = QPushButton(self.t("home_button_start"))
        self.home_start_btn.setStyleSheet(self._button_style(COLORS["green"], COLORS["surface"]))
        self.home_start_btn.clicked.connect(lambda: (self._play_ui_click(), self.show_screen("level")))
        self.home_guide_btn = QPushButton(self.t("home_button_guide"))
        self.home_guide_btn.setStyleSheet(self._button_style(COLORS["cyan"], COLORS["surface"]))
        self.home_guide_btn.clicked.connect(lambda: (self._play_ui_click(), self.show_screen("level")))
        buttons_row.addWidget(self.home_start_btn)
        buttons_row.addWidget(self.home_guide_btn)
        buttons_row.addStretch()
        hero_layout.addLayout(buttons_row)

        layout.addWidget(header)
        layout.addWidget(hero)

        self.home_footer = QLabel(self.t("home_footer"))
        self.home_footer.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['muted']}; font-family: {FONT_FAMILY}; font-size: 11px;")
        layout.addWidget(self.home_footer, alignment=Qt.AlignLeft)

        self.home_page = page
        self.stacked.addWidget(page)

    def _build_level_view(self):
        page = self._page()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(34, 28, 34, 28)
        layout.setSpacing(16)

        top = QHBoxLayout()
        back_btn = QPushButton(self.t("back_to_menu"))
        back_btn.setStyleSheet(self._button_style(COLORS["panel"], COLORS["cyan"]))
        back_btn.clicked.connect(lambda: (self._play_ui_click(), self.show_screen("home")))
        self.level_back_btn = back_btn
        top.addWidget(back_btn)

        self.level_title = QLabel(self.t("level_title"))
        self.level_title.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['text']}; font-family: {FONT_FAMILY}; font-size: 36px; font-weight: 900;")
        top.addWidget(self.level_title)
        top.addStretch()
        layout.addLayout(top)

        self.level_subtitle = QLabel(self.t("level_subtitle"))
        self.level_subtitle.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['soft']}; font-family: {FONT_FAMILY}; font-size: 14px; font-weight: 600;")
        layout.addWidget(self.level_subtitle)

        grid = QGridLayout()
        grid.setSpacing(16)
        self.level_cards = {}
        self.level_card_refs = {}
        for number, config in NIVELES.items():
            time_bonus = self._time_bonus_for_level(number)
            card = QFrame()
            card.setStyleSheet(self._card_style(config["color"]))
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(18, 18, 18, 18)
            card_layout.setSpacing(10)

            status = QLabel(self.t("level_status_completed") if self.level_status.get(number) == "COMPLETADO" else self.t("level_status_new"))
            status_color = COLORS["green"] if self.level_status.get(number) == "COMPLETADO" else COLORS["cyan"]
            status.setStyleSheet(f"background-color: transparent; border: none; color: {status_color}; font-family: {FONT_FAMILY}; font-size: 10px; font-weight: 900;")
            card_layout.addWidget(status, alignment=Qt.AlignRight)

            title_label = QLabel(self.t("level_card_title", number=number))
            title_label.setStyleSheet(f"background-color: transparent; border: none; color: {config['color']}; font-family: {FONT_FAMILY}; font-size: 11px; font-weight: 900;")
            card_layout.addWidget(title_label)

            nome = QLabel(self._level_name(number).upper())
            nome.setStyleSheet(f"background-color: transparent; border: none; color: {config['color']}; font-family: {FONT_FAMILY}; font-size: 26px; font-weight: 900;")
            card_layout.addWidget(nome)

            info = QLabel(self.t("level_info", size=config["tamano"], time=formatear_tiempo(config["tiempo"]), lives=config["vidas"]))
            info.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['text']}; font-family: {FONT_FAMILY}; font-size: 12px; font-weight: 700;")
            info.setWordWrap(True)
            card_layout.addWidget(info)

            tags = QHBoxLayout()
            hints = QLabel(self.t("level_hints", count=config["pistas"]))
            hints.setStyleSheet(f"background-color: {COLORS['surface']}; color: {COLORS['purple']}; border-radius: 8px; padding: 6px 9px; font-family: {FONT_FAMILY}; font-size: 9px; font-weight: 800;")
            points = QLabel(f"{config['puntos_base']} pts")
            points.setStyleSheet(f"background-color: {COLORS['surface']}; color: {COLORS['orange']}; border-radius: 8px; padding: 6px 9px; font-family: {FONT_FAMILY}; font-size: 9px; font-weight: 800;")
            bonus = QLabel(f"+{time_bonus}s")
            bonus.setStyleSheet(f"background-color: {COLORS['surface']}; color: {COLORS['neon']}; border-radius: 8px; padding: 6px 9px; font-family: {FONT_FAMILY}; font-size: 9px; font-weight: 800;")
            tags.addWidget(hints)
            tags.addWidget(points)
            tags.addWidget(bonus)
            tags.addStretch()
            card_layout.addLayout(tags)

            play_btn = QPushButton(self.t("level_button_play"))
            play_btn.setStyleSheet(self._button_style(config["color"], COLORS["surface"]))
            play_btn.clicked.connect(lambda checked=False, n=number: (self._play_ui_click(), self.start_level(n)))
            card_layout.addWidget(play_btn)

            row = (number - 1) // 3
            col = (number - 1) % 3
            grid.addWidget(card, row, col)
            self.level_cards[number] = card
            self.level_card_refs[number] = {
                "status": status,
                "title": title_label,
                "name": nome,
                "info": info,
                "hints": hints,
                "points": points,
                "bonus": bonus,
                "button": play_btn,
            }

        layout.addLayout(grid)
        self.level_page = page
        self.stacked.addWidget(page)

    def _build_game_view(self):
        page = self._page()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        header = QFrame()
        header.setStyleSheet(f"background-color: rgba(16, 24, 39, 205); border: 1px solid {COLORS['line']}; border-radius: 10px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 7, 10, 7)

        back_btn = QPushButton(self.t("game_exit"))
        back_btn.setStyleSheet(self._button_style(COLORS["surface"], COLORS["red"]))
        back_btn.clicked.connect(lambda: (self._play_ui_click(), self.show_screen("level")))
        header_layout.addWidget(back_btn)

        self.level_header = QLabel("")
        self.level_header.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['text']}; font-family: {FONT_FAMILY}; font-size: 20px; font-weight: 800;")
        header_layout.addWidget(self.level_header)
        header_layout.addStretch()

        self.timer_label = QLabel("03:00")
        self.timer_label.setStyleSheet(f"background-color: {COLORS['surface']}; color: {COLORS['neon']}; border: 1px solid {COLORS['cyan']}; border-radius: 10px; padding: 8px 16px; font-family: {FONT_FAMILY}; font-size: 24px; font-weight: 900;")
        self._add_glow(self.timer_label, COLORS["cyan"], 18)
        header_layout.addWidget(self.timer_label)

        layout.addWidget(header)

        content = QHBoxLayout()
        content.setSpacing(14)

        left_panel = QFrame()
        left_panel.setStyleSheet(f"background-color: rgba(16, 24, 39, 235); border-radius: 12px; border: 1px solid {COLORS['cyan']};")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        timer_progress = QFrame()
        timer_progress.setStyleSheet(f"background-color: {COLORS['panel']}; border-radius: 5px;")
        timer_progress.setFixedHeight(8)
        timer_progress_layout = QHBoxLayout(timer_progress)
        timer_progress_layout.setContentsMargins(0,0,0,0)
        self.time_fill = QFrame()
        self.time_fill.setStyleSheet(f"background-color: {COLORS['cyan']}; border-radius: 5px;")
        self.time_fill.setFixedWidth(0)
        timer_progress_layout.addWidget(self.time_fill)
        left_layout.addWidget(timer_progress)

        board_card = QFrame()
        board_card.setStyleSheet(f"background-color: {COLORS['panel']}; border-radius: 10px; border: 1px solid {COLORS['neon']};")
        board_layout = QVBoxLayout(board_card)
        board_layout.setContentsMargins(8, 8, 8, 8)

        self.board_widget = QWidget()
        self.board_grid = QGridLayout(self.board_widget)
        self.board_grid.setSpacing(6)
        self.board_grid.setContentsMargins(0,0,0,0)
        board_layout.addWidget(self.board_widget, alignment=Qt.AlignCenter)
        left_layout.addWidget(board_card, 1)

        controls = QFrame()
        controls.setStyleSheet(f"background-color: {COLORS['surface']}; border: 1px solid {COLORS['line']}; border-radius: 8px;")
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(10, 7, 10, 7)

        self.word_preview = QLabel("")
        self.word_preview.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['yellow']}; font-family: {FONT_FAMILY}; font-size: 24px; font-weight: 900;")
        self.word_preview.setMinimumHeight(26)
        self._add_glow(self.word_preview, COLORS["yellow"], 18)
        controls_layout.addWidget(self.word_preview)

        controls_layout.addStretch()

        self.status_label = QLabel(self.t("game_select_letters"))
        self.status_label.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['soft']}; font-family: {FONT_FAMILY}; font-size: 11px; font-weight: 700;")
        controls_layout.addWidget(self.status_label, alignment=Qt.AlignRight)
        left_layout.addWidget(controls)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.confirm_btn = QPushButton(self.t("game_confirm"))
        self.confirm_btn.setStyleSheet(self._button_style(COLORS["green"], COLORS["surface"]))
        self.confirm_btn.clicked.connect(lambda: (self._play_ui_click(), self.confirm_selection()))
        actions.addWidget(self.confirm_btn)

        self.clear_btn = QPushButton(self.t("game_clear"))
        self.clear_btn.setStyleSheet(self._button_style(COLORS["red"], COLORS["surface"]))
        self.clear_btn.clicked.connect(lambda: (self._play_ui_click(), self.clear_selection()))
        actions.addWidget(self.clear_btn)

        self.hint_btn = QPushButton(self.t("game_hint", count=0))
        self.hint_btn.setStyleSheet(self._button_style(COLORS["purple"], COLORS["surface"]))
        self.hint_btn.clicked.connect(lambda: (self._play_ui_click(), self.use_hint()))
        actions.addWidget(self.hint_btn)
        left_layout.addLayout(actions)

        right_panel = QFrame()
        right_panel.setStyleSheet(f"background-color: rgba(23, 32, 51, 235); border-radius: 12px; border: 1px solid {COLORS['line']};")
        right_panel.setMinimumWidth(286)
        right_panel.setMaximumWidth(300)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(14, 14, 14, 14)
        right_layout.setSpacing(9)

        self.game_stats_title = self._label(self.t("game_stats_title"), COLORS["text"], 14, 900)
        self.game_stats_title.setText(self.t("game_stats_title"))
        right_layout.addWidget(self.game_stats_title, alignment=Qt.AlignLeft)
        self.game_stats_subtitle = self._label(self.t("game_stats_subtitle"), COLORS["soft"], 11, 800)
        right_layout.addWidget(self.game_stats_subtitle, alignment=Qt.AlignLeft)

        self.score_card = self._create_stat_card(self.t("game_stats_score"), "0", COLORS["yellow"])
        self.combo_card = self._create_stat_card(self.t("game_stats_combo"), "x0", COLORS["orange"])
        self.lives_card = self._create_stat_card(self.t("game_stats_lives"), "●●●", COLORS["red"])
        self.score_value_label = self.score_card.value_label
        self.combo_value_label = self.combo_card.value_label
        self.lives_value_label = self.lives_card.value_label
        right_layout.addWidget(self.score_card)
        right_layout.addWidget(self.combo_card)
        right_layout.addWidget(self.lives_card)

        self.game_words_title = QLabel(self.t("game_words"))
        self.game_words_title.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['text']}; font-family: {FONT_FAMILY}; font-size: 13px; font-weight: 900;")
        right_layout.addWidget(self.game_words_title)

        self.words_container = QWidget()
        self.words_layout = QVBoxLayout(self.words_container)
        self.words_layout.setContentsMargins(0,0,0,0)
        self.words_layout.setSpacing(6)
        self.words_scroll = QScrollArea()
        self.words_scroll.setWidgetResizable(True)
        self.words_scroll.setStyleSheet("background-color: transparent; border: none;")
        self.words_scroll.setWidget(self.words_container)
        right_layout.addWidget(self.words_scroll)

        self.progress_label = QLabel(self.t("game_progress", found=0, total=0, percent=0))
        self.progress_label.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['cyan']}; font-family: {FONT_FAMILY}; font-size: 13px; font-weight: 900;")
        right_layout.addWidget(self.progress_label)

        content.addWidget(left_panel, 4)
        content.addWidget(right_panel, 1)

        layout.addLayout(content)
        self.game_page = page
        self.stacked.addWidget(page)

    def _build_summary_view(self):
        page = self._page()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 36, 40, 36)
        layout.setSpacing(24)

        self.summary_title = QLabel(self.t("summary_victory"))
        self.summary_title.setAlignment(Qt.AlignCenter)
        self.summary_title.setStyleSheet(
            f"background-color: transparent; border: none; color: {COLORS['green']}; font-family: {FONT_FAMILY}; font-size: 58px; font-weight: 900; letter-spacing: 1px;"
        )
        layout.addWidget(self.summary_title)

        self.summary_subtitle = QLabel(self.t("summary_subtitle_victory"))
        self.summary_subtitle.setAlignment(Qt.AlignCenter)
        self.summary_subtitle.setWordWrap(True)
        self.summary_subtitle.setStyleSheet(
            f"background-color: transparent; border: none; color: {COLORS['soft']}; font-family: {FONT_FAMILY}; font-size: 18px; font-weight: 600; line-height: 1.5; margin-bottom: 8px;"
        )
        layout.addWidget(self.summary_subtitle)

        layout.addSpacing(20)
        summary_cards = QHBoxLayout()
        summary_cards.setSpacing(20)
        summary_cards.addStretch()
        self.summary_score = self._create_stat_card(self.t("summary_score"), "0", COLORS["yellow"])
        self.summary_bonus = self._create_stat_card(self.t("summary_bonus"), "0", COLORS["cyan"])
        self.summary_combo = self._create_stat_card(self.t("summary_combo"), "x0", COLORS["orange"])
        self.summary_score.setMinimumHeight(120)
        self.summary_bonus.setMinimumHeight(120)
        self.summary_combo.setMinimumHeight(120)
        self.summary_score.setMinimumWidth(120)
        self.summary_bonus.setMinimumWidth(120)
        self.summary_combo.setMinimumWidth(120)
        summary_cards.addWidget(self.summary_score)
        summary_cards.addWidget(self.summary_bonus)
        summary_cards.addWidget(self.summary_combo)
        summary_cards.addStretch()
        layout.addLayout(summary_cards)

        action_row = QHBoxLayout()
        action_row.setSpacing(18)
        action_row.addStretch()
        retry_btn = QPushButton(self.t("summary_retry"))
        retry_btn.setStyleSheet(self._button_style(COLORS["cyan"], COLORS["surface"]))
        retry_btn.setMinimumWidth(120)
        retry_btn.clicked.connect(lambda: (self._play_ui_click(), self.retry_level()))
        self.summary_retry_btn = retry_btn
        next_btn = QPushButton(self.t("summary_next"))
        next_btn.setStyleSheet(self._button_style(COLORS["green"], COLORS["surface"]))
        next_btn.setMinimumWidth(110)
        next_btn.clicked.connect(lambda: (self._play_ui_click(), self.next_level()))
        self.summary_next_btn = next_btn
        menu_btn = QPushButton(self.t("summary_menu"))
        menu_btn.setStyleSheet(self._button_style(COLORS["purple"], COLORS["surface"]))
        menu_btn.setMinimumWidth(110)
        menu_btn.clicked.connect(lambda: (self._play_ui_click(), self.show_screen("home")))
        self.summary_menu_btn = menu_btn
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

        # Ajuste de estilos dinámico según resultado
        def update_summary_styles():
            if getattr(self, "summary_result", "victory") == "victory":
                self.summary_title.setText(self.t("summary_victory"))
                self.summary_title.setStyleSheet(
                    f"color: {COLORS['green']}; font-family: {LETTER_FONT}; font-size: 58px; font-weight: 900; letter-spacing: 1px; text-shadow: 0 2px 16px {COLORS['green']};"
                )
                self.summary_subtitle.setText(self.t("summary_subtitle_victory"))
                self.summary_subtitle.setStyleSheet(
                    f"color: {COLORS['soft']}; font-family: {FONT_FAMILY}; font-size: 18px; font-weight: 700; line-height: 1.5; margin: 0 0 16px 0;"
                )
                self._launch_confetti()
            else:
                self.summary_title.setText(self.t("summary_defeat"))
                self.summary_title.setStyleSheet(
                    f"color: {COLORS['red']}; font-family: {LETTER_FONT}; font-size: 58px; font-weight: 900; letter-spacing: 1px; text-shadow: 0 2px 12px rgba(255, 0, 0, 0.22);"
                )
                self.summary_subtitle.setText(self.t("summary_subtitle_defeat"))
                self.summary_subtitle.setStyleSheet(
                    f"color: {COLORS['soft']}; font-family: {FONT_FAMILY}; font-size: 18px; font-weight: 700; line-height: 1.5; margin: 0 0 16px 0;"
                )
                self.confetti_layer.hide()
        self.update_summary_styles = update_summary_styles

        self.summary_page = page
        self.stacked.addWidget(page)

    def _launch_confetti(self):
        self.confetti_layer.show()
        self.confetti_layer.raise_()
        self.confetti_layer.setGeometry(0, 0, self.width(), self.height())
        for particle in self.confetti_particles:
            particle["widget"].deleteLater()
        self.confetti_particles = []

        colors = [COLORS["green"], COLORS["cyan"], COLORS["yellow"], COLORS["orange"], COLORS["purple"], COLORS["red"], COLORS["pink"]]
        for _ in range(48):
            particle = QLabel(random.choice(["✦", "●", "★", "❇"]))
            particle.setAttribute(Qt.WA_TransparentForMouseEvents)
            particle.setStyleSheet(f"color: {random.choice(colors)}; font-family: {FONT_FAMILY}; font-size: 18px; font-weight: 800;")
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

    def _write_wave(self, samples, sample_rate, volume):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.close()
        file_path = temp_file.name
        with wave.open(file_path, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            sample_values = []
            for sample in samples:
                sample_value = max(-32767, min(32767, int(sample * 32767 * volume)))
                sample_values.append(sample_value)
            wav_file.writeframes(struct.pack("<" + "h" * len(sample_values), *sample_values))
        self._audio_temp_paths.append(file_path)
        return file_path

    def _create_sound_effect(self, notes, volume=0.2, sample_rate=44100):
        samples = []
        for frequency, duration_ms in notes:
            note_samples = int(sample_rate * duration_ms / 1000)
            attack = max(1, int(note_samples * 0.08))
            release = max(1, int(note_samples * 0.1))
            for index in range(note_samples):
                phase = index / sample_rate
                raw = math.sin(2 * math.pi * frequency * phase)
                envelope = min((index + 1) / attack, (note_samples - index) / release)
                envelope = max(0.0, min(1.0, envelope))
                samples.append(raw * envelope)

        file_path = self._write_wave(samples, sample_rate, volume)
        effect = QSoundEffect(self)
        effect.setSource(QUrl.fromLocalFile(file_path))
        effect.setVolume(volume)
        return effect

    def _play_effect(self, effect):
        if effect is None:
            return
        effect.stop()
        effect.play()

    def _play_ui_click(self):
        self._play_effect(self.ui_click_sound)

    def closeEvent(self, event):
        for path in self._audio_temp_paths:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass
        super().closeEvent(event)

    def _create_stat_card(self, title, value, accent):
        card = QFrame()
        card.setStyleSheet(
            f"QFrame {{ background-color: {COLORS['surface']}; border-radius: 12px; border: 1px solid {accent}; }}"
        )
        card.setMinimumHeight(70)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 9, 12, 9)
        layout.setSpacing(3)
        title_label = QLabel(title)
        title_label.setStyleSheet(f"background-color: transparent; border: none; color: {COLORS['soft']}; font-family: {FONT_FAMILY}; font-size: 10px; font-weight: 900;")
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"background-color: transparent; border: none; color: {accent}; font-family: {FONT_FAMILY}; font-size: 24px; font-weight: 900;")
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.title_label = title_label
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
        completed = sum(1 for status in self.level_status.values() if status == "COMPLETADO")
        self.home_score_card.value_label.setText(str(self.best_score))
        self.home_games_card.value_label.setText(str(self.games_played))
        self.home_words_card.value_label.setText(str(self.total_words_found))
        self.home_levels_card.value_label.setText(f"{completed}/{len(NIVELES)}")

    def refresh_level_cards(self):
        for number, card in self.level_cards.items():
            status = self.t("level_status_completed") if self.level_status.get(number) == "COMPLETADO" else self.t("level_status_new")
            status_color = COLORS["green"] if self.level_status.get(number) == "COMPLETADO" else COLORS["cyan"]
            for child in card.findChildren(QLabel):
                if child.text() in [self.t("level_status_new"), self.t("level_status_completed")]:
                    child.setText(status)
                    child.setStyleSheet(f"background-color: transparent; border: none; color: {status_color}; font-family: {FONT_FAMILY}; font-size: 10px; font-weight: 900;")
                    break

    def start_level(self, level_number):
        self.current_level = level_number
        config = NIVELES[level_number]
        palabras = obtener_palabras_del_nivel(level_number, self.current_language)
        self.current_board, self.hidden_positions, self.hidden_words = generar_tablero(config["tamano"], palabras)
        palette = [COLORS["cyan"], COLORS["green"], COLORS["yellow"], COLORS["orange"], COLORS["pink"], COLORS["purple"], COLORS["red"]]
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
        self.level_header.setText(f"{self.t('level_header', level=level_number, name=self._level_name(level_number).upper())}")
        self.level_header.setStyleSheet(f"background-color: transparent; border: none; color: {config['color']}; font-family: {FONT_FAMILY}; font-size: 19px; font-weight: 900;")
        self.timer_label.setText(formatear_tiempo(self.time_left))
        self.timer_label.setStyleSheet(f"background-color: {COLORS['surface']}; color: {config['color']}; border: 1px solid {config['color']}; border-radius: 8px; padding: 7px 14px; font-family: {LETTER_FONT}; font-size: 24px; font-weight: 900;")
        self.hint_btn.setText(self.t("game_hint", count=self.hints_left))
        self.word_preview.setText("")
        self.status_label.setText(self.t("game_select_letters"))
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
        if size <= 8:
            cell_size = 49
            cell_font = 24
            grid_gap = 5
        elif size <= 10:
            cell_size = 40
            cell_font = 20
            grid_gap = 4
        elif size <= 12:
            cell_size = 33
            cell_font = 17
            grid_gap = 3
        elif size <= 14:
            cell_size = 29
            cell_font = 15
            grid_gap = 2
        elif size <= 16:
            cell_size = 26
            cell_font = 13
            grid_gap = 2
        else:
            cell_size = 23
            cell_font = 12
            grid_gap = 2
        cell_radius = 6 if cell_size >= 40 else 3
        board_size = (size * cell_size) + ((size - 1) * grid_gap)
        self.board_widget.setFixedSize(board_size, board_size)
        self.board_grid.setSpacing(grid_gap)
        for row in range(size):
            row_buttons = []
            for col in range(size):
                letter = self.current_board[row][col]
                cell_btn = QPushButton(letter)
                cell_btn.setFixedSize(cell_size, cell_size)
                cell_btn.setCheckable(True)
                cell_btn.setFocusPolicy(Qt.NoFocus)
                cell_btn.setProperty("cell_font", cell_font)
                cell_btn.setProperty("cell_radius", cell_radius)
                cell_btn.setStyleSheet(
                    f"QPushButton {{ background-color: #0d1628; color: {COLORS['letter']}; border: 1px solid {COLORS['line']}; border-radius: {cell_radius}px; padding: 0px; outline: none; font-family: {LETTER_FONT}; font-size: {cell_font}px; font-weight: 900; }}"
                    f"QPushButton:hover {{ background-color: #16284a; color: {COLORS['neon']}; border-color: {COLORS['cyan']}; }}"
                    f"QPushButton:checked {{ background-color: {COLORS['cyan']}; color: {COLORS['surface']}; }}"
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
                    cell_font = button.property("cell_font") or 13
                    cell_radius = button.property("cell_radius") or 3
                    button.setChecked(True)
                    button.setStyleSheet(
                        f"QPushButton {{ background-color: {COLORS['cyan']}; color: {COLORS['surface']}; border-radius: {cell_radius}px; border: 2px solid {COLORS['neon']}; padding: 0px; outline: none; font-family: {LETTER_FONT}; font-size: {cell_font}px; font-weight: 900; }}"
                    )
                elif position in found_positions:
                    cell_font = button.property("cell_font") or 13
                    cell_radius = button.property("cell_radius") or 3
                    word = found_word_by_pos[position]
                    accent = self.word_colors.get(word, COLORS["green"])
                    button.setChecked(False)
                    button.setStyleSheet(
                        f"QPushButton {{ background-color: {accent}; color: {COLORS['surface']}; border-radius: {cell_radius}px; border: 2px solid {accent}; padding: 0px; outline: none; font-family: {LETTER_FONT}; font-size: {cell_font}px; font-weight: 900; }}"
                    )
                elif position in self.hint_positions:
                    cell_font = button.property("cell_font") or 13
                    cell_radius = button.property("cell_radius") or 3
                    button.setChecked(False)
                    button.setStyleSheet(
                        f"QPushButton {{ background-color: {COLORS['surface']}; color: {COLORS['yellow']}; border-radius: {cell_radius}px; border: 2px solid {COLORS['yellow']}; padding: 0px; outline: none; font-family: {LETTER_FONT}; font-size: {cell_font}px; font-weight: 900; }}"
                    )
                else:
                    cell_font = button.property("cell_font") or 13
                    cell_radius = button.property("cell_radius") or 3
                    button.setChecked(False)
                    button.setStyleSheet(
                        f"QPushButton {{ background-color: #0d1628; color: {COLORS['letter']}; border: 1px solid {COLORS['line']}; border-radius: {cell_radius}px; padding: 0px; outline: none; font-family: {LETTER_FONT}; font-size: {cell_font}px; font-weight: 900; }}"
                        f"QPushButton:hover {{ background-color: #16284a; color: {COLORS['neon']}; border-color: {COLORS['cyan']}; }}"
                    )

    def clear_selection(self):
        self.selected_positions = []
        self.selected_letters = []
        self.word_preview.setText("")
        self.status_label.setText(self.t("game_select_letters"))
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
        self._play_effect(self.success_sound)
        self.combo += 1
        self.best_combo = max(self.best_combo, self.combo)
        config = NIVELES[self.current_level]
        time_bonus = self._time_bonus_for_level(self.current_level)
        gained = config["puntos_base"] * len(word) * max(1, self.combo)
        self.score += gained
        self.time_left += time_bonus
        self.timer_label.setText(formatear_tiempo(self.time_left))
        self._refresh_sidebar()
        self._refresh_progress()
        self.word_preview.setText("")
        self.selected_positions = []
        self.selected_letters = []
        self.status_label.setText(self.t("game_word_found", word=word, gained=gained, bonus=time_bonus))
        self._rebuild_board_visuals()
        self._update_time_bar()
        if len(self.found_words) == len(self.hidden_words):
            self.finish_level(victory=True)

    def _wrong_word(self):
        self._play_effect(self.error_sound)
        self.lives -= 1
        self.combo = 0
        self.status_label.setText(self.t("game_word_wrong"))
        self._refresh_sidebar()
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
        self.status_label.setText(self.t("game_hint_used", word=word))
        self.hints_left -= 1
        self.hint_btn.setText(self.t("game_hint", count=self.hints_left))
        self._rebuild_board_visuals()

    def _refresh_sidebar(self):
        self.score_value_label.setText(str(self.score))
        self.combo_value_label.setText(f"x{self.combo}")
        self.lives_value_label.setText("●" * self.lives)

    def _refresh_progress(self):
        found = len(self.found_words)
        total = len(self.hidden_words)
        percent = int((found / total) * 100) if total else 0
        self.progress_label.setText(self.t("game_progress", found=found, total=total, percent=percent))

        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for word in self.hidden_words:
            row = QFrame()
            accent = self.word_colors.get(word, COLORS["cyan"])
            row.setStyleSheet(
                f"QFrame {{ background-color: {COLORS['surface']}; border-radius: 8px; border: 1px solid {accent}; }}"
            )
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(11, 8, 11, 8)
            word_label = QLabel(word)
            word_label.setStyleSheet(f"background-color: transparent; border: none; color: {accent}; font-family: {LETTER_FONT}; font-size: 13px; font-weight: 900;")
            row_layout.addWidget(word_label)

            is_found = word in self.found_words
            status_label = QLabel(self.t("game_found") if is_found else self.t("game_hidden"))
            status_color = COLORS["green"] if is_found else COLORS["red"]
            status_label.setStyleSheet(
                f"background-color: transparent; border: none; color: {status_color}; font-family: {FONT_FAMILY}; font-size: 9px; font-weight: 900;"
            )
            row_layout.addStretch()
            row_layout.addWidget(status_label)
            self.words_layout.addWidget(row)

    def _update_time_bar(self):
        config = NIVELES[self.current_level]
        ratio = min(max(self.time_left / config["tiempo"], 0), 1)
        fill_width = max(10, int(320 * ratio))
        self.time_fill.setFixedWidth(fill_width)
        if ratio < 0.25:
            self.time_fill.setStyleSheet(f"background-color: {COLORS['red']}; border-radius: 5px;")
        elif ratio < 0.5:
            self.time_fill.setStyleSheet(f"background-color: {COLORS['yellow']}; border-radius: 5px;")
        else:
            self.time_fill.setStyleSheet(f"background-color: {COLORS['cyan']}; border-radius: 5px;")

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
        self.summary_result = "victory" if victory else "defeat"
        if victory:
            self._play_effect(self.level_complete_sound)
            self.level_status[self.current_level] = "COMPLETADO"
        self.update_summary_styles()
        self.summary_score.value_label.setText(str(final_score if victory else self.score))
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
