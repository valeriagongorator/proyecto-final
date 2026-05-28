"""
Word Hunt - Sopa de Letras Interactiva
Proyecto Final para Code in Place
Autor: Estudiante

Requisitos cumplidos:
- Python puro
- Tkinter para GUI
- Listas/matrices para el tablero
- Funciones modulares
- Eventos de botones
- Sin base de datos ni backend
"""

import tkinter as tk
from tkinter import messagebox
import random
import string


# ============================================================
# CONFIGURACION DE COLORES - PALETA MODERNA
# ============================================================

COLORS = {
    # Fondos
    "bg_dark": "#1a1b26",
    "bg_medium": "#24283b",
    "bg_light": "#414868",
    
    # Acentos vibrantes
    "cyan": "#7dcfff",
    "pink": "#ff79c6",
    "green": "#9ece6a",
    "yellow": "#e0af68",
    "purple": "#bb9af7",
    "orange": "#ff9e64",
    "red": "#f7768e",
    "blue": "#7aa2f7",
    
    # Texto
    "text_white": "#c0caf5",
    "text_gray": "#565f89",
    "text_dark": "#1a1b26",
}


# ============================================================
# CONFIGURACION DE NIVELES
# ============================================================

NIVELES = {
    1: {
        "nombre": "Principiante",
        "tamano": 8,
        "palabras": ["SOL", "LUZ", "MAR", "RIO", "PEZ", "AVE", "OJO", "DIA"],
        "tiempo": 180,
        "vidas": 5,
        "pistas": 3,
        "color": COLORS["green"],
        "puntos_base": 10
    },
    2: {
        "nombre": "Facil",
        "tamano": 10,
        "palabras": ["PYTHON", "CODIGO", "JUEGO", "LETRA", "BUSCAR", "MATRIZ", "CICLO", "CLASE"],
        "tiempo": 240,
        "vidas": 4,
        "pistas": 2,
        "color": COLORS["cyan"],
        "puntos_base": 15
    },
    3: {
        "nombre": "Intermedio",
        "tamano": 12,
        "palabras": ["VARIABLE", "FUNCION", "ARREGLO", "METODO", "OBJETO", "LOGICA", "BUCLE", "DATOS"],
        "tiempo": 300,
        "vidas": 4,
        "pistas": 2,
        "color": COLORS["yellow"],
        "puntos_base": 20
    },
    4: {
        "nombre": "Avanzado",
        "tamano": 14,
        "palabras": ["ALGORITMO", "RECURSION", "INTERFAZ", "HERENCIA", "ESTRUCTURA", "PARAMETRO", "ITERACION"],
        "tiempo": 360,
        "vidas": 3,
        "pistas": 1,
        "color": COLORS["orange"],
        "puntos_base": 30
    },
    5: {
        "nombre": "Experto",
        "tamano": 16,
        "palabras": ["PROGRAMACION", "COMPUTADORA", "DESARROLLO", "APLICACION", "COMPILADOR", "OPTIMIZAR", "DEPURADOR"],
        "tiempo": 420,
        "vidas": 3,
        "pistas": 1,
        "color": COLORS["pink"],
        "puntos_base": 40
    },
    6: {
        "nombre": "Maestro",
        "tamano": 18,
        "palabras": ["ENCAPSULAMIENTO", "POLIMORFISMO", "ABSTRACCION", "MODULARIDAD", "CONSTRUCTOR", "INSTANCIACION"],
        "tiempo": 480,
        "vidas": 2,
        "pistas": 0,
        "color": COLORS["purple"],
        "puntos_base": 50
    }
}


# ============================================================
# FUNCIONES PARA GENERAR EL TABLERO (MATRIZ)
# ============================================================

def crear_matriz_vacia(tamano):
    """Crea una matriz NxN llena de cadenas vacias."""
    return [['' for _ in range(tamano)] for _ in range(tamano)]


def obtener_direcciones():
    """Retorna las 8 direcciones posibles para colocar palabras."""
    return [
        (0, 1),   # Horizontal derecha
        (0, -1),  # Horizontal izquierda
        (1, 0),   # Vertical abajo
        (-1, 0),  # Vertical arriba
        (1, 1),   # Diagonal abajo-derecha
        (-1, -1), # Diagonal arriba-izquierda
        (1, -1),  # Diagonal abajo-izquierda
        (-1, 1)   # Diagonal arriba-derecha
    ]


def puede_colocar_palabra(tablero, palabra, fila, col, dir_fila, dir_col):
    """Verifica si una palabra puede colocarse en una posicion y direccion."""
    tamano = len(tablero)
    
    for i, letra in enumerate(palabra):
        nueva_fila = fila + (i * dir_fila)
        nueva_col = col + (i * dir_col)
        
        # Verificar limites
        if nueva_fila < 0 or nueva_fila >= tamano:
            return False
        if nueva_col < 0 or nueva_col >= tamano:
            return False
        
        # Verificar si la celda esta vacia o tiene la misma letra
        celda = tablero[nueva_fila][nueva_col]
        if celda != '' and celda != letra:
            return False
    
    return True


def colocar_palabra(tablero, palabra, fila, col, dir_fila, dir_col):
    """Coloca una palabra en el tablero y retorna las posiciones."""
    posiciones = []
    
    for i, letra in enumerate(palabra):
        nueva_fila = fila + (i * dir_fila)
        nueva_col = col + (i * dir_col)
        tablero[nueva_fila][nueva_col] = letra
        posiciones.append((nueva_fila, nueva_col))
    
    return posiciones


def insertar_palabra_en_tablero(tablero, palabra, max_intentos=100):
    """Intenta insertar una palabra en el tablero en una posicion aleatoria."""
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
    """Rellena las celdas vacias del tablero con letras aleatorias."""
    letras = string.ascii_uppercase
    
    for fila in range(len(tablero)):
        for col in range(len(tablero[fila])):
            if tablero[fila][col] == '':
                tablero[fila][col] = random.choice(letras)


def generar_tablero(tamano, palabras):
    """Genera un tablero completo con las palabras ocultas."""
    tablero = crear_matriz_vacia(tamano)
    posiciones_palabras = {}
    palabras_colocadas = []
    
    # Ordenar palabras por longitud (las mas largas primero)
    palabras_ordenadas = sorted(palabras, key=len, reverse=True)
    
    for palabra in palabras_ordenadas:
        posiciones = insertar_palabra_en_tablero(tablero, palabra)
        if posiciones:
            posiciones_palabras[palabra] = posiciones
            palabras_colocadas.append(palabra)
    
    rellenar_tablero_con_letras(tablero)
    
    return tablero, posiciones_palabras, palabras_colocadas


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def formatear_tiempo(segundos):
    """Convierte segundos a formato MM:SS."""
    minutos = segundos // 60
    segs = segundos % 60
    return f"{minutos:02d}:{segs:02d}"


def aplicar_estilo_boton_nativo(boton, bg_color, fg_color, active_bg_color=None, active_fg_color=None):
    """Aplica un estilo visual consistente a botones Tk en macOS."""
    boton.configure(
        bg=bg_color,
        fg=fg_color,
        activebackground=active_bg_color or bg_color,
        activeforeground=active_fg_color or fg_color,
        highlightthickness=1,
        highlightbackground=COLORS["bg_medium"],
        highlightcolor=COLORS["cyan"],
        borderwidth=0,
        bd=0,
        relief="flat",
        cursor="hand2",
        takefocus=0,
    )
    return boton


