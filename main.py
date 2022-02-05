import os
import sys
import math
import pygame
import requests
from PIL import Image

from io import BytesIO
xp = 0.002
yp = 0.002

def get_pic(coords=[0, 0], z=1):
    map_params = {
        "l": "map",
        "size": "650,450",
        "ll": ",".join(map(str, coords)),
        "z": str(z)
    }
    response = requests.get('https://static-maps.yandex.ru/1.x/', map_params)
    print(map_params)
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
    if z == 1:
        provershit_visoti = 70
        provershit_dlini = 170
    if z == 2:
        provershit_visoti = 70
        provershit_dlini = 170
    if z == 3:
        provershit_visoti = 61
        provershit_dlini = 112.5
    if z == 4:
        provershit_visoti = 36
        provershit_dlini = 57
    if z == 5:
        provershit_visoti = 19.5
        provershit_dlini = 29
    if z == 6:
        provershit_visoti = 10
        provershit_dlini = 14.5
    if z > 6:
        provershit_visoti = 10
        provershit_dlini = 14.5
        for i in range(z - 6):
            provershit_visoti /= 2
            provershit_dlini /= 2
    #if z == 7
    #print(z)
    for event in pygame.event.get():
        #print(provershit_visoti, provershit_visoti)
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
            if event.type == pygame.KEYDOWN:
                if event.key == 1073741904:
                    if not int(coords[0]) - provershit_dlini < -170:
                        coords[0] -= provershit_dlini
                        pg_pic = get_pic(coords, z)
                    else:
                        coords[0] = -170
                if event.key == 1073741906:
                    if not int(coords[1]) + provershit_visoti > 70:
                        coords[1] += provershit_visoti
                        pg_pic = get_pic(coords, z)
                    else:
                        coords[1] = 70
                if event.key == 1073741905:
                    if not int(coords[1]) - provershit_visoti < -70:
                        coords[1] -= provershit_visoti
                        pg_pic = get_pic(coords, z)
                if event.key == 1073741903:
                    if not int(coords[0]) + provershit_dlini > 170:
                        coords[0] += provershit_dlini
                        pg_pic = get_pic(coords, z)
                    else:
                        coords[0] = 170
    screen.blit(pg_pic, (0, 0))
    pygame.display.flip()
pygame.quit()
