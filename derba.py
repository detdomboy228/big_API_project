import os
import sys
import pygame
import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
a = float(input())
b = float(input())
z = 17
pts = []
map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={z}&l=sat"


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('bebrar.ui', self)
        self.setWindowTitle('       ПАНЕЛЬ УПРАВЛЕНИЯ')
        self.btn.clicked.connect(self.run)
        self.btn2.clicked.connect(self.delete)

    def run(self):
        global a, b, pts
        adress = self.name_l.text()
        result = str(find_coords(adress))
        if result != 'None':
            a = float(result.split()[0])
            b = float(result.split()[-1])
            pts.append(f'{a},{b}')

    def delete(self):
        global pts
        del pts[-1]
        self.name_l.setText('')


# 123
def bebra(map_r):
    response = requests.get(map_r)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def find_coords(adr):
    geocoder_request = f"""http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={adr}&format=json"""
    response = requests.get(geocoder_request)
    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates
    except Exception:
        return


pygame.init()
mapp = bebra(map_request)
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(mapp), (0, 0))
pygame.display.flip()
running = True
mode = 'sat'
app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            os.remove(mapp)
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_PAGEUP:
                z += 1
            if e.key == pygame.K_PAGEDOWN:
                z -= 1
            if e.key == pygame.K_RIGHT:
                a += 1 / z ** 2
            if e.key == pygame.K_LEFT:
                a -= 1 / z ** 2
            if e.key == pygame.K_DOWN:
                b -= 1 / (z ** 2 + 10)
            if e.key == pygame.K_UP:
                b += 1 / (z ** 2 + 10)
            if e.key == pygame.K_1:
                mode = 'sat'
            if e.key == pygame.K_2:
                mode = 'map'
            if e.key == pygame.K_3:
                mode = 'sat,skl'
    screen.fill(pygame.Color('white'))
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={z}&l={mode}"
    if pts:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={z}&l={mode}&pt="
    for e in pts:
        if e != pts[-1]:
            map_request += e + '~'
        else:
            map_request += e
    mapp = bebra(map_request)
    try:
        screen.blit(pygame.image.load(mapp), (0, 0))
    except Exception:
        pass
    pygame.display.flip()
pygame.quit()