def configurar_estilo_global(ventana):
    """Forza un aspecto consistente en botones y fondos del entorno Tk."""
    ventana.option_add("*Font", "Consolas 11")
    ventana.option_add("*Button.highlightThickness", "1")
    ventana.option_add("*Button.borderWidth", "0")
    ventana.option_add("*Button.relief", "flat")
    ventana.option_add("*Button.background", COLORS["bg_light"])
    ventana.option_add("*Button.foreground", COLORS["text_dark"])
    ventana.option_add("*Button.activeBackground", COLORS["cyan"])
    ventana.option_add("*Button.activeForeground", COLORS["text_dark"])
    ventana.option_add("*Button.highlightBackground", COLORS["bg_medium"])
    ventana.option_add("*Button.highlightColor", COLORS["cyan"])
    ventana.option_add("*Label.background", COLORS["bg_dark"])
    ventana.option_add("*Frame.background", COLORS["bg_dark"])


def crear_boton_estilizado(parent, texto, color, comando, ancho=15, alto=1, tamano_fuente=12):
    """Crea un boton con estilo personalizado."""
    btn = tk.Button(
        parent,
        text=texto,
        font=("Consolas", tamano_fuente, "bold"),
        width=ancho,
        height=alto,
        command=comando
    )
    aplicar_estilo_boton_nativo(
        btn,
        color,
        COLORS["text_dark"],
        active_bg_color=color,
        active_fg_color=COLORS["text_dark"],
    )
    
    # Efectos hover
    def on_enter(e):
        btn.configure(bg=COLORS["text_white"], fg=COLORS["text_dark"])
    
    def on_leave(e):
        btn.configure(bg=color, fg=COLORS["text_dark"])
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn


def crear_panel(parent, bg_color, padx=18, pady=18, highlight_color=None, highlight_width=1):
    """Crea un panel visual con borde sutil para secciones del juego."""
    panel = tk.Frame(
        parent,
        bg=bg_color,
        padx=padx,
        pady=pady,
        highlightbackground=highlight_color or bg_color,
        highlightcolor=highlight_color or bg_color,
        highlightthickness=highlight_width,
    )
    return panel


def crear_badge(parent, texto, fg_color, bg_color, ancho=None, alto=None):
    """Crea un badge compacto para destacar metadatos o estados."""
    frame = tk.Frame(parent, bg=bg_color)
    frame.pack(side="left", padx=4, pady=2)
    label = tk.Label(
        frame,
        text=texto,
        font=("Consolas", 9, "bold"),
        fg=fg_color,
        bg=bg_color,
        padx=8,
        pady=3
    )
    if ancho:
        label.configure(width=ancho)
    if alto:
        label.configure(height=alto)
    label.pack()
    return frame


def crear_tarjeta_estadistica(parent, titulo, valor, color, bg_color=COLORS["bg_medium"]):
    """Crea una tarjeta compacta para mostrar métricas del juego."""
    card = crear_panel(parent, bg_color, padx=14, pady=12, highlight_color=COLORS["bg_light"], highlight_width=1)
    card.pack(side="left", fill="both", expand=True, padx=6)

    lbl_titulo = tk.Label(
        card,
        text=titulo,
        font=("Consolas", 9),
        fg=COLORS["text_gray"],
        bg=bg_color
    )
    lbl_titulo.pack(anchor="w")

    lbl_valor = tk.Label(
        card,
        text=valor,
        font=("Consolas", 18, "bold"),
        fg=color,
        bg=bg_color
    )
    lbl_valor.pack(anchor="w", pady=(4, 0))

    return card


def crear_metric_card(parent, titulo, valor, color, bg_color=COLORS["bg_medium"]):
    """Crea una tarjeta vertical de métricas para la pantalla de juego."""
    card = crear_panel(parent, bg_color, padx=12, pady=12, highlight_color=COLORS["bg_light"], highlight_width=1)
    card.pack(fill="x", pady=6)

    lbl_titulo = tk.Label(
        card,
        text=titulo,
        font=("Consolas", 9, "bold"),
        fg=COLORS["text_gray"],
        bg=bg_color
    )
    lbl_titulo.pack(anchor="w")

    lbl_valor = tk.Label(
        card,
        text=valor,
        font=("Consolas", 24, "bold"),
        fg=color,
        bg=bg_color
    )
    lbl_valor.pack(anchor="w", pady=(4, 0))

    return card, lbl_valor


# ============================================================
# CLASE PRINCIPAL DEL JUEGO
# ============================================================

