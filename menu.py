import pygame
import os
import settings
import save_data

class Button:
    def __init__(self, text, pos, size, callback, sprite_path=None, sprite_size=None):
        self.rect = pygame.Rect(pos, size)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("PixeloidSans", 32)
        self.color_idle = (180, 180, 180)
        self.color_hover = (120, 120, 255)
        self.color = self.color_idle
        #self.sprite = None
        if sprite_path:
            import os
            try:
                sprite_full_path = os.path.join(os.path.dirname(__file__), "graphics", sprite_path)
                image = pygame.image.load(sprite_full_path).convert_alpha()
                # Масштабируем спрайт до нужного размера
                if sprite_size:
                    self.sprite = pygame.transform.smoothscale(image, sprite_size)
                else:
                    self.sprite = pygame.transform.smoothscale(image, (size[0], size[1]))
            except Exception:
                self.sprite = None  # если файл не найден, просто не используем спрайт

    def draw(self, surface):
        if self.sprite:
            # Растягиваем спрайт на всю кнопку
            scaled_sprite = pygame.transform.smoothscale(self.sprite, (self.rect.width, self.rect.height))
            surface.blit(scaled_sprite, self.rect)
        # Цвета
        outline_color = "#f07e13"  # чёрная обводка
        text_color = "white" # основной цвет текста
        # Текст
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        # Обводка: рисуем текст вокруг центра сдвигами
        # for dx in [-2, 0, 2]:
        #     for dy in [-2, 0, 2]:
        #         if dx != 0 or dy != 0:
        #             outline_surf = self.font.render(self.text, True, outline_color)
        #             outline_rect = outline_surf.get_rect(center=(self.rect.centerx + dx, self.rect.centery + dy))
        #             surface.blit(outline_surf, outline_rect)
        # Основной текст
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.color = self.color_hover if self.rect.collidepoint(event.pos) else self.color_idle
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class Menu:
    def __init__(self, start_game, open_settings, exit_game):
        self.display_surface = pygame.display.get_surface()
        # Область меню
        self.menu_area = pygame.Rect(
            settings.MENU_AREA_X,
            settings.MENU_AREA_Y,
            settings.MENU_AREA_WIDTH,
            settings.MENU_AREA_HEIGHT
        )
        btn_w = settings.MENU_BUTTON_WIDTH
        btn_h = settings.MENU_BUTTON_HEIGHT
        gap = settings.MENU_BUTTON_GAP
        # Кнопки внутри области
        center_x = self.menu_area.x + self.menu_area.width // 2 - btn_w // 2
        start_y = self.menu_area.y + settings.MENU_BUTTON_START_Y

        self.buttons = [
            Button("Играть", (center_x, start_y), (btn_w, btn_h), start_game, sprite_path=settings.BUTTON_SPRITE_PATH),
            Button("Настройки", (center_x, start_y + gap), (btn_w, btn_h), open_settings, sprite_path=settings.BUTTON_SPRITE_PATH),
            Button("Выход", (center_x, start_y + 2 * gap), (btn_w, btn_h), exit_game, sprite_path=settings.BUTTON_SPRITE_PATH),
        ]
        self.title_font = pygame.font.SysFont("PixeloidSans", 64, bold=True)
        # Загружаем фон один раз!
        bg_path = os.path.join(os.path.dirname(__file__), settings.MENU_BG_PATH)
        try:
            self.bg_sprite = pygame.image.load(bg_path).convert()
            self.bg_sprite = pygame.transform.smoothscale(self.bg_sprite, self.display_surface.get_size())
        except Exception:
            self.bg_sprite = None

    def Update(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for btn in self.buttons:
                    btn.handle_event(event)
            # Используем уже загруженный фон!
            if self.bg_sprite:
                self.display_surface.blit(self.bg_sprite, (0, 0))
            else:
                self.display_surface.fill(self.bg_color)
            # --- Больше не рисуем area_surface! ---
            # Заголовок
            title_surf = self.title_font.render("MegaTetris", True, (255, 255, 255))
            title_x = self.menu_area.x + self.menu_area.width // 2 - title_surf.get_width() // 2
            title_y = self.menu_area.y + settings.MENU_TITLE_Y
            self.display_surface.blit(title_surf, (title_x, title_y))
            # Кнопки
            for btn in self.buttons:
                btn.draw(self.display_surface)
            pygame.display.update()
            clock.tick(60)

class SettingsMenu:
    def __init__(self, on_back):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(settings.FONT_MAIN, settings.FONT_MAIN_SIZE)
        self.small_font = pygame.font.SysFont(settings.FONT_MAIN, 24)
        self.hint_font = pygame.font.SysFont(settings.FONT_MAIN, getattr(settings, "SETTINGS_HINT_FONT_SIZE", 24))
        data = save_data.load_data()
        self.fields = [
            {
                "name": "START_LEVEL",
                "label": "Начальный уровень",
                "value": data.get("START_LEVEL", settings.START_LEVEL),
                "min": 1,
                "max": 10
            },
        ]
        self.music_volume = data.get("MUSIC_VOLUME", 0.5)
        self.effects_volume = data.get("EFFECTS_VOLUME", 0.5)
        self.selected = 0
        self.on_back = on_back

        # Область меню
        self.menu_area = pygame.Rect(
            settings.SETTINGS_AREA_X,
            settings.SETTINGS_AREA_Y,
            settings.SETTINGS_AREA_WIDTH,
            settings.SETTINGS_AREA_HEIGHT
        )
        # Загружаем фон один раз!
        bg_path = os.path.join(os.path.dirname(__file__), settings.MENU_BG_PATH)
        try:
            self.bg_sprite = pygame.image.load(bg_path).convert()
            self.bg_sprite = pygame.transform.smoothscale(self.bg_sprite, self.display_surface.get_size())
        except Exception:
            self.bg_sprite = None

    def draw_slider(self, x, y, value, label, selected=False):
        bar_width = 200
        bar_height = 8
        slider_radius = 12
        pygame.draw.rect(self.display_surface, (180,180,180), (x, y, bar_width, bar_height), border_radius=4)
        slider_x = x + int(bar_width * value)
        pygame.draw.circle(self.display_surface, (255,255,0) if selected else (220,220,0), (slider_x, y + bar_height//2), slider_radius)
        text = self.small_font.render(f"{label}: {int(value*100)}%", True, (255,255,255))
        self.display_surface.blit(text, (x, y - 30))
        return pygame.Rect(slider_x-slider_radius, y + bar_height//2-slider_radius, slider_radius*2, slider_radius*2), pygame.Rect(x, y, bar_width, bar_height)

    def Update(self):
        running = True
        clock = pygame.time.Clock()
        dragging = None
        slider_x = self.menu_area.x + settings.SETTINGS_SLIDER_X
        slider_y_music = self.menu_area.y + settings.SETTINGS_SLIDER_START_Y
        slider_y_effects = slider_y_music + settings.SETTINGS_SLIDER_GAP
        bar_width = 200
        slider_radius = 12

        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            # --- вычисляем положение полос и кружков ползунков ---
            music_slider_center = (slider_x + int(bar_width * self.music_volume), slider_y_music + 4)
            effects_slider_center = (slider_x + int(bar_width * self.effects_volume), slider_y_effects + 4)
            music_slider_circle = pygame.Rect(
                music_slider_center[0] - slider_radius, music_slider_center[1] - slider_radius,
                slider_radius * 2, slider_radius * 2
            )
            effects_slider_circle = pygame.Rect(
                effects_slider_center[0] - slider_radius, effects_slider_center[1] - slider_radius,
                slider_radius * 2, slider_radius * 2
            )
            music_slider_bar = pygame.Rect(slider_x, slider_y_music, bar_width, 16)
            effects_slider_bar = pygame.Rect(slider_x, slider_y_effects, bar_width, 16)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and not dragging:
                    if event.key == pygame.K_ESCAPE:
                        self.save_settings()
                        self.on_back()
                        return
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % (len(self.fields) + 2)
                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % (len(self.fields) + 2)
                    if event.key == pygame.K_LEFT:
                        if self.selected < len(self.fields):
                            field = self.fields[self.selected]
                            if field["value"] > field["min"]:
                                field["value"] -= 1
                        elif self.selected == len(self.fields):
                            self.music_volume = max(0.0, self.music_volume - 0.05)
                        elif self.selected == len(self.fields) + 1:
                            self.effects_volume = max(0.0, self.effects_volume - 0.05)
                    if event.key == pygame.K_RIGHT:
                        if self.selected < len(self.fields):
                            field = self.fields[self.selected]
                            if field["value"] < field["max"]:
                                field["value"] += 1
                        elif self.selected == len(self.fields):
                            self.music_volume = min(1.0, self.music_volume + 0.05)
                        elif self.selected == len(self.fields) + 1:
                            self.effects_volume = min(1.0, self.effects_volume + 0.05)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if music_slider_circle.collidepoint(mouse_pos) or music_slider_bar.collidepoint(mouse_pos):
                        dragging = "music"
                    elif effects_slider_circle.collidepoint(mouse_pos) or effects_slider_bar.collidepoint(mouse_pos):
                        dragging = "effects"
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = None

            # Drag-and-drop мышью (всегда после обработки событий)
            if dragging == "music" and mouse_pressed:
                rel_x = min(max(mouse_pos[0] - slider_x, 0), bar_width)
                self.music_volume = rel_x / bar_width
            if dragging == "effects" and mouse_pressed:
                rel_x = min(max(mouse_pos[0] - slider_x, 0), bar_width)
                self.effects_volume = rel_x / bar_width

            # Используем уже загруженный фон!
            if self.bg_sprite:
                self.display_surface.blit(self.bg_sprite, (0, 0))
            else:
                self.display_surface.fill((30, 30, 50))

            # Заголовок
            title = self.font.render("Настройки", True, (255, 255, 255))
            title_x = self.menu_area.x + self.menu_area.width // 2 - title.get_width() // 2
            title_y = self.menu_area.y + settings.SETTINGS_TITLE_Y
            self.display_surface.blit(title, (title_x, title_y))

            # Поля
            for i, field in enumerate(self.fields):
                color = (255, 255, 0) if i == self.selected else (200, 200, 200)
                text = f"{field.get('label', field['name'])}: {field['value']}"
                surf = self.small_font.render(text, True, color)
                field_x = self.menu_area.x + self.menu_area.width // 2 - surf.get_width() // 2
                field_y = self.menu_area.y + settings.SETTINGS_FIELD_START_Y + i * settings.SETTINGS_FIELD_GAP
                self.display_surface.blit(surf, (field_x, field_y))

            # Ползунки
            self.draw_slider(
                slider_x, slider_y_music, self.music_volume, "Громкость музыки", self.selected == len(self.fields)
            )
            self.draw_slider(
                slider_x, slider_y_effects, self.effects_volume, "Громкость эффектов", self.selected == len(self.fields)+1
            )

            # Подсказка
            info = self.hint_font.render(settings.SETTINGS_HINT_TEXT, True, settings.SETTINGS_HINT_COLOR)
            info_x = self.menu_area.x + self.menu_area.width // 2 - info.get_width() // 2
            info_y = self.menu_area.y + self.menu_area.height + settings.SETTINGS_HINT_Y_OFFSET
            self.display_surface.blit(info, (info_x, info_y))

            pygame.display.update()
            clock.tick(60)

    def save_settings(self):
        data = save_data.load_data()
        for field in self.fields:
            data[field["name"]] = field["value"]
            setattr(settings, field["name"], field["value"])
        data["MUSIC_VOLUME"] = self.music_volume
        data["EFFECTS_VOLUME"] = self.effects_volume
        save_data.save_data(data)

