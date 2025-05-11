import sys
import abc
import pygame
import random
import os

pygame.init()

# Общие настройки
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
size = (1280, 720)  # Для меню
BACKGROUND = (50, 50, 50)  # Темный фон для меню
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 48)  # Читаемый шрифт
menu_font = pygame.font.SysFont('Arial', 36)  # Читаемый шрифт

# Цвета (лучше определить все используемые)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TEXT_COLOR = (220, 220, 220)  # Светло-серый для текста

# Классы игровых состояний
class State(abc.ABC):
    @abc.abstractmethod
    def handle_events(self, events):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self, screen):
        pass

class SplashScreen(State):
    def __init__(self):
        self.text = 'Заставка'
        self.surface = font.render(self.text, True, TEXT_COLOR)
        self.hint = 'Нажмите для продолжения'
        self.hint_surface = menu_font.render(self.hint, True, TEXT_COLOR)
        self.hint_visible = True
        self.hint_time = pygame.time.get_ticks()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return MainMenu(self.name if hasattr(self, 'name') else "Аноним")  # передаем имя в MainMenu
        return self

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.hint_time > 800:
            self.hint_visible = not self.hint_visible
            self.hint_time = current_time

    def draw(self, screen):
        screen.fill(BACKGROUND)

        rect = self.surface.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.centery = screen.get_rect().centery - 100
        screen.blit(self.surface, rect)

        if self.hint_visible:
            hint_rect = self.hint_surface.get_rect()
            hint_rect.centerx = screen.get_rect().centerx
            hint_rect.centery = screen.get_rect().centery + 100
            screen.blit(self.hint_surface, hint_rect)

class MainMenu(State):
    def __init__(self, player_name="Аноним"): # Имя игрока по умолчанию
        self.options = ["Играть", "Выбрать имя", "Выйти"]
        self.selected = 0
        self.menu_surfaces = [menu_font.render(opt, True, TEXT_COLOR) for opt in self.options]
        self.title = font.render("Главное меню", True, TEXT_COLOR)
        self.player_name = player_name # Сохраняем имя игрока

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # Enter key
                    if self.selected == 0:
                        return PuzzleGame(self.player_name)  # Передаем имя в PuzzleGame
                    elif self.selected == 1:
                        return NameInputScreen(self.player_name) # Передаем имя в NameInputScreen
                    elif self.selected == 2:
                        pygame.quit()
                        sys.exit()

        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BACKGROUND)

        title_rect = self.title.get_rect()
        title_rect.centerx = screen.get_rect().centerx
        title_rect.centery = 100
        screen.blit(self.title, title_rect)

        for i, surface in enumerate(self.menu_surfaces):
            color = GREEN if i == self.selected else TEXT_COLOR
            surface = menu_font.render(self.options[i], True, color)
            rect = surface.get_rect()
            rect.centerx = screen.get_rect().centerx
            rect.centery = 300 + i * 80
            screen.blit(surface, rect)

class NameInputScreen(State):
    def __init__(self, current_name="Аноним"): # Принимаем текущее имя
        self.name = current_name
        self.title = font.render("Введите имя:", True, TEXT_COLOR)
        self.name_surface = font.render(self.name, True, TEXT_COLOR)
        self.cursor = "|"
        self.cursor_visible = True
        self.cursor_time = pygame.time.get_ticks()
        self.back_text = menu_font.render("Нажмите ESC для возврата", True, TEXT_COLOR)
        # Инициализация cursor_surface здесь
        self.cursor_surface = font.render(self.cursor, True, TEXT_COLOR)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MainMenu(self.name)  # Возвращаем в меню с текущим именем
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    return MainMenu(self.name) #  Возвращаемся в меню с текущим именем
                else:
                    if len(self.name) < 15 and event.unicode.isprintable():
                        self.name += event.unicode
                self.name_surface = font.render(self.name, True, TEXT_COLOR)
        # Обновление cursor_surface при каждом изменении имени
        self.cursor_surface = font.render(self.cursor, True, TEXT_COLOR)

        return self

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_time > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_time = current_time

    def draw(self, screen):
        screen.fill(BACKGROUND)

        title_rect = self.title.get_rect()
        title_rect.centerx = screen.get_rect().centerx
        title_rect.centery = 200
        screen.blit(self.title, title_rect)

        name_rect = self.name_surface.get_rect()
        name_rect.centerx = screen.get_rect().centerx
        name_rect.centery = 300
        screen.blit(self.name_surface, name_rect)

        if self.cursor_visible:
            cursor_surface = font.render(self.cursor, True, TEXT_COLOR)
            cursor_rect = cursor_surface.get_rect()
            cursor_rect.midleft = name_rect.midright
            screen.blit(cursor_surface, cursor_rect)

        back_rect = self.back_text.get_rect()
        back_rect.centerx = screen.get_rect().centerx
        back_rect.centery = 400
        screen.blit(self.back_text, back_rect)

