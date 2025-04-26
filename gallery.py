import pygame

# Stałe
THUMBNAIL_SIZE = (200, 200)
SPACING = 50
FONT_SIZE = 24
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

class Gallery:
    def __init__(self, images):
        self.images = images
        self.selected_index = 0
        self.current_page = 0
        self.font = pygame.font.SysFont("Courier", FONT_SIZE)   # Główna czcionka (np. legenda, loading, input)
        self.title_font = pygame.font.SysFont("Courier", 18, bold=True)  # Czcionka podpisów miniatur (mniejsza + bold)

        self.columns = SCREEN_WIDTH // (THUMBNAIL_SIZE[0] + SPACING)
        self.rows = (SCREEN_HEIGHT - 180) // (THUMBNAIL_SIZE[1] + SPACING)  # 180px na legendę, loading, input
        self.images_per_page = self.columns * self.rows

    def handle_input(self, key):
        if key == pygame.K_RIGHT:
            self.selected_index = (self.selected_index + 1) % len(self.images_on_page())
        elif key == pygame.K_LEFT:
            self.selected_index = (self.selected_index - 1) % len(self.images_on_page())
        elif key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + self.columns) % len(self.images_on_page())
        elif key == pygame.K_UP:
            self.selected_index = (self.selected_index - self.columns) % len(self.images_on_page())
        elif key == pygame.K_a:
            if self.current_page > 0:
                self.current_page -= 1
                self.selected_index = 0
        elif key == pygame.K_d:
            if (self.current_page + 1) * self.images_per_page < len(self.images):
                self.current_page += 1
                self.selected_index = 0

    def images_on_page(self):
        start_index = self.current_page * self.images_per_page
        end_index = start_index + self.images_per_page
        return self.images[start_index:end_index]

    def draw(self, screen, loading, input_active=False, user_input_text=""):
        screen.fill(BLACK)

        # --- Rysujemy legendę ---
        legend_text = "[A] Poprzednia strona   [D] Następna strona   [Enter] Powiększ obraz   [Esc] Wyjście   [F] Wyszukiwanie"
        legend_surface = self.font.render(legend_text, True, WHITE)
        legend_rect = legend_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(legend_surface, legend_rect)

        # --- Jeśli ładowanie trwa, pokazujemy napis ---
        if loading:
            loading_text = "LOADING..."
            loading_surface = self.font.render(loading_text, True, BLUE)
            loading_rect = loading_surface.get_rect(center=(SCREEN_WIDTH // 2, 70))
            screen.blit(loading_surface, loading_rect)

        # --- Rysujemy miniaturki + tytuły ---
        images_to_draw = self.images_on_page()

        for idx, img_data in enumerate(images_to_draw):
            row = idx // self.columns
            col = idx % self.columns
            x = col * (THUMBNAIL_SIZE[0] + SPACING) + (SPACING // 2)
            y = row * (THUMBNAIL_SIZE[1] + SPACING) + 110  # odsuń miniaturki niżej

            if idx == self.selected_index:
                pygame.draw.rect(screen, BLUE, (x - 5, y - 5, THUMBNAIL_SIZE[0] + 10, THUMBNAIL_SIZE[1] + 10), 3)

            screen.blit(img_data.surface, (x, y))

            # podpis pod miniaturką
            title_surface = self.title_font.render(img_data.title[:20], True, BLUE)
            screen.blit(title_surface, (x, y + THUMBNAIL_SIZE[1] + 5))

        # --- Rysujemy informację o stronie ---
        if self.images:
            total_pages = max(1, (len(self.images) + self.images_per_page - 1) // self.images_per_page)
            page_info_text = f"Strona {self.current_page + 1}/{total_pages}"
            page_info_surface = self.font.render(page_info_text, True, BLUE)
            page_info_rect = page_info_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
            screen.blit(page_info_surface, page_info_rect)

        # --- Rysujemy input box do wpisywania wyszukiwania ---
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 50, 400, 30)
        pygame.draw.rect(screen, BLUE, input_box, 2)

        if input_active:
            input_text_surface = self.font.render(user_input_text + "|", True, WHITE)
        else:
            input_text_surface = self.font.render("Wciśnij [F], aby wpisać zapytanie...", True, WHITE)

        screen.blit(input_text_surface, (input_box.x + 10, input_box.y + 5))
