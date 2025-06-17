import pygame

# Game size
COLUMNS = 10
ROWS = 20
CELL_SIZE = 40
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

# Side bar size
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

# Window
PADDING = 20
WINDOW_WIDHT = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# Game behaviour
UPDATE_START_SPEED = 300
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

# Colors
YELLOW = "#f1e60d"
RED = "#e51b20"
BLUE = "#204b9b"
GREEN = "#65b32e"
PURPLE = "#7b217f"
CYAN = "#6cc6d9"
ORANGE = "#f07e13"
GRAY = "#1C1C1C"
LINE_COLOR = "#FFFFFF"

# Shapes
TETROMINOS = {
    "T": {"shape": [(0, 0), (-1, 0), (1, 0), (0, -1)], "color": PURPLE},
    "O": {"shape": [(0, 0), (0, -1), (1, 0), (1, -1)], "color": YELLOW},
    "J": {"shape": [(0, 0), (0, -1), (0, 1), (-1, 1)], "color": BLUE},
    "L": {"shape": [(0, 0), (0, -1), (0, 1), (1, 1)], "color": ORANGE},
    "I": {"shape": [(0, 0), (0, -1), (0, -2), (0, 1)], "color": CYAN},
    "S": {"shape": [(0, 0), (-1, 0), (0, -1), (1, -1)], "color": GREEN},
    "Z": {"shape": [(0, 0), (1, 0), (0, -1), (-1, -1)], "color": RED}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}
START_LEVEL = 1
SPEEDUP_COEFF = 0.75  # ускорение для всех таймеров

# --- Дизайн и ресурсы ---

# Пути к шрифтам
FONT_MAIN = "PixeloidSans"
FONT_MAIN_SIZE = 32
FONT_TITLE_SIZE = 64
FONT_PATH = None  # если нужен путь к ttf-файлу, например: os.path.join("graphics", "PixeloidSans.ttf")

# Пути к спрайтам
MENU_BG_PATH = "graphics/menu_background(3).png"
BUTTON_SPRITE_PATH = "button(3).png"
PREVIEW_SPRITES = {shape: f"graphics/{shape}.png" for shape in TETROMINOS.keys()}

# Пути к звукам
MUSIC_PATH = "sound/tetris.mp3"
LANDING_SOUND_PATH = "sound/landing.wav"

# Громкость
DEFAULT_MUSIC_VOLUME = 0.5
DEFAULT_EFFECTS_VOLUME = 0.5

# --- Положение и размеры кнопок главного меню ---
MENU_BUTTON_WIDTH = 320
MENU_BUTTON_HEIGHT = 100
MENU_BUTTON_GAP = 120
MENU_BUTTON_START_Y = 300  # например, отступ сверху
MENU_BUTTON_CENTER_X = 325  # вычислять по центру экрана

# --- Положение и размеры кнопок меню настроек ---
SETTINGS_BUTTON_WIDTH = 320
SETTINGS_BUTTON_HEIGHT = 100
SETTINGS_BUTTON_GAP = 120
SETTINGS_BUTTON_START_Y = 220
SETTINGS_BUTTON_CENTER_X = None  # вычислять по центру экрана

# Главное меню
MENU_TITLE_X = None  # если None — по центру, иначе абсолютное значение
MENU_TITLE_Y = 230

# Меню настроек
SETTINGS_TITLE_X = None  # если None — по центру, иначе абсолютное значение
SETTINGS_TITLE_Y = 140

# --- Область меню (главное меню) ---
MENU_AREA_X = 30
MENU_AREA_Y = 180
MENU_AREA_WIDTH = 600
MENU_AREA_HEIGHT = 500

# --- Положение объектов внутри области ---
MENU_TITLE_Y = 5   # относительно области
MENU_BUTTON_START_Y = 120  # относительно области
MENU_BUTTON_GAP = 120

# --- Область меню (настроек) ---
SETTINGS_AREA_X = 30
SETTINGS_AREA_Y = 120
SETTINGS_AREA_WIDTH = 600
SETTINGS_AREA_HEIGHT = 500

SETTINGS_TITLE_Y = 80
SETTINGS_FIELD_START_Y = 150
SETTINGS_FIELD_GAP = 60
SETTINGS_SLIDER_START_Y = 300
SETTINGS_SLIDER_GAP = 70
SETTINGS_SLIDER_X = 100  # X-координата ползунков относительно области меню (например, 200)

# --- Подсказка в меню настроек ---
SETTINGS_HINT_TEXT = "←/→/мышь изменить, ↑/↓ выбрать, Esc - назад"
SETTINGS_HINT_COLOR = (180, 180, 180)
SETTINGS_HINT_Y_OFFSET = 0  # смещение по Y от нижнего края области меню
SETTINGS_HINT_FONT_SIZE = 15  # размер шрифта подсказки