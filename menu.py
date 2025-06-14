import pygame
import os
import save_data
import settings

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

class SettingsMenu:
    def __init__(self, on_back):
        self.display_surface = pygame.display.get_surface()
        self.bg_color = (30, 30, 50)
        self.font = pygame.font.SysFont("arial", 32)
        self.small_font = pygame.font.SysFont("arial", 24)
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
        # Ползунки для громкости
        self.music_volume = data.get("MUSIC_VOLUME", 0.5)
        self.effects_volume = data.get("EFFECTS_VOLUME", 0.5)
        self.selected = 0
        self.on_back = on_back

        # Загрузка фонового спрайта (как в Menu)
        w, h = self.display_surface.get_size()
        bg_path = os.path.join(os.path.dirname(__file__), "graphics", "menu_background(3).png")
        try:
            self.bg_sprite = pygame.image.load(bg_path).convert()
            self.bg_sprite = pygame.transform.smoothscale(self.bg_sprite, (w, h))
        except Exception:
            self.bg_sprite = None

    def draw_slider(self, x, y, value, label, selected=False):
        bar_width = 200
        bar_height = 8
        slider_radius = 12
        # Бар
        pygame.draw.rect(self.display_surface, (180,180,180), (x, y, bar_width, bar_height), border_radius=4)
        # Ползунок
        slider_x = x + int(bar_width * value)
        pygame.draw.circle(self.display_surface, (255,255,0) if selected else (220,220,0), (slider_x, y + bar_height//2), slider_radius)
        # Подпись
        text = self.small_font.render(f"{label}: {int(value*100)}%", True, (255,255,255))
        self.display_surface.blit(text, (x, y - 30))
        return pygame.Rect(slider_x-slider_radius, y + bar_height//2-slider_radius, slider_radius*2, slider_radius*2), pygame.Rect(x, y, bar_width, bar_height)

    def Update(self):
        running = True
        clock = pygame.time.Clock()
        dragging = None  # None, "music", "effects"
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
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
                    if dragging is None:
                        # Проверяем, захватывает ли мышь ползунок
                        for i in range(2):
                            slider_x, slider_y = 220, 220 + i * 70
                            slider_rect, bar_rect = self.draw_slider(slider_x, slider_y, self.music_volume if i == 0 else self.effects_volume, "Громкость музыки" if i == 0 else "Громкость эффектов")
                            if slider_rect.collidepoint(event.pos):
                                dragging = "music" if i == 0 else "effects"
                                break
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = None

            if dragging == "music":
                # Перетаскивание ползунка музыки
                self.music_volume = (mouse_pos[0] - 220) / 200
                self.music_volume = max(0.0, min(1.0, self.music_volume))
            elif dragging == "effects":
                # Перетаскивание ползунка эффектов
                self.effects_volume = (mouse_pos[0] - 220) / 200
                self.effects_volume = max(0.0, min(1.0, self.effects_volume))

            # Рисуем фон
            if self.bg_sprite:
                self.display_surface.blit(self.bg_sprite, (0, 0))
            else:
                self.display_surface.fill(self.bg_color)

            title = self.font.render("Настройки", True, (255, 255, 255))
            self.display_surface.blit(title, (self.display_surface.get_width()//2 - title.get_width()//2, 140))

            for i, field in enumerate(self.fields):
                color = (255, 255, 0) if i == self.selected else (200, 200, 200)
                text = f"{field.get('label', field['name'])}: {field['value']}"
                surf = self.small_font.render(text, True, color)
                self.display_surface.blit(surf, (self.display_surface.get_width()//2 - 100, 220 + i*50))

            # Ползунки
            slider_x = self.display_surface.get_width()//2 - 100
            slider_y_music = 220 + len(self.fields)*50 + 40
            slider_y_effects = slider_y_music + 70

            self.draw_slider(slider_x, slider_y_music, self.music_volume, "Громкость музыки")
            self.draw_slider(slider_x, slider_y_effects, self.effects_volume, "Громкость эффектов")

            # Подсветка выбранного ползунка
            if self.selected == len(self.fields):
                pygame.draw.rect(self.display_surface, (255,255,0), (slider_x-10, slider_y_music-35, 220, 50), 2, 4)
            if self.selected == len(self.fields)+1:
                pygame.draw.rect(self.display_surface, (255,255,0), (slider_x-10, slider_y_effects-35, 220, 50), 2, 4)

            info = self.small_font.render("←/→ изменить, ↑/↓ выбрать, Esc - назад", True, (180, 180, 180))
            self.display_surface.blit(info, (self.display_surface.get_width()//2 - info.get_width()//2, slider_y_effects + 60))

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

class Menu:
    def __init__(self, start_game, open_settings, exit_game):
        self.display_surface = pygame.display.get_surface()
        self.bg_color = (40, 40, 60)
        w, h = self.display_surface.get_size()
        btn_w, btn_h = 320, 100
        center_x = w // 2 - btn_w // 2
        start_y = h // 2 - 120
        gap = 120

        # Загрузка фонового спрайта
        bg_path = os.path.join(os.path.dirname(__file__), "graphics", "menu_background(3).png")
        try:
            self.bg_sprite = pygame.image.load(bg_path).convert()
            self.bg_sprite = pygame.transform.smoothscale(self.bg_sprite, (w, h))
        except Exception:
            self.bg_sprite = None

        self.buttons = [
            Button("Играть", (center_x, start_y), (btn_w, btn_h), start_game, sprite_path="button(3).png"),
            Button("Настройки", (center_x, start_y + gap), (btn_w, btn_h), open_settings, sprite_path="button(3).png"),
            Button("Выход", (center_x, start_y + 2 * gap), (btn_w, btn_h), exit_game, sprite_path="button(3).png"),
        ]
        self.title_font = pygame.font.SysFont("PixeloidSans", 64, bold=True)

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
            # Рисуем фон
            if self.bg_sprite:
                self.display_surface.blit(self.bg_sprite, (0, 0))
            else:
                self.display_surface.fill(self.bg_color)
            # Рисуем заголовок и кнопки
            title_surf = self.title_font.render("MegaTetris", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(self.display_surface.get_width()//2, 230))
            self.display_surface.blit(title_surf, title_rect)
            for btn in self.buttons:
                btn.draw(self.display_surface)
            pygame.display.update()
            clock.tick(60)

