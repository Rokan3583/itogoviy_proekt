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
    def __init__(self, player_name="Аноним"):  # Add player_name parameter
        self.text = 'Заставка'
        self.surface = font.render(self.text, True, TEXT_COLOR)
        self.hint = 'Нажмите для продолжения'
        self.hint_surface = menu_font.render(self.hint, True, TEXT_COLOR)
        self.hint_visible = True
        self.hint_time = pygame.time.get_ticks()
        self.player_name = player_name  # Store player_name

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return MainMenu(self.player_name)  # Pass the name to MainMenu
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
    def __init__(self, player_name="Аноним"):  # Make player_name optional
        self.options = ["Играть", "Выбрать имя", "Выйти"]
        self.selected = 0
        self.menu_surfaces = [menu_font.render(opt, True, TEXT_COLOR) for opt in self.options]
        self.title = font.render("Главное меню", True, TEXT_COLOR)
        self.player_name = player_name  # Save the name
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
                        return PuzzleGame(self.player_name)  # Pass the name to PuzzleGame
                    elif self.selected == 1:
                        return NameInputScreen(self.player_name)  # Pass the name to NameInputScreen
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
    def __init__(self, current_name="Аноним"):  # Take player name as parameter
        self.name = current_name
        self.title = font.render("Введите имя:", True, TEXT_COLOR)
        self.name_surface = font.render(self.name, True, TEXT_COLOR)
        self.cursor = "|"
        self.cursor_visible = True
        self.cursor_time = pygame.time.get_ticks()
        self.back_text = menu_font.render("Нажмите ESC для возврата", True, TEXT_COLOR)
        self.cursor_surface = font.render(self.cursor, True, TEXT_COLOR)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MainMenu(self.name)  # Return to MainMenu with current name
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    return MainMenu(self.name)  # Return to MainMenu with current name
                else:
                    if len(self.name) < 15 and event.unicode.isprintable():
                        self.name += event.unicode
                self.name_surface = font.render(self.name, True, TEXT_COLOR)
        # Update cursor surface with the same color
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
    def __init__(self, player_name, level=1):  # Accept level
        # Settings depending on the level
        self.level = level
        self.ROWS = self.COLS = self.calculate_tile_count(level)  # Dynamic rows and cols
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.MARGIN = 2
        self.BACKGROUND = BLACK
        self.SELECT_COLOR = GREEN
        self.FONT_COLOR = TEXT_COLOR
        self.TIME_LIMIT = 60 + ((self.ROWS - 2)) * 15 # More time for each level + each tile
        self.MAX_SWAPS = 50 + ((self.ROWS - 2)) * 10  # More moves for each level + each tile

        # Player details
        self.player_name = player_name

        # Pygame setup
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption(f"Пазл - Уровень {self.level}")
        self.screen.fill(self.BACKGROUND)

        try:
            self.font = pygame.font.Font(None, 36)
        except:
            self.font = pygame.font.SysFont('arial', 36)

        # Load image
        self.picture_folder = 'picture'
        self.pictures = [f for f in os.listdir(self.picture_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.picture = random.choice(self.pictures)
        self.image = pygame.image.load(os.path.join(self.picture_folder, self.picture))

        # Scale the image
        image_width, image_height = self.image.get_size()
        if image_width > self.SCREEN_WIDTH:
            scale = self.SCREEN_WIDTH / image_width
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.image_width, self.image_height = self.image.get_size()

        # Calculate tile sizes
        self.TILE_WIDTH = self.image_width // self.COLS
        self.TILE_HEIGHT = self.image_height // self.ROWS

        # Create tiles
        self.tiles = []
        for i in range(self.ROWS):
            for j in range(self.COLS):
                rect = pygame.Rect(j * self.TILE_WIDTH, i * self.TILE_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)
                tile = self.image.subsurface(rect)
                self.tiles.append(tile)

        self.origin_tiles = self.tiles.copy()
        random.shuffle(self.tiles)

        # Game state variables
        self.selected = None
        self.swaps = 0
        self.completed = False
        self.game_over = False
        self.swaps_exceeded = False
        self.start_time = pygame.time.get_ticks()
        self.back_text = menu_font.render("Нажмите ESC для возврата", True, TEXT_COLOR)  # Светлый текст

    def calculate_tile_count(self, level):
        # Increase tiles every 5 levels
        tile_level = (level - 1) // 5  # Integer division to get "tile level"
        if tile_level == 0:
            return 3  # Levels 1-4: 3x3
        elif tile_level == 1:
            return 4  # Levels 5-9: 4x4
        elif tile_level == 2:
            return 5  # Levels 10-14: 5x5
        else:
            return 6  #Levels 15+: 6x6

    def get_remaining_time(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
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
                pygame.draw.rect(self.screen, self.SELECT_COLOR, (x - 2, y - 2, self.TILE_WIDTH + 4, self.TILE_HEIGHT + 4), 3)

    def is_puzzle_completed(self):
        return all(tile == self.origin_tiles[i] for i, tile in enumerate(self.tiles))

    def draw_info(self):
        # Time display
        remaining_time = self.get_remaining_time()
        time_text = self.font.render(f"Время: {int(remaining_time)} сек", True, self.FONT_COLOR)
        self.screen.blit(time_text, (self.SCREEN_WIDTH - time_text.get_width() - 20, 20))

        # Player name display
        name_text = self.font.render(f"Игрок: {self.player_name}", True, self.FONT_COLOR)
        self.screen.blit(name_text, (20, 20))

        # Swaps and level
        swaps_text = self.font.render(f"Ходы: {self.swaps}/{self.MAX_SWAPS}", True, self.FONT_COLOR)
        level_text = self.font.render(f"Уровень: {self.level}", True, self.FONT_COLOR)
        self.screen.blit(swaps_text, (20, self.SCREEN_HEIGHT - 80))
        self.screen.blit(level_text, (20, self.SCREEN_HEIGHT - 50))

        # "Press ESC"
        back_rect = self.back_text.get_rect()
        back_rect.centerx = self.SCREEN_WIDTH // 2
        back_rect.bottom = self.SCREEN_HEIGHT - 10
        self.screen.blit(self.back_text, back_rect)

        # Game outcome display
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
                    pygame.display.set_mode(size)  # Back to menu
                    return MainMenu(self.player_name) # Back to MainMenu
                elif event.key == pygame.K_r and (self.game_over or self.completed or self.swaps_exceeded):
                    return PuzzleGame(self.player_name, self.level)  # Restart current level

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
                                if self.swaps >= self.MAX_SWAPS:
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
        # Use the provided screen from the main loop
        self.screen.fill(self.BACKGROUND)
        self.draw_tiles()
        self.draw_info()
        pygame.display.flip()

# Set up the main loop to keep track of the level
pygame.display.set_mode(size)
player_name = "Аноним"  # Initialize a player_name variable

# Start with the splash screen, passing player_name
state = SplashScreen(player_name)

while True:
    events = pygame.event.get()
    if isinstance(state, PuzzleGame) and state.completed:
        # If puzzle is completed, move to the next level with same player_name
        level = state.level + 1
        player_name = state.player_name  # Keep the current player name
        state = PuzzleGame(player_name, level)
    else:
        next_state = state.handle_events(events)

        if next_state is not state:
            if isinstance(next_state, PuzzleGame):
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            else:
                pygame.display.set_mode(size)
            state = next_state

    state.update()
    state.draw(pygame.display.get_surface())
    pygame.display.flip()
    clock.tick(FPS)