class WordHunt:
    """Clase principal que maneja el juego Word Hunt."""
    
    def __init__(self, ventana):
        """Inicializa la ventana y variables del juego."""
        self.ventana = ventana
        configurar_estilo_global(self.ventana)
        self.ventana.title("Word Hunt • Proyecto Final")
        self.ventana.configure(bg=COLORS["bg_dark"])
        self.ventana.minsize(1000, 750)
        self.ventana.geometry("1180x820")
        
        # Estado del juego (en memoria, sin persistencia)
        self.nivel_actual = 1
        self.niveles_completados = []
        self.record_puntos = 0
        self.partidas_jugadas = 0
        self.palabras_encontradas_total = 0
        
        # Variables de partida
        self.tablero = []
        self.botones_tablero = []
        self.palabras_por_encontrar = []
        self.palabras_encontradas = []
        self.posiciones_palabras = {}
        self.letras_seleccionadas = []
        self.posiciones_seleccionadas = []
        self.puntos = 0
        self.tiempo_restante = 0
        self.vidas = 0
        self.vidas_maximas = 0
        self.pistas_restantes = 0
        self.combo = 0
        self.mejor_combo = 0
        self.timer_activo = False
        self.timer_id = None
        self.hud_anim_id = None
        self.hud_anim_index = 0
        self.hud_anim_panels = []
        self.hud_anim_colors = [COLORS["cyan"], COLORS["purple"], COLORS["yellow"], COLORS["green"]]
        
        # Mostrar menu principal
        self.mostrar_menu_principal()
    
    # --------------------------------------------------------
    # LIMPIAR VENTANA
    # --------------------------------------------------------
    
    def limpiar_ventana(self):
        """Elimina todos los widgets de la ventana."""
        if self.timer_id:
            self.ventana.after_cancel(self.timer_id)
            self.timer_id = None
        if self.hud_anim_id:
            self.ventana.after_cancel(self.hud_anim_id)
            self.hud_anim_id = None
        self.timer_activo = False
        self.hud_anim_panels = []
        
        for widget in self.ventana.winfo_children():
            widget.destroy()
    
    # --------------------------------------------------------
    # MENU PRINCIPAL
    # --------------------------------------------------------
    
    def mostrar_menu_principal(self):
        """Muestra el menu principal del juego con una presentación profesional."""
        self.limpiar_ventana()
        
        frame_principal = tk.Frame(self.ventana, bg=COLORS["bg_dark"])
        frame_principal.pack(expand=True, fill="both", padx=32, pady=28)
        frame_principal.columnconfigure(0, weight=1)
        
        # Hero principal
        frame_hero = tk.Frame(frame_principal, bg=COLORS["bg_dark"])
        frame_hero.pack(fill="x")
        frame_hero.columnconfigure(0, weight=2)
        frame_hero.columnconfigure(1, weight=1)
        
        frame_texto = tk.Frame(frame_hero, bg=COLORS["bg_dark"])
        frame_texto.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        frame_badges = tk.Frame(frame_texto, bg=COLORS["bg_dark"])
        frame_badges.pack(anchor="w", pady=(0, 12))
        crear_badge(frame_badges, "PROYECTO FINAL", COLORS["cyan"], COLORS["bg_medium"])
        crear_badge(frame_badges, "PYTHON + TKINTER", COLORS["yellow"], COLORS["bg_light"])
        
        titulo_word = tk.Label(
            frame_texto,
            text="WORD",
            font=("Consolas", 68, "bold"),
            fg=COLORS["cyan"],
            bg=COLORS["bg_dark"]
        )
        titulo_word.pack(anchor="w")
        
        titulo_hunt = tk.Label(
            frame_texto,
            text="HUNT",
            font=("Consolas", 68, "bold"),
            fg=COLORS["pink"],
            bg=COLORS["bg_dark"]
        )
        titulo_hunt.pack(anchor="w")
        
        subtitulo = tk.Label(
            frame_texto,
            text="Sopa de letras interactiva con niveles, combos, pistas y una interfaz pensada para presentar.",
            font=("Consolas", 12),
            fg=COLORS["text_white"],
            bg=COLORS["bg_dark"],
            justify="left",
            anchor="w"
        )
        subtitulo.pack(anchor="w", pady=(12, 4))
        
        descripcion = tk.Label(
            frame_texto,
            text="Busca palabras escondidas, suma puntos, desbloquea retos y muestra tu mejor rendimiento en cada partida.",
            font=("Consolas", 10),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_dark"],
            justify="left",
            anchor="w"
        )
        descripcion.pack(anchor="w")
        
        panel_preview = crear_panel(
            frame_hero,
            COLORS["bg_medium"],
            padx=16,
            pady=16,
            highlight_color=COLORS["bg_light"],
            highlight_width=1
        )
        panel_preview.grid(row=0, column=1, sticky="nsew")
        
        preview_titulo = tk.Label(
            panel_preview,
            text="PREVIEW",
            font=("Consolas", 9, "bold"),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_medium"]
        )
        preview_titulo.pack(anchor="w")
        
        preview_subtitulo = tk.Label(
            panel_preview,
            text="NIVEL 1 | RETO INICIAL",
            font=("Consolas", 13, "bold"),
            fg=COLORS["green"],
            bg=COLORS["bg_medium"]
        )
        preview_subtitulo.pack(anchor="w", pady=(5, 0))
        
        preview_grid = tk.Frame(panel_preview, bg=COLORS["bg_medium"])
        preview_grid.pack(fill="x", pady=(10, 0))
        
        preview_letras = [
            ["P", "Y", "T", "H"],
            ["O", "N", "A", "R"],
            ["C", "O", "D", "E"],
            ["L", "E", "T", "R"],
        ]
        
        for fila, letras in enumerate(preview_letras):
            for col, letra in enumerate(letras):
                celda = tk.Label(
                    preview_grid,
                    text=letra,
                    font=("Consolas", 12, "bold"),
                    fg=COLORS["text_white"],
                    bg=COLORS["bg_light"],
                    width=3,
                    padx=4,
                    pady=4,
                    relief="flat"
                )
                celda.grid(row=fila, column=col, padx=2, pady=2)
        
        preview_badges = tk.Frame(panel_preview, bg=COLORS["bg_medium"])
        preview_badges.pack(fill="x", pady=(12, 0))
        crear_badge(preview_badges, "8 NIVELES", COLORS["cyan"], COLORS["bg_light"])
        crear_badge(preview_badges, "COMBOS", COLORS["green"], COLORS["bg_light"])
        crear_badge(preview_badges, "PISTAS", COLORS["purple"], COLORS["bg_light"])
        
        frame_stats = crear_panel(frame_principal, COLORS["bg_medium"], padx=16, pady=14, highlight_color=COLORS["bg_light"], highlight_width=1)
        frame_stats.pack(fill="x", pady=22)
        
        frame_stats_inner = tk.Frame(frame_stats, bg=COLORS["bg_medium"])
        frame_stats_inner.pack(fill="x")
        
        estadisticas = [
            ("RECORD", str(self.record_puntos), COLORS["yellow"]),
            ("PARTIDAS", str(self.partidas_jugadas), COLORS["cyan"]),
            ("PALABRAS", str(self.palabras_encontradas_total), COLORS["green"]),
            ("NIVELES", f"{len(self.niveles_completados)}/6", COLORS["purple"]),
        ]
        
        for titulo, valor, color in estadisticas:
            crear_tarjeta_estadistica(frame_stats_inner, titulo, valor, color)
        
        frame_botones = tk.Frame(frame_principal, bg=COLORS["bg_dark"])
        frame_botones.pack(fill="x")
        
        btn_jugar = crear_boton_estilizado(
            frame_botones,
            "INICIAR PARTIDA",
            COLORS["green"],
            self.mostrar_selector_nivel,
            ancho=24,
            alto=2,
            tamano_fuente=16
        )
        btn_jugar.pack(side="left")
        
        btn_como_jugar = crear_boton_estilizado(
            frame_botones,
            "VER GUIA",
            COLORS["cyan"],
            self.mostrar_instrucciones,
            ancho=18,
            alto=2,
            tamano_fuente=12
        )
        btn_como_jugar.pack(side="left", padx=(12, 0))
        
        frame_features = tk.Frame(frame_principal, bg=COLORS["bg_dark"])
        frame_features.pack(fill="x", pady=(14, 0))
        crear_badge(frame_features, "✓ Progresión por niveles", COLORS["green"], COLORS["bg_medium"])
        crear_badge(frame_features, "✓ Eventos de combo", COLORS["orange"], COLORS["bg_medium"])
        crear_badge(frame_features, "✓ Pistas estratégicas", COLORS["purple"], COLORS["bg_medium"])
        
        creditos = tk.Label(
            frame_principal,
            text="Code in Place · Proyecto Final · Python + Tkinter",
            font=("Consolas", 10),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_dark"]
        )
        creditos.pack(anchor="w", pady=(16, 0))
    
    # --------------------------------------------------------
    # INSTRUCCIONES
    # --------------------------------------------------------
    
    def mostrar_instrucciones(self):
        """Muestra las instrucciones del juego con un layout editorial."""
        self.limpiar_ventana()
        
        frame = tk.Frame(self.ventana, bg=COLORS["bg_dark"])
        frame.pack(expand=True, fill="both", padx=32, pady=24)
        
        btn_volver = tk.Button(
            frame,
            text="< VOLVER",
            font=("Consolas", 12, "bold"),
            command=self.mostrar_menu_principal
        )
        aplicar_estilo_boton_nativo(
            btn_volver,
            COLORS["bg_dark"],
            COLORS["cyan"],
            active_bg_color=COLORS["bg_medium"],
            active_fg_color=COLORS["text_white"],
        )
        btn_volver.pack(anchor="w")
        
        titulo = tk.Label(
            frame,
            text="GUIA Y REGLAS",
            font=("Consolas", 36, "bold"),
            fg=COLORS["cyan"],
            bg=COLORS["bg_dark"]
        )
        titulo.pack(anchor="w", pady=(16, 6))
        
        subtitulo = tk.Label(
            frame,
            text="Domina la mecánica del juego y prepárate para presentar cada ronda con claridad.",
            font=("Consolas", 11),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_dark"],
            justify="left",
            anchor="w"
        )
        subtitulo.pack(anchor="w")
        
        frame_contenido = tk.Frame(frame, bg=COLORS["bg_dark"])
        frame_contenido.pack(fill="both", expand=True, pady=(20, 0))
        
        instrucciones = [
            ("SELECCIONA LETRAS", "Haz clic en las letras del tablero para construir una palabra y observa cómo se resalta tu camino.", COLORS["cyan"], "1"),
            ("CONFIRMA O BORRA", "Confirma la palabra con el botón adecuado o borra la selección cuando quieras corregirla.", COLORS["green"], "2"),
            ("ENCUENTRA TODAS", "Busca cada palabra antes de que termine el tiempo y avanza de nivel con un puntaje más alto.", COLORS["yellow"], "3"),
            ("CUIDA TUS VIDAS", "Cada error quita una vida, así que prioriza precisión y estrategia para no perder la partida.", COLORS["red"], "4"),
            ("USA PISTAS", "Las pistas revelan la primera letra de una palabra y te ayudan cuando te quedas atascado.", COLORS["purple"], "5"),
            ("COMBOS", "Acierta palabras consecutivas para multiplicar los puntos y aumentar la emoción del juego.", COLORS["orange"], "6"),
        ]
        
        for nombre, desc, color, numero in instrucciones:
            card = crear_panel(frame_contenido, COLORS["bg_medium"], padx=18, pady=14, highlight_color=COLORS["bg_light"], highlight_width=1)
            card.pack(fill="x", pady=8)
            
            header = tk.Frame(card, bg=COLORS["bg_medium"])
            header.pack(fill="x")
            
            marker = tk.Label(
                header,
                text=numero,
                font=("Consolas", 12, "bold"),
                fg=color,
                bg=COLORS["bg_medium"]
            )
            marker.pack(side="left")
            
            lbl_titulo = tk.Label(
                header,
                text=nombre,
                font=("Consolas", 14, "bold"),
                fg=color,
                bg=COLORS["bg_medium"]
            )
            lbl_titulo.pack(side="left", padx=(10, 0))
            
            lbl_desc = tk.Label(
                card,
                text=desc,
                font=("Consolas", 10),
                fg=COLORS["text_white"],
                bg=COLORS["bg_medium"],
                justify="left",
                anchor="w"
            )
            lbl_desc.pack(anchor="w", pady=(10, 0))
    
    # --------------------------------------------------------
    # SELECTOR DE NIVEL
    # --------------------------------------------------------
    
    def mostrar_selector_nivel(self):
        """Muestra la pantalla de seleccion de nivel con tarjetas destacadas."""
        self.limpiar_ventana()
        
        frame = tk.Frame(self.ventana, bg=COLORS["bg_dark"])
        frame.pack(expand=True, fill="both", padx=32, pady=24)
        
        frame_header = tk.Frame(frame, bg=COLORS["bg_dark"])
        frame_header.pack(fill="x", pady=(0, 20))
        
        btn_volver = tk.Button(
            frame_header,
            text="< MENU",
            font=("Consolas", 12, "bold"),
            command=self.mostrar_menu_principal
        )
        aplicar_estilo_boton_nativo(
            btn_volver,
            COLORS["bg_dark"],
            COLORS["cyan"],
            active_bg_color=COLORS["bg_medium"],
            active_fg_color=COLORS["text_white"],
        )
        btn_volver.pack(side="left")
        
        frame_titulo = tk.Frame(frame_header, bg=COLORS["bg_dark"])
        frame_titulo.pack(side="left", padx=(16, 0))
        
        titulo = tk.Label(
            frame_titulo,
            text="SELECCIONA TU RETO",
            font=("Consolas", 28, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_dark"]
        )
        titulo.pack(anchor="w")
        
        subtitulo = tk.Label(
            frame_titulo,
            text="Cada nivel tiene una dificultad distinta y una experiencia visual diferente.",
            font=("Consolas", 10),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_dark"]
        )
        subtitulo.pack(anchor="w")
        
        frame_niveles = tk.Frame(frame, bg=COLORS["bg_dark"])
        frame_niveles.pack(expand=True, fill="both")
        
        frame_niveles.columnconfigure(0, weight=1)
        frame_niveles.columnconfigure(1, weight=1)
        frame_niveles.columnconfigure(2, weight=1)
        
        for num_nivel, config in NIVELES.items():
            fila = (num_nivel - 1) // 3
            col = (num_nivel - 1) % 3
            
            completado = num_nivel in self.niveles_completados
            
            card = tk.Frame(
                frame_niveles,
                bg=COLORS["bg_medium"],
                padx=18,
                pady=18,
                highlightbackground=config["color"],
                highlightcolor=config["color"],
                highlightthickness=2
            )
            card.grid(row=fila, column=col, padx=10, pady=10, sticky="nsew")
            frame_niveles.rowconfigure(fila, weight=1)
            frame_niveles.columnconfigure(col, weight=1)
            
            top_card = tk.Frame(card, bg=COLORS["bg_medium"])
            top_card.pack(fill="x")
            
            estado_texto = "COMPLETADO" if completado else "NUEVO"
            estado_color = COLORS["green"] if completado else COLORS["cyan"]
            estado = tk.Label(
                top_card,
                text=estado_texto,
                font=("Consolas", 8, "bold"),
                fg=estado_color,
                bg=COLORS["bg_medium"]
            )
            estado.pack(anchor="e")
            
            lbl_num = tk.Label(
                card,
                text=f"NIVEL {num_nivel}",
                font=("Consolas", 10),
                fg=COLORS["text_gray"],
                bg=COLORS["bg_medium"]
            )
            lbl_num.pack(anchor="w", pady=(8, 0))
            
            lbl_nombre = tk.Label(
                card,
                text=config["nombre"].upper(),
                font=("Consolas", 22, "bold"),
                fg=config["color"],
                bg=COLORS["bg_medium"]
            )
            lbl_nombre.pack(anchor="w", pady=(4, 8))
            
            info_texto = f"Tablero {config['tamano']}x{config['tamano']} • {formatear_tiempo(config['tiempo'])} • {'●' * config['vidas']}"
            lbl_info = tk.Label(
                card,
                text=info_texto,
                font=("Consolas", 10),
                fg=COLORS["text_white"],
                bg=COLORS["bg_medium"],
                justify="left",
                anchor="w"
            )
            lbl_info.pack(anchor="w")
            
            meta = tk.Frame(card, bg=COLORS["bg_medium"])
            meta.pack(fill="x", pady=(12, 0))
            crear_badge(meta, f"{config['pistas']} PISTAS", COLORS["purple"], COLORS["bg_light"])
            crear_badge(meta, f"{config['puntos_base']} PTS/WORD", COLORS["orange"], COLORS["bg_light"])
            
            btn_jugar = crear_boton_estilizado(
                card,
                "REJUGAR" if completado else "JUGAR",
                config["color"],
                lambda n=num_nivel: self.iniciar_partida(n),
                ancho=12,
                alto=1,
                tamano_fuente=11
            )
            btn_jugar.pack(pady=(14, 0))
    
    # --------------------------------------------------------
    # INICIAR PARTIDA
    # --------------------------------------------------------
    
    def iniciar_partida(self, nivel):
        """Inicia una nueva partida con el nivel especificado."""
        self.nivel_actual = nivel
        config = NIVELES[nivel]
        
        # Generar tablero
        self.tablero, self.posiciones_palabras, self.palabras_por_encontrar = generar_tablero(
            config["tamano"],
            config["palabras"]
        )
        
        # Reiniciar variables de partida
        self.palabras_encontradas = []
        self.letras_seleccionadas = []
        self.posiciones_seleccionadas = []
        self.puntos = 0
        self.tiempo_restante = config["tiempo"]
        self.vidas = config["vidas"]
        self.vidas_maximas = config["vidas"]
        self.pistas_restantes = config["pistas"]
        self.combo = 0
        self.mejor_combo = 0
        
        # Mostrar pantalla de juego
        self.mostrar_pantalla_juego()
        
        # Iniciar timer
        self.timer_activo = True
        self.actualizar_timer()
    
    # --------------------------------------------------------
    # PANTALLA DE JUEGO
    # --------------------------------------------------------
    
    def actualizar_acento_hud(self):
        """Cambia el color de acento de los paneles principales para dar dinamismo visual."""
        if not self.hud_anim_panels:
            self.hud_anim_id = None
            return

        vivos = []
        color = self.hud_anim_colors[self.hud_anim_index % len(self.hud_anim_colors)]
        for panel in self.hud_anim_panels:
            try:
                if panel.winfo_exists():
                    panel.configure(highlightbackground=color, highlightcolor=color)
                    vivos.append(panel)
            except tk.TclError:
                continue

        self.hud_anim_panels = vivos
        self.hud_anim_index = (self.hud_anim_index + 1) % len(self.hud_anim_colors)

        if vivos:
            self.hud_anim_id = self.ventana.after(700, self.actualizar_acento_hud)
        else:
            self.hud_anim_id = None

    def mostrar_pantalla_juego(self):
        """Muestra la pantalla principal del juego."""
        self.limpiar_ventana()
        
        config = NIVELES[self.nivel_actual]
        
        # Frame principal con grid
        frame_principal = tk.Frame(self.ventana, bg=COLORS["bg_dark"])
        frame_principal.pack(expand=True, fill="both", padx=20, pady=15)
        
        frame_principal.columnconfigure(0, weight=3)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(1, weight=1)
        
        # ========== HEADER ==========
        frame_header = tk.Frame(frame_principal, bg=COLORS["bg_dark"])
        frame_header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        btn_salir = tk.Button(
            frame_header,
            text="X SALIR",
            font=("Consolas", 10, "bold"),
            command=self.confirmar_salir
        )
        aplicar_estilo_boton_nativo(
            btn_salir,
            COLORS["bg_dark"],
            COLORS["red"],
            active_bg_color=COLORS["bg_medium"],
            active_fg_color=COLORS["text_white"],
        )
        btn_salir.pack(side="left")
        
        frame_info_nivel = tk.Frame(frame_header, bg=COLORS["bg_dark"])
        frame_info_nivel.pack(side="left", padx=(20, 0))
        
        lbl_nivel = tk.Label(
            frame_info_nivel,
            text=f"NIVEL {self.nivel_actual}: {config['nombre'].upper()}",
            font=("Consolas", 18, "bold"),
            fg=config["color"],
            bg=COLORS["bg_dark"]
        )
        lbl_nivel.pack(anchor="w")
        
        lbl_nivel_sub = tk.Label(
            frame_info_nivel,
            text="Juego creativo · modo presentación",
            font=("Consolas", 9),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_dark"]
        )
        lbl_nivel_sub.pack(anchor="w")
        
        frame_timer_panel = crear_panel(
            frame_header,
            COLORS["bg_medium"],
            padx=12,
            pady=8,
            highlight_color=COLORS["bg_light"],
            highlight_width=1
        )
        frame_timer_panel.pack(side="right")
        self.hud_anim_panels.append(frame_timer_panel)
        
        lbl_timer_titulo = tk.Label(
            frame_timer_panel,
            text="TIEMPO RESTANTE",
            font=("Consolas", 9),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_medium"]
        )
        lbl_timer_titulo.pack(anchor="w")
        
        self.lbl_timer = tk.Label(
            frame_timer_panel,
            text=formatear_tiempo(self.tiempo_restante),
            font=("Consolas", 24, "bold"),
            fg=COLORS["cyan"],
            bg=COLORS["bg_medium"]
        )
        self.lbl_timer.pack(anchor="w")
        
        # ========== AREA DE JUEGO (IZQUIERDA) ==========
        frame_juego = tk.Frame(frame_principal, bg=COLORS["bg_dark"])
        frame_juego.grid(row=1, column=0, sticky="nsew", padx=(0, 15))
        
        frame_juego.rowconfigure(0, weight=0)
        frame_juego.rowconfigure(1, weight=1)
        frame_juego.rowconfigure(2, weight=0)
        frame_juego.columnconfigure(0, weight=1)
        
        # Barra de progreso del tiempo
        frame_barra_tiempo = tk.Frame(
            frame_juego,
            bg=COLORS["bg_medium"],
            height=10,
            highlightbackground=COLORS["bg_light"],
            highlightcolor=COLORS["bg_light"],
            highlightthickness=1
        )
        frame_barra_tiempo.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        frame_barra_tiempo.pack_propagate(False)
        
        porcentaje_tiempo = self.tiempo_restante / config["tiempo"]
        self.barra_tiempo = tk.Frame(
            frame_barra_tiempo,
            bg=COLORS["cyan"],
            width=int(frame_barra_tiempo.winfo_reqwidth() * porcentaje_tiempo)
        )
        self.barra_tiempo.pack(side="left", fill="y")
        self.actualizar_barra_tiempo()
        
        # ========== TABLERO ==========
        frame_tablero = tk.Frame(
            frame_juego,
            bg=COLORS["bg_medium"],
            padx=10,
            pady=10,
            highlightbackground=COLORS["bg_light"],
            highlightcolor=COLORS["bg_light"],
            highlightthickness=1
        )
        frame_tablero.grid(row=1, column=0, sticky="nsew")
        
        # Configurar grid del tablero
        tamano = config["tamano"]
        for i in range(tamano):
            frame_tablero.rowconfigure(i, weight=1)
            frame_tablero.columnconfigure(i, weight=1)
        
        # Crear botones del tablero
        self.botones_tablero = []
        
        for fila in range(tamano):
            fila_botones = []
            for col in range(tamano):
                letra = self.tablero[fila][col]
                
                btn = tk.Button(
                    frame_tablero,
                    text=letra,
                    font=("Consolas", max(14, 24 - tamano), "bold"),
                    width=2,
                    height=1
                )
                aplicar_estilo_boton_nativo(
                    btn,
                    COLORS["bg_light"],
                    COLORS["text_white"],
                    active_bg_color=COLORS["cyan"],
                    active_fg_color=COLORS["text_dark"],
                )
                btn.grid(row=fila, column=col, padx=2, pady=2, sticky="nsew")
                
                # Vincular evento de clic
                btn.configure(command=lambda f=fila, c=col: self.seleccionar_letra(f, c))
                
                # Efectos hover
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=COLORS["bg_medium"]) if b.cget("bg") == COLORS["bg_light"] else None)
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=COLORS["bg_light"]) if b.cget("bg") == COLORS["bg_medium"] else None)
                
                fila_botones.append(btn)
            self.botones_tablero.append(fila_botones)
        
        # ========== CONTROLES ==========
        frame_controles = tk.Frame(frame_juego, bg=COLORS["bg_dark"])
        frame_controles.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        
        # Palabra seleccionada
        frame_palabra = tk.Frame(
            frame_controles,
            bg=COLORS["bg_medium"],
            padx=18,
            pady=10,
            highlightbackground=COLORS["bg_light"],
            highlightcolor=COLORS["bg_light"],
            highlightthickness=1
        )
        frame_palabra.pack(fill="x", pady=(0, 10))
        
        lbl_seleccion = tk.Label(
            frame_palabra,
            text="SELECCION:",
            font=("Consolas", 10),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_medium"]
        )
        lbl_seleccion.pack(side="left")
        
        self.lbl_palabra_actual = tk.Label(
            frame_palabra,
            text="",
            font=("Consolas", 20, "bold"),
            fg=COLORS["yellow"],
            bg=COLORS["bg_medium"]
        )
        self.lbl_palabra_actual.pack(side="left", padx=10)
        
        self.lbl_estado_juego = tk.Label(
            frame_palabra,
            text="Selecciona letras para formar una palabra.",
            font=("Consolas", 9, "bold"),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_medium"]
        )
        self.lbl_estado_juego.pack(side="right")
        
        # Botones de accion
        frame_acciones = tk.Frame(frame_controles, bg=COLORS["bg_dark"])
        frame_acciones.pack()
        
        btn_confirmar = crear_boton_estilizado(
            frame_acciones,
            "CONFIRMAR",
            COLORS["green"],
            self.confirmar_palabra,
            ancho=12,
            tamano_fuente=12
        )
        btn_confirmar.pack(side="left", padx=5)
        
        btn_borrar = crear_boton_estilizado(
            frame_acciones,
            "BORRAR",
            COLORS["red"],
            self.borrar_seleccion,
            ancho=12,
            tamano_fuente=12
        )
        btn_borrar.pack(side="left", padx=5)
        
        btn_pista = crear_boton_estilizado(
            frame_acciones,
            f"PISTA ({self.pistas_restantes})",
            COLORS["purple"],
            self.usar_pista,
            ancho=12,
            tamano_fuente=12
        )
        btn_pista.pack(side="left", padx=5)
        self.btn_pista = btn_pista
        
        # ========== PANEL LATERAL (DERECHA) ==========
        frame_lateral = tk.Frame(
            frame_principal,
            bg=COLORS["bg_medium"],
            padx=18,
            pady=18,
            highlightbackground=COLORS["bg_light"],
            highlightcolor=COLORS["bg_light"],
            highlightthickness=1
        )
        frame_lateral.grid(row=1, column=1, sticky="nsew")
        self.hud_anim_panels.append(frame_lateral)
        
        lbl_panel_titulo = tk.Label(
            frame_lateral,
            text="ESTADÍSTICAS",
            font=("Consolas", 12, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_medium"]
        )
        lbl_panel_titulo.pack(anchor="w")
        
        lbl_panel_subtitulo = tk.Label(
            frame_lateral,
            text="Seguimiento visual del progreso",
            font=("Consolas", 9),
            fg=COLORS["text_gray"],
            bg=COLORS["bg_medium"]
        )
        lbl_panel_subtitulo.pack(anchor="w", pady=(2, 10))
        
        # Métricas
        _, self.lbl_puntos = crear_metric_card(frame_lateral, "PUNTOS", str(self.puntos), COLORS["yellow"])
        _, self.lbl_combo = crear_metric_card(frame_lateral, "COMBO", f"x{self.combo}", COLORS["orange"])
        _, self.lbl_vidas = crear_metric_card(frame_lateral, "VIDAS", "*" * self.vidas, COLORS["red"])
        
        # Separador
        separador = tk.Frame(frame_lateral, bg=COLORS["bg_light"], height=2)
        separador.pack(fill="x", pady=15)
        
        # Lista de palabras
        lbl_palabras_titulo = tk.Label(
            frame_lateral,
            text="PALABRAS",
            font=("Consolas", 12, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_medium"]
        )
        lbl_palabras_titulo.pack(pady=(0, 10))
        
        self.labels_palabras = {}
        
        for palabra in sorted(self.palabras_por_encontrar, key=len):
            frame_palabra = tk.Frame(
                frame_lateral,
                bg=COLORS["bg_light"],
                padx=10,
                pady=6,
                highlightbackground=COLORS["bg_medium"],
                highlightcolor=COLORS["bg_medium"],
                highlightthickness=1
            )
            frame_palabra.pack(fill="x", pady=4)
            
            lbl = tk.Label(
                frame_palabra,
                text=palabra,
                font=("Consolas", 12, "bold"),
                fg=COLORS["text_gray"],
                bg=COLORS["bg_light"]
            )
            lbl.pack(anchor="w")
            
            self.labels_palabras[palabra] = lbl
        
        # Progreso
        self.lbl_progreso = tk.Label(
            frame_lateral,
            text=f"{len(self.palabras_encontradas)}/{len(self.palabras_por_encontrar)} · 0%",
            font=("Consolas", 14, "bold"),
            fg=COLORS["cyan"],
            bg=COLORS["bg_medium"]
        )
        self.lbl_progreso.pack(pady=(15, 0))

        if not self.hud_anim_id:
            self.hud_anim_id = self.ventana.after(700, self.actualizar_acento_hud)
    
    # --------------------------------------------------------
    # LOGICA DE SELECCION
    # --------------------------------------------------------
    
    def seleccionar_letra(self, fila, col):
        """Maneja la seleccion de una letra en el tablero."""
        posicion = (fila, col)
        
        # Si ya esta seleccionada, deseleccionar
        if posicion in self.posiciones_seleccionadas:
            indice = self.posiciones_seleccionadas.index(posicion)
            # Deseleccionar desde este punto en adelante
            for i in range(indice, len(self.posiciones_seleccionadas)):
                f, c = self.posiciones_seleccionadas[i]
                self.botones_tablero[f][c].configure(
                    bg=COLORS["bg_light"],
                    fg=COLORS["text_white"],
                    highlightbackground=COLORS["bg_medium"],
                    highlightcolor=COLORS["bg_medium"],
                    highlightthickness=1
                )
            
            self.posiciones_seleccionadas = self.posiciones_seleccionadas[:indice]
            self.letras_seleccionadas = self.letras_seleccionadas[:indice]
            self.lbl_estado_juego.configure(text="Continuando la palabra...", fg=COLORS["cyan"])
        else:
            # Seleccionar nueva letra
            self.posiciones_seleccionadas.append(posicion)
            self.letras_seleccionadas.append(self.tablero[fila][col])
            self.botones_tablero[fila][col].configure(
                bg=COLORS["cyan"],
                fg=COLORS["text_dark"],
                highlightbackground=COLORS["text_white"],
                highlightcolor=COLORS["text_white"],
                highlightthickness=2
            )
            self.lbl_estado_juego.configure(text="Letra añadida. Confirma o borra la selección.", fg=COLORS["yellow"])
        
        # Actualizar palabra mostrada
        self.lbl_palabra_actual.configure(text="".join(self.letras_seleccionadas))
    
    def borrar_seleccion(self):
        """Borra toda la seleccion actual."""
        for fila, col in self.posiciones_seleccionadas:
            self.botones_tablero[fila][col].configure(
                bg=COLORS["bg_light"],
                fg=COLORS["text_white"],
                highlightbackground=COLORS["bg_medium"],
                highlightcolor=COLORS["bg_medium"],
                highlightthickness=1
            )
        
        self.posiciones_seleccionadas = []
        self.letras_seleccionadas = []
        self.lbl_palabra_actual.configure(text="")
        self.lbl_estado_juego.configure(text="Selecciona letras para formar una palabra.", fg=COLORS["text_gray"])
    
    def confirmar_palabra(self):
        """Verifica si la palabra seleccionada es correcta."""
        palabra = "".join(self.letras_seleccionadas)
        
        if not palabra:
            return
        
        if palabra in self.palabras_por_encontrar and palabra not in self.palabras_encontradas:
            # Palabra correcta
            self.palabra_encontrada(palabra)
        else:
            # Palabra incorrecta
            self.palabra_incorrecta()
    
    def palabra_encontrada(self, palabra):
        """Maneja cuando se encuentra una palabra correcta."""
        self.palabras_encontradas.append(palabra)
        
        # Incrementar combo
        self.combo += 1
        if self.combo > self.mejor_combo:
            self.mejor_combo = self.combo
        
        # Calcular puntos (con multiplicador de combo)
        config = NIVELES[self.nivel_actual]
        puntos_ganados = config["puntos_base"] * len(palabra) * max(1, self.combo)
        self.puntos += puntos_ganados
        
        # Marcar letras como encontradas (verde)
        for fila, col in self.posiciones_seleccionadas:
            self.botones_tablero[fila][col].configure(
                bg=COLORS["green"],
                fg=COLORS["text_dark"],
                highlightbackground=COLORS["green"],
                highlightcolor=COLORS["green"],
                highlightthickness=2
            )
        
        # Actualizar UI
        self.labels_palabras[palabra].configure(fg=COLORS["green"])
        self.lbl_puntos.configure(text=str(self.puntos))
        self.lbl_combo.configure(text=f"x{self.combo}")
        progreso = len(self.palabras_encontradas) / max(len(self.palabras_por_encontrar), 1)
        self.lbl_progreso.configure(text=f"{len(self.palabras_encontradas)}/{len(self.palabras_por_encontrar)} · {int(progreso * 100)}%")
        self.lbl_estado_juego.configure(text=f"¡{palabra} encontrada! +{puntos_ganados} puntos.", fg=COLORS["green"])
        
        # Limpiar seleccion
        self.posiciones_seleccionadas = []
        self.letras_seleccionadas = []
        self.lbl_palabra_actual.configure(text="")
        
        # Verificar victoria
        if len(self.palabras_encontradas) == len(self.palabras_por_encontrar):
            self.victoria()
    
    def palabra_incorrecta(self):
        """Maneja cuando la palabra es incorrecta."""
        # Perder vida
        self.vidas -= 1
        self.combo = 0
        
        # Efecto visual de error
        for fila, col in self.posiciones_seleccionadas:
            self.botones_tablero[fila][col].configure(
                bg=COLORS["red"],
                fg=COLORS["text_white"],
                highlightbackground=COLORS["red"],
                highlightcolor=COLORS["red"],
                highlightthickness=2
            )
        
        # Restaurar despues de un momento
        self.ventana.after(300, self.borrar_seleccion)
        
        # Actualizar UI
        self.lbl_vidas.configure(text="*" * self.vidas)
        self.lbl_combo.configure(text=f"x{self.combo}")
        self.lbl_estado_juego.configure(text="Palabra incorrecta. Pierdes una vida.", fg=COLORS["red"])
        
        # Verificar derrota
        if self.vidas <= 0:
            self.derrota("Sin vidas")
    
    # --------------------------------------------------------
    # SISTEMA DE PISTAS
    # --------------------------------------------------------
    
    def usar_pista(self):
        """Usa una pista para revelar la primera letra de una palabra."""
        if self.pistas_restantes <= 0:
            return
        
        # Encontrar una palabra no descubierta
        palabras_restantes = [p for p in self.palabras_por_encontrar if p not in self.palabras_encontradas]
        
        if not palabras_restantes:
            return
        
        palabra = random.choice(palabras_restantes)
        posiciones = self.posiciones_palabras.get(palabra)
        
        if posiciones:
            # Resaltar primera letra
            fila, col = posiciones[0]
            self.botones_tablero[fila][col].configure(
                bg=COLORS["purple"],
                fg=COLORS["text_white"],
                highlightbackground=COLORS["purple"],
                highlightcolor=COLORS["purple"],
                highlightthickness=2
            )
        
        self.pistas_restantes -= 1
        self.btn_pista.configure(text=f"PISTA ({self.pistas_restantes})")
        self.lbl_estado_juego.configure(text=f"Pista usada: se resaltó una letra de {palabra}.", fg=COLORS["purple"])
    
    # --------------------------------------------------------
    # TIMER
    # --------------------------------------------------------
    
    def actualizar_barra_tiempo(self):
        """Actualiza la barra de progreso visual del tiempo restante."""
        if not hasattr(self, 'barra_tiempo'):
            return
        
        frame_barra_tiempo = self.barra_tiempo.master
        frame_barra_tiempo.update_idletasks()
        ancho_total = max(frame_barra_tiempo.winfo_width(), 1)
        
        config = NIVELES[self.nivel_actual]
        porcentaje = max(self.tiempo_restante / max(config["tiempo"], 1), 0)
        ancho = max(8, int(ancho_total * porcentaje))
        
        self.barra_tiempo.configure(width=ancho)
        if porcentaje < 0.25:
            self.barra_tiempo.configure(bg=COLORS["red"])
        elif porcentaje < 0.5:
            self.barra_tiempo.configure(bg=COLORS["yellow"])
        else:
            self.barra_tiempo.configure(bg=COLORS["cyan"])

    def actualizar_timer(self):
        """Actualiza el cronometro cada segundo."""
        if not self.timer_activo:
            return
        
        self.tiempo_restante -= 1
        self.lbl_timer.configure(text=formatear_tiempo(self.tiempo_restante))
        self.actualizar_barra_tiempo()
        
        # Cambiar color segun tiempo restante
        config = NIVELES[self.nivel_actual]
        porcentaje = self.tiempo_restante / config["tiempo"]
        
        if porcentaje < 0.25:
            self.lbl_timer.configure(fg=COLORS["red"])
            self.lbl_estado_juego.configure(text="¡Último tramo! Mantén el ritmo.", fg=COLORS["red"])
        elif porcentaje < 0.5:
            self.lbl_timer.configure(fg=COLORS["yellow"])
            self.lbl_estado_juego.configure(text="Racha activa: acelera el ritmo.", fg=COLORS["yellow"])
        else:
            self.lbl_timer.configure(fg=COLORS["cyan"])
            self.lbl_estado_juego.configure(text="Juego en marcha: descubre palabras con calma.", fg=COLORS["cyan"])
        
        # Verificar tiempo agotado
        if self.tiempo_restante <= 0:
            self.derrota("Tiempo agotado")
            return
        
        # Programar siguiente actualizacion
        self.timer_id = self.ventana.after(1000, self.actualizar_timer)
    
    # --------------------------------------------------------
    # FIN DE PARTIDA
    # --------------------------------------------------------
    
    def victoria(self):
        """Maneja la victoria del jugador."""
        self.timer_activo = False
        
        config = NIVELES[self.nivel_actual]
        
        # Bonus por tiempo restante
        bonus_tiempo = self.tiempo_restante * 2
        # Bonus por vidas restantes
        bonus_vidas = self.vidas * 50
        # Bonus por juego perfecto
        bonus_perfecto = 200 if self.vidas == self.vidas_maximas else 0
        
        puntos_finales = self.puntos + bonus_tiempo + bonus_vidas + bonus_perfecto
        
        # Actualizar estadisticas
        self.partidas_jugadas += 1
        self.palabras_encontradas_total += len(self.palabras_encontradas)
        
        if puntos_finales > self.record_puntos:
            self.record_puntos = puntos_finales
        
        if self.nivel_actual not in self.niveles_completados:
            self.niveles_completados.append(self.nivel_actual)
        
        # Mostrar pantalla de victoria
        self.mostrar_pantalla_fin(True, puntos_finales, bonus_tiempo, bonus_vidas, bonus_perfecto)
    
    def derrota(self, razon):
        """Maneja la derrota del jugador."""
        self.timer_activo = False
        
        # Actualizar estadisticas
        self.partidas_jugadas += 1
        self.palabras_encontradas_total += len(self.palabras_encontradas)
        
        if self.puntos > self.record_puntos:
            self.record_puntos = self.puntos
        
        self.mostrar_pantalla_fin(False, self.puntos, razon=razon)
    
    def mostrar_pantalla_fin(self, victoria, puntos_finales, bonus_tiempo=0, bonus_vidas=0, bonus_perfecto=0, razon=""):
        """Muestra la pantalla de fin de partida con un resumen visual profesional."""
        self.limpiar_ventana()
        
        config = NIVELES[self.nivel_actual]
        
        frame = tk.Frame(self.ventana, bg=COLORS["bg_dark"])
        frame.pack(expand=True, fill="both", padx=36, pady=28)
        
        frame_header = tk.Frame(frame, bg=COLORS["bg_dark"])
        frame_header.pack(fill="x")
        
        frame_badges = tk.Frame(frame_header, bg=COLORS["bg_dark"])
        frame_badges.pack(anchor="w")
        if victoria:
            titulo_texto = "VICTORIA"
            titulo_color = COLORS["green"]
            badge_color = COLORS["green"]
            status_badge = "PARTIDA GANADA"
            resumen_texto = "Has completado el nivel con estilo y acumulaste puntaje extra."
        else:
            titulo_texto = "DERROTA"
            titulo_color = COLORS["red"]
            badge_color = COLORS["red"]
            status_badge = "PARTIDA TERMINADA"
            resumen_texto = "Puedes volver a intentarlo con una nueva estrategia."
        
        crear_badge(frame_badges, status_badge, badge_color, COLORS["bg_medium"])
        crear_badge(frame_badges, f"Nivel {self.nivel_actual}: {config['nombre']}", config["color"], COLORS["bg_medium"])
        
        titulo = tk.Label(
            frame_header,
            text=titulo_texto,
            font=("Consolas", 54, "bold"),
            fg=titulo_color,
            bg=COLORS["bg_dark"]
        )
        titulo.pack(anchor="w", pady=(12, 4))
        
        lbl_resumen = tk.Label(
            frame_header,
            text=resumen_texto,
            font=("Consolas", 11),
            fg=COLORS["text_white"],
            bg=COLORS["bg_dark"]
        )
        lbl_resumen.pack(anchor="w")
        
        if not victoria and razon:
            lbl_razon = tk.Label(
                frame_header,
                text=razon,
                font=("Consolas", 10, "bold"),
                fg=COLORS["yellow"],
                bg=COLORS["bg_dark"]
            )
            lbl_razon.pack(anchor="w", pady=(6, 0))
        
        frame_panel = crear_panel(
            frame,
            COLORS["bg_medium"],
            padx=24,
            pady=24,
            highlight_color=COLORS["bg_light"],
            highlight_width=1
        )
        frame_panel.pack(fill="both", expand=True, pady=(20, 0))
        
        frame_stats_inner = tk.Frame(frame_panel, bg=COLORS["bg_medium"])
        frame_stats_inner.pack(fill="x")
        
        stats = [
            ("NIVEL", f"{self.nivel_actual}: {config['nombre']}", config["color"]),
            ("PALABRAS", f"{len(self.palabras_encontradas)}/{len(self.palabras_por_encontrar)}", COLORS["cyan"]),
            ("COMBO", f"x{self.mejor_combo}", COLORS["orange"]),
            ("PUNTOS BASE", str(self.puntos), COLORS["yellow"]),
        ]
        
        if victoria:
            if bonus_tiempo > 0:
                stats.append(("BONUS TIEMPO", f"+{bonus_tiempo}", COLORS["cyan"]))
            if bonus_vidas > 0:
                stats.append(("BONUS VIDAS", f"+{bonus_vidas}", COLORS["green"]))
            if bonus_perfecto > 0:
                stats.append(("JUEGO PERFECTO", f"+{bonus_perfecto}", COLORS["purple"]))
        
        for titulo_card, valor_card, color_card in stats:
            crear_tarjeta_estadistica(frame_stats_inner, titulo_card, valor_card, color_card)
        
        separador = tk.Frame(frame_panel, bg=COLORS["bg_light"], height=2)
        separador.pack(fill="x", pady=(18, 0))
        
        frame_total = tk.Frame(frame_panel, bg=COLORS["bg_medium"])
        frame_total.pack(fill="x", pady=(12, 0))
        
        lbl_total_titulo = tk.Label(
            frame_total,
            text="PUNTUACIÓN FINAL",
            font=("Consolas", 14, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_medium"]
        )
        lbl_total_titulo.pack(side="left")
        
        lbl_total_valor = tk.Label(
            frame_total,
            text=str(puntos_finales),
            font=("Consolas", 32, "bold"),
            fg=COLORS["yellow"],
            bg=COLORS["bg_medium"]
        )
        lbl_total_valor.pack(side="right")
        
        frame_botones = tk.Frame(frame, bg=COLORS["bg_dark"])
        frame_botones.pack(fill="x", pady=(20, 0))
        
        btn_reintentar = crear_boton_estilizado(
            frame_botones,
            "REINTENTAR",
            COLORS["cyan"],
            lambda: self.iniciar_partida(self.nivel_actual),
            ancho=15,
            alto=2,
            tamano_fuente=14
        )
        btn_reintentar.pack(side="left")
        
        if victoria and self.nivel_actual < 6:
            btn_siguiente = crear_boton_estilizado(
                frame_botones,
                "SIGUIENTE NIVEL",
                COLORS["green"],
                lambda: self.iniciar_partida(self.nivel_actual + 1),
                ancho=18,
                alto=2,
                tamano_fuente=14
            )
            btn_siguiente.pack(side="left", padx=(10, 0))
        
        btn_menu = crear_boton_estilizado(
            frame_botones,
            "MENU",
            COLORS["purple"],
            self.mostrar_menu_principal,
            ancho=15,
            alto=2,
            tamano_fuente=14
        )
        btn_menu.pack(side="left", padx=(10, 0))
    
    # --------------------------------------------------------
    # UTILIDADES
    # --------------------------------------------------------
    
    def confirmar_salir(self):
        """Confirma si el jugador quiere salir de la partida."""
        respuesta = messagebox.askyesno(
            "Salir",
            "Perderas el progreso de esta partida.\n\nSalir?"
        )
        
        if respuesta:
            self.mostrar_menu_principal()


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

def main():
    """Funcion principal que inicia el juego."""
    ventana = tk.Tk()
    juego = WordHunt(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
