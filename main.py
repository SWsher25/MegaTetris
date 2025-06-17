from settings import *
import settings
from sys import exit
from os.path import join
import save_data
import os

# components
from game import Game
from score import Score
from preview import Preview
from menu import Menu, SettingsMenu

from random import choice

data = save_data.load_data()
for key, value in data.items():
    setattr(settings, key, value)

# Главный игровой класс. Управляет игровой сессией, инициализирует все игровые компоненты (поле, счёт, предпросмотр фигур, музыку).
class Main():
    # Инициализация компонентов, обращение к классам, определение переменных с настройками
    # Создаёт окно, инициализирует очередь фигур, игровые компоненты, музыку.
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("MegaTetris")

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # components
        self.game = Game(self.get_next_shape, self.update_score)
        # Передаём стартовые значения в Score
        self.score = Score(
            score=self.game.current_score,
            level=self.game.current_level,
            lines=self.game.current_lines
        )
        self.preview = Preview()

        # audio
        self.music = pygame.mixer.Sound(settings.MUSIC_PATH)
        self.music.set_volume(save_data.load_data().get("MUSIC_VOLUME", settings.DEFAULT_MUSIC_VOLUME))
        self.music.play(-1)  # -1 — зацикливание

        # font
        # self.font = pygame.font.SysFont(settings.FONT_MAIN, settings.FONT_MAIN_SIZE)
        # self.title_font = pygame.font.SysFont(settings.FONT_MAIN, settings.FONT_TITLE_SIZE, bold=True)
        # bg_path = os.path.join(os.path.dirname(__file__), settings.MENU_BG_PATH)
        # button_sprite_path = settings.BUTTON_SPRITE_PATH

    # Обновляет значения счёта, уровня и линий в панели Score.
    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    # Получение следующей фигуры
    # Возвращает следующую фигуру из очереди и добавляет новую случайную в конец очереди.
    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0) # удаляем первую фигуру в списке отображаемых фигур
        self.next_shapes.append(choice(list(TETROMINOS.keys()))) # с помощью метода choice выбираем фигуру и добавляем её в список отображаемых фигур
        return next_shape

    # Метод обновления
    # Главный игровой цикл. Обрабатывает события, обновляет состояние игры и интерфейса.
    def Update(self):
        running = True # пока эта переменная == True - игра идёт
        #Основной игровой цикл
        while running:
            # Обработка событий пользователя
            for event in pygame.event.get():
                # обработка выхода(чтобы окно можно было закрыть, нажав на крестик в углу)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Обработка выхода из игры по кнопке Escape
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False  # выйти из игрового цикла
            # Ещё одна обработка события выхода, в этот раз после проигрыша
            if self.game.game_over: running = False

            # Display
            self.display_surface.fill(GRAY)

            # Вызываем метод Update во всех вспомогательных классах, в которых он есть
            self.game.Update()      # игровое поле и фигуры
            self.score.Update()     # панель счёта
            self.preview.Update(self.next_shapes)  # предпросмотр фигур
            pygame.display.update()
            self.clock.tick()       # ограничение FPS

    # Останавливает фоновую музыку (вызывается при завершении игровой сессии).
    def stop_music(self):
        if hasattr(self, "music"):
            self.music.stop()

# Запускает игровую сессию. После завершения останавливает музыку.
def start_game():
    main = Main()
    main.Update()
    main.stop_music()  # Остановить музыку после выхода из игрового цикла

# Открывает меню настроек.
def open_settings():
    settings_menu = SettingsMenu(menu.Update)
    settings_menu.Update()

# Завершает работу приложения.
def exit_game():
    pygame.quit()
    exit()

# Стандартное условие для pygame, инициализируется сама библиотека, так же создаём экземпляр класса Menu
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))
    menu = Menu(start_game, open_settings, exit_game)
    while True:
        menu.Update()