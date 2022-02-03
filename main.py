import os
import sys
import math
import pygame
import requests
from PIL import Image
from io import BytesIO


def get_pic(coords=[0, 0], z=1):
    map_params = {
        "l": "map",
        "size": "650,450",
        "ll": ",".join(map(str, coords)),
        "z": str(z)
    }
    response = requests.get('https://static-maps.yandex.ru/1.x/', map_params)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return pygame.image.load(BytesIO(response.content))


z = 1
coords = [0, 0]
pg_pic = get_pic(coords, z)

pygame.init()
pygame.display.set_caption('Карта')
screen = pygame.display.set_mode((650, 450))
running = True

pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if z <= 16:
                    z += 1
                    pg_pic = get_pic(coords, z)
            if event.key == pygame.K_PAGEDOWN:
                if z >= 1:
                    z -= 1
                    pg_pic = get_pic(coords, z)
    screen.blit(pg_pic, (0, 0))
    pygame.display.flip()
pygame.quit()
