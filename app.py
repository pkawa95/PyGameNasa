#Piotr Kawa - 78228 - WZ_ININ4_PR1
import pygame
import sys
from image_loader import ImageLoader
from gallery import Gallery
from fullscreen_view import FullscreenView

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FPS = 60
BLACK = (0, 0, 0)

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption("NASA Viewer - Pygame")
        self.clock = pygame.time.Clock()
        self.running = True

        self.loader = ImageLoader()
        self.gallery = Gallery(self.loader.images)
        self.fullscreen_view = None

        self.input_active = False
        self.user_input_text = ""


    def run(self):
        self.loader.fetch_image_urls()
        self.loader.start_loading()

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.fullscreen_view:
                    if event.key == pygame.K_ESCAPE:
                        self.fullscreen_view = None
                    elif event.key == pygame.K_RIGHT:
                        self.fullscreen_view.next_image()
                    elif event.key == pygame.K_LEFT:
                        self.fullscreen_view.previous_image()
                else:
                    if self.input_active:
                        if event.key == pygame.K_RETURN:
                            if self.user_input_text.strip():
                                self.search_new_query(self.user_input_text.strip())
                            self.input_active = False
                            self.user_input_text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_input_text = self.user_input_text[:-1]
                        else:
                            if len(event.unicode) == 1:
                                self.user_input_text += event.unicode
                    else:
                        if event.key == pygame.K_f:
                            self.input_active = True
                            self.user_input_text = ""
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                        elif event.key == pygame.K_RETURN:
                            if self.gallery.images:
                                index = self.gallery.selected_index
                                if index < len(self.gallery.images_on_page()):
                                    self.fullscreen_view = FullscreenView(self.gallery.images,
                                                                          self.gallery.current_page * self.gallery.images_per_page + index)
                        else:
                            self.gallery.handle_input(event.key)

    def search_new_query(self, query):
        self.loader = ImageLoader()
        self.gallery = Gallery(self.loader.images)
        self.loader.fetch_image_urls(query=query)
        self.loader.start_loading()

    def update(self):
        self.gallery.images = self.loader.images

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.fullscreen_view:
            self.fullscreen_view.draw(self.screen)
        else:
            self.gallery.draw(self.screen, loading=self.loader.loading, input_active=self.input_active, user_input_text=self.user_input_text)

        pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
