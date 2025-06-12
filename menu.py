import pygame
import save_data
import settings

class Button:
    def __init__(self, text, pos, size, callback):
        self.rect = pygame.Rect(pos, size)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("arial", 32)
        self.color_idle = (180, 180, 180)
        self.color_hover = (120, 120, 255)
        self.color = self.color_idle

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, (30, 30, 30))
        text_rect = text_surf.get_rect(center=self.rect.center)
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
        self.selected = 0
        self.on_back = on_back

    def Update(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.save_settings()
                        self.on_back()
                        return
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.fields)
                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.fields)
                    if event.key == pygame.K_LEFT:
                        field = self.fields[self.selected]
                        if field["value"] > field["min"]:
                            field["value"] -= 1
                    if event.key == pygame.K_RIGHT:
                        field = self.fields[self.selected]
                        if field["value"] < field["max"]:
                            field["value"] += 1

            self.display_surface.fill(self.bg_color)
            title = self.font.render("Настройки", True, (255, 255, 255))
            self.display_surface.blit(title, (self.display_surface.get_width()//2 - title.get_width()//2, 80))

            for i, field in enumerate(self.fields):
                color = (255, 255, 0) if i == self.selected else (200, 200, 200)
                text = f"{field.get('label', field['name'])}: {field['value']}"
                surf = self.small_font.render(text, True, color)
                self.display_surface.blit(surf, (self.display_surface.get_width()//2 - 100, 180 + i*50))

            info = self.small_font.render("←/→ изменить, ↑/↓ выбрать, Esc - назад", True, (180, 180, 180))
            self.display_surface.blit(info, (self.display_surface.get_width()//2 - info.get_width()//2, 400))

            pygame.display.update()
            clock.tick(60)

    def save_settings(self):
        data = save_data.load_data()
        for field in self.fields:
            data[field["name"]] = field["value"]
            setattr(settings, field["name"], field["value"])
        save_data.save_data(data)

class Menu:
    def __init__(self, start_game, open_settings, show_authors):
        self.display_surface = pygame.display.get_surface()
        self.bg_color = (40, 40, 60)
        w, h = self.display_surface.get_size()
        btn_w, btn_h = 260, 60
        center_x = w // 2 - btn_w // 2
        start_y = h // 2 - 100

        self.buttons = [
            Button("Играть", (center_x, start_y), (btn_w, btn_h), start_game),
            Button("Настройки", (center_x, start_y + 80), (btn_w, btn_h), open_settings),
            Button("Авторы", (center_x, start_y + 160), (btn_w, btn_h), show_authors),
        ]
        self.title_font = pygame.font.SysFont("arial", 64, bold=True)

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
            self.display_surface.fill(self.bg_color)
            title_surf = self.title_font.render("MegaTetris", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(self.display_surface.get_width()//2, 120))
            self.display_surface.blit(title_surf, title_rect)
            for btn in self.buttons:
                btn.draw(self.display_surface)
            pygame.display.update()
            clock.tick(60)

