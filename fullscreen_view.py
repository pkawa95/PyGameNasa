import pygame
import json

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

class FullscreenView:
    def __init__(self, images, selected_index):
        self.images = images
        self.selected_index = selected_index
        self.font = pygame.font.SysFont("Courier", 24)

    def draw(self, screen):
        screen.fill(BLACK)

        image_data = self.images[self.selected_index]

        # Wyświetlenie obrazu po lewej
        original = image_data.surface
        image_rect = original.get_rect()
        max_width = SCREEN_WIDTH // 2 - 50
        max_height = SCREEN_HEIGHT - 150

        scale = min(max_width / image_rect.width, max_height / image_rect.height)
        new_size = (int(image_rect.width * scale), int(image_rect.height * scale))
        image = pygame.transform.scale(original, new_size)

        x = 50
        y = (SCREEN_HEIGHT - new_size[1]) // 2
        screen.blit(image, (x, y))

        # Przygotowanie bardziej szczegółowego JSON-a
        # UWAGA: W image_data potrzebne będą dodatkowe pola!
        json_info = {
            "title": image_data.title,
            "description": getattr(image_data, "description", "Brak opisu"),
            "date_created": getattr(image_data, "date_created", "Brak daty")
        }
        json_text = json.dumps(json_info, indent=4, ensure_ascii=False)

        lines = json_text.split("\n")
        start_x = SCREEN_WIDTH // 2 + 50
        start_y = 100
        for line in lines:
            line_surface = self.font.render(line, True, BLUE)
            screen.blit(line_surface, (start_x, start_y))
            start_y += 30

        # Wyświetlenie legendy na dole
        legend_text = "ESC - wyjście    ←/→ - zmiana zdjęcia"
        legend_surface = self.font.render(legend_text, True, WHITE)
        legend_rect = legend_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(legend_surface, legend_rect)

    def next_image(self):
        self.selected_index = (self.selected_index + 1) % len(self.images)

    def previous_image(self):
        self.selected_index = (self.selected_index - 1) % len(self.images)