class PuzzleGame(State):
    def __init__(self, player_name): # Принимаем имя игрока
        # Настройки пазла
        self.SCREEN_WIDTH = 800  # Уменьшено для лучшего отображения в меню
        self.SCREEN_HEIGHT = 600  # Уменьшено для лучшего отображения в меню
        self.ROWS = 3
        self.COLS = 3
        self.MARGIN = 2
        self.BACKGROUND = BLACK  # Черный фон для пазла
        self.SELECT_COLOR = GREEN
        self.FONT_COLOR = TEXT_COLOR  # Светло-серый для текста в игре
        self.TIME_LIMIT = 60  # 60 секунд на сборку пазла
        self.MAX_SWAPS = 50  # Максимальное количество ходов

        # Имя игрока (используем переданное имя)
        self.player_name = player_name

        # Настройки экрана (используем экран меню)
        self.screen = pygame.display.get_surface()  # Используем экран из меню
        pygame.display.set_caption("Пазл")  # Заголовок для окна
        self.screen.fill(self.BACKGROUND)  # Цвет окна

        try:
            self.font = pygame.font.Font(None, 36)
        except:
            self.font = pygame.font.SysFont('arial', 36)

        self.picture_folder = 'picture'
        self.pictures = [f for f in os.listdir(self.picture_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

        self.picture = random.choice(self.pictures)
        self.image = pygame.image.load(os.path.join(self.picture_folder, self.picture))

        # Масштабирование изображения
        image_width, image_height = self.image.get_size()
        if image_width > self.SCREEN_WIDTH:
            scale = self.SCREEN_WIDTH / image_width
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
            self.image_width, self.image_height = self.image.get_size()
        else:
            self.image_width, self.image_height = self.image.get_size()

        self.TILE_WIDTH = self.image_width // self.COLS
        self.TILE_HEIGHT = self.image_height // self.ROWS

        self.tiles = []
        for i in range(self.ROWS):
            for j in range(self.COLS):
                rect = pygame.Rect(j * self.TILE_WIDTH, i * self.TILE_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)
                tile = self.image.subsurface(rect)
                self.tiles.append(tile)

        self.origin_tiles = self.tiles.copy()
        random.shuffle(self.tiles)

        self.selected = None
        self.swaps = 0
        self.completed = False
        self.game_over = False
        self.swaps_exceeded = False
        self.start_time = pygame.time.get_ticks()
        self.back_text = menu_font.render("Нажмите ESC для возврата", True, TEXT_COLOR)  # Светлый текст

    def get_remaining_time(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000  # в секундах
        remaining = max(0, self.TIME_LIMIT - elapsed)
        return remaining

    def draw_tiles(self):
        for i in range(len(self.tiles)):
            tile = self.tiles[i]
            row = i // self.ROWS
            col = i % self.COLS
            x = col * (self.TILE_WIDTH + self.MARGIN) + self.MARGIN
            y = row * (self.TILE_HEIGHT + self.MARGIN) + self.MARGIN
            self.screen.blit(tile, (x, y))
            if i == self.selected:
                pygame.draw.rect(self.screen, self.SELECT_COLOR,
                                 (x - 2, y - 2, self.TILE_WIDTH + 4, self.TILE_HEIGHT + 4), 3)

    def is_puzzle_completed(self):
        return all(tile == self.origin_tiles[i] for i, tile in enumerate(self.tiles))

    def draw_info(self):
        # Отображение оставшегося времени
        remaining_time = self.get_remaining_time()
        time_text = self.font.render(f"Время: {int(remaining_time)} сек", True, self.FONT_COLOR)
        self.screen.blit(time_text, (self.SCREEN_WIDTH - time_text.get_width() - 20, 20)) # выравнивание справа

        # Отображение имени игрока
        name_text = self.font.render(f"Игрок: {self.player_name}", True, self.FONT_COLOR)
        self.screen.blit(name_text, (20, 20))

        # Отображение ходов и оставшихся ходов
        swaps_text = self.font.render(f"Ходы: {self.swaps}/{self.MAX_SWAPS}", True, self.FONT_COLOR)
        self.screen.blit(swaps_text, (20, self.SCREEN_HEIGHT - 50))

        back_rect = self.back_text.get_rect()
        back_rect.centerx = self.SCREEN_WIDTH // 2
        back_rect.bottom = self.SCREEN_HEIGHT - 10 # выравнивание по нижнему краю
        self.screen.blit(self.back_text, back_rect)

        # Отображение результатов игры (центровка)
        if self.completed:
            result_text = self.font.render("Пазл собран!", True, GREEN)
        elif self.game_over:
            result_text = self.font.render("Время вышло!", True, RED)
        elif self.swaps_exceeded:
            result_text = self.font.render("Ходы закончились!", True, RED)
        else:
            result_text = None

        if result_text:
            text_rect = result_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(result_text, text_rect)

            restart_text = self.font.render("Нажмите R для рестарта", True, TEXT_COLOR)
            restart_rect = restart_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode(size)  # Возвращаем размер экрана к меню
                    return MainMenu(self.player_name) # Возвращаемся в MainMenu с именем
                elif event.key == pygame.K_r and (self.game_over or self.completed or self.swaps_exceeded):
                    return PuzzleGame(self.player_name)  # Рестарт игры

            if not self.game_over and not self.completed and not self.swaps_exceeded:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for i in range(len(self.tiles)):
                        row = i // self.ROWS
                        col = i % self.COLS
                        x = col * (self.TILE_WIDTH + self.MARGIN) + self.MARGIN
                        y = row * (self.TILE_HEIGHT + self.MARGIN) + self.MARGIN

                        if x <= mouse_x <= x + self.TILE_WIDTH and y <= mouse_y <= y + self.TILE_HEIGHT:
                            if self.selected is not None and self.selected != i:
                                self.tiles[i], self.tiles[self.selected] = self.tiles[self.selected], self.tiles[i]
                                self.selected = None
                                self.swaps += 1
                                self.completed = self.is_puzzle_completed()
                                if self.swaps >= self.MAX_SWAPS:  # Проверяем превышение лимита ходов
                                    self.swaps_exceeded = True
                            elif self.selected == i:
                                self.selected = None
                            else:
                                self.selected = i

        return self

    def update(self):
        if not self.completed and not self.game_over and not self.swaps_exceeded:
            if self.get_remaining_time() <= 0:
                self.game_over = True
            if self.swaps >= self.MAX_SWAPS:
                self.swaps_exceeded = True

    def draw(self, screen):
        # Используем screen, переданный из основного цикла (это экран меню)
        self.screen.fill(self.BACKGROUND)
        self.draw_tiles()
        self.draw_info()
        pygame.display.flip()

# Инициализация и запуск игры
pygame.display.set_mode(size)  # Устанавливаем размер экрана для меню
state = SplashScreen()  # начинаем с заставки
while True:
    events = pygame.event.get()
    next_state = state.handle_events(events)

    if next_state is not state:
        if isinstance(next_state, PuzzleGame):  # Если переходим в игру
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Устанавливаем размер экрана для игры
        else:
            pygame.display.set_mode(size)  # Возвращаемся в размер экрана для меню
        state = next_state  # Переключаем состояние

    state.update()
    state.draw(pygame.display.get_surface())  # Используем текущий экран
    pygame.display.flip()
    clock.tick(FPS)
