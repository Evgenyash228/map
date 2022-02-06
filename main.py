import os
import sys
import math
import pygame
import requests
from PIL import Image

from io import BytesIO
xp = 0.002
yp = 0.002

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def get_pic(coords=[0, 0], z=1, l="map"):
    map_params = {
        "l": chose_map[l],
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

button = load_image("button.png")

z = 1
coords = [0, 0]
global chose_map
chose_map = ["map", "sat", "sat,skl"]
ll = 0
pg_pic = get_pic(coords, z, ll)

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (x > 10 and x < 110) and (y > 390 and x < 440):
                if ll < 2:
                    ll += 1
                else:
                    ll = 0
                pg_pic = get_pic(coords, z, ll)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_PAGEUP:
                if z <= 16:
                    z += 1
                    pg_pic = get_pic(coords, z, ll)
            if event.key == pygame.K_PAGEDOWN:
                if z >= 1:
                    z -= 1
                    pg_pic = get_pic(coords, z, ll)

            if event.type == pygame.KEYDOWN:
                if event.key == 1073741904:
                    if not int(coords[0]) - provershit_dlini < -170:
                        coords[0] -= provershit_dlini
                        pg_pic = get_pic(coords, z, ll)
                    else:
                        coords[0] = -170

                if event.key == 1073741906:
                    if not int(coords[1]) + provershit_visoti > 70:
                        coords[1] += provershit_visoti
                        pg_pic = get_pic(coords, z, ll)
                    else:
                        coords[1] = 70

                if event.key == 1073741905:
                    if not int(coords[1]) - provershit_visoti < -70:
                        coords[1] -= provershit_visoti
                        pg_pic = get_pic(coords, z, ll)

                if event.key == 1073741903:
                    if not int(coords[0]) + provershit_dlini > 170:
                        coords[0] += provershit_dlini
                        pg_pic = get_pic(coords, z, ll)
                    else:
                        coords[0] = 170

    screen.blit(pg_pic, (0, 0))
    screen.blit(button, (10, 390))
    pygame.display.flip()
pygame.quit()
