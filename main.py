import os
import sys
import math
import pygame
import requests
from PIL import Image

from io import BytesIO
xp = 0.002
yp = 0.002
vvedenie = pygame.Rect(0, 0, 140, 32)
sbros = pygame.Rect(0, 34, 70, 32)
pt = [1, 1]
pygame.init()
sbros_provershit = False

def poisk(s='Хабаровск'):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={s}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        lower = \
        json_response["response"]['GeoObjectCollection']['featureMember'][-1]['GeoObject']['boundedBy']['Envelope'][
            'lowerCorner']
        upper = \
        json_response["response"]['GeoObjectCollection']['featureMember'][-1]['GeoObject']['boundedBy']['Envelope'][
            'upperCorner']
        return (json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos'].split())
print(poisk())

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
#http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Хабаровск&format=json
#"https://static-maps.yandex.ru/1.x/?ll=37.620070,55.753630&size=450,450&z=10&l=map&pt=37.620070,55.753630,pmwtm2~37.440334%2C55.81775,pmwtm3~37.560812%2C55.791181,pmwtm1"

def get_pic(coords=[0, 0], z=1, l="map", resp='https://static-maps.yandex.ru/1.x/', pt=[1, 1]):
    map_params = {
        "l": chose_map[l],
        "size": "650,450",
        "ll": ",".join(map(str, coords)),
        "z": str(z),
    }
    if pt != [1, 1] and sbros_provershit:
        map_params['pt'] = ",".join(map(str, pt))
    else:
        if 'pt' in map_params.keys():
            del map_params['pt']
    response = requests.get(resp, map_params)
    print(map_params, response)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return pygame.image.load(BytesIO(response.content))

button = load_image("button.png")


z = 1
coords = [0, 0]
vvodimiy_text = []
respo = ''
global chose_map
chose_map = ["map", "sat", "sat,skl"]
ll = 0
pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
pygame.init()
pygame.display.set_caption('Карта')
screen = pygame.display.set_mode((650, 450))
zapret = [13, 9, 8, 1073741912, 27]
font = pygame.font.Font(None, 32)
running = True
vvedenie_chek = False
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
        provershit_visoti = 35
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
                pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
            if vvedenie.collidepoint(event.pos):
                if vvedenie_chek == True:
                    vvedenie_chek = False
                    vvodimiy_text = []
                else:
                    vvedenie_chek = True
            if sbros.collidepoint(event.pos) and sbros_provershit:
                sbros_provershit = False
                pt = [1, 1]
                pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', [1, 1])
        if event.type == pygame.KEYDOWN:
            if vvedenie_chek:
                if not int(event.key) in zapret and not event.unicode == '':
                    vvodimiy_text.append(str(event.unicode))
                #print(vvodimiy_text, event.key)
                if len(vvodimiy_text) and event.key == 8:
                    vvodimiy_text = vvodimiy_text[:-1]
                if event.key == 13:
                    sbros_provershit = True
                    adres = ''.join(vvodimiy_text)
                    print(poisk(adres))
                    coords = [poisk(adres)[0], poisk(adres)[1]]
                    pt = [poisk(adres)[0], poisk(adres)[1]]
                    pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
                    vvedenie_chek = False
                    vvodimiy_text = []
            if event.key == pygame.K_PAGEUP:
                if z <= 16:
                    z += 1
                    pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
            if event.key == pygame.K_PAGEDOWN:
                if z >= 1:
                    z -= 1
                    pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
            if event.key == 1073741904:
                if not float(coords[0]) - provershit_dlini < -170:
                    coords[0] = float(coords[0])
                    coords[0] -= float(provershit_dlini)
                    pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
                else:
                    coords[0] = -170
            if event.key == 1073741906:
                if not float(coords[1]) + provershit_visoti > 70:
                    coords[1] = float(coords[1])
                    coords[1] += float(provershit_visoti)
                    pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
                else:
                    coords[1] = 70
            if event.key == 1073741905:
                if not float(coords[1]) - provershit_visoti < -70:
                    coords[1] = float(coords[1])
                    coords[1] -= float(provershit_visoti)
                    pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
            if event.key == 1073741903:
                if not float(coords[0]) + provershit_dlini > 170:
                    coords[0] = float(coords[0])
                    coords[0] += float(provershit_dlini)
                    pg_pic = get_pic(coords, z, ll, 'https://static-maps.yandex.ru/1.x/', pt)
                else:
                    coords[0] = 170
    vivodimiy_text = font.render(''.join(vvodimiy_text), True, 'black')
    sbros_text = font.render('Сброс', True, 'black')
    screen.blit(pg_pic, (0, 0))
    screen.blit(vivodimiy_text, (3, 4))
    screen.blit(button, (10, 390))

    if len(vvodimiy_text) > 10:
        vvedenie[2] = (140 / 10) * len(vvodimiy_text)
    if vvedenie_chek == False:
        pygame.draw.rect(screen, 'blue', vvedenie, 2)
    else:
        pygame.draw.rect(screen, 'black', vvedenie, 2)
    if sbros_provershit:
        pygame.draw.rect(screen, 'yellow', sbros)
        screen.blit(sbros_text, (0, 34))

    pygame.display.flip()
pygame.quit()
