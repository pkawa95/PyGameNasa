#Piotr Kawa - 78228 - WZ_ININ4_PR1
import requests
import threading
import pygame
from io import BytesIO
import time

# Rozmiar miniatur
THUMBNAIL_SIZE = (200, 200)

class ImageData:
    def __init__(self, surface, title, description="", date_created=""):
        self.surface = surface
        self.title = title
        self.description = description
        self.date_created = date_created

class ImageLoader:
    def __init__(self):
        self.images = []
        self.queue = []
        self.loading = False

    def fetch_image_urls(self, query="moon"):
        url = "https://images-api.nasa.gov/search"
        params = {
            "q": query,
            "media_type": "image"
        }
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            items = data.get("collection", {}).get("items", [])
            for item in items:
                link = item.get("links", [{}])[0].get("href", None)
                data_block = item.get("data", [{}])[0]
                title = data_block.get("title", "Brak tytułu")
                description = data_block.get("description", "Brak opisu")
                date_created = data_block.get("date_created", "Brak daty")
                if link:
                    self.queue.append((link, title, description, date_created))
        except Exception as e:
            print(f"Błąd pobierania URL-i: {e}")

    def start_loading(self):
        self.loading = True
        threading.Thread(target=self._load_images_thread, daemon=True).start()

    def _load_images_thread(self):
        while self.queue:
            url, title, description, date_created = self.queue.pop(0)
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                image = pygame.image.load(BytesIO(response.content))
                thumbnail = pygame.transform.scale(image, THUMBNAIL_SIZE)
                self.images.append(ImageData(thumbnail, title, description, date_created))
            except Exception as e:
                print(f"Błąd pobierania obrazu: {e}")
            time.sleep(0.1)
        self.loading = False
