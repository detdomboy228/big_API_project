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
        self.pushButton.clicked.connect(self.on_off_index_potch)
        self.flag_on_off = True
        self.pocht_index = ''

    def run(self):
        global a, b, pts
        adress = self.name_l.text()
        result, adress_doma, pocht_index = str(find_coords(adress)[0]), str(find_coords(adress)[1]), str(find_coords(adress)[2])
        self.pocht_index = pocht_index
        self.label_3.setText(adress_doma.split(', ')[-2])
        self.label_4.setText(adress_doma.split(', ')[-1])
        if result != 'None':
            a = float(result.split()[0])
            b = float(result.split()[-1])
            pts.append(f'{a},{b}')

    def on_off_index_potch(self):
        if self.flag_on_off:
            self.label_5.setText(self.pocht_index)
            self.flag_on_off = False
        else:
            self.label_5.setText('')
            self.flag_on_off = True

    def delete(self):
        global pts
        del pts[-1]
        self.name_l.setText('')
        self.label_3.setText('')
        self.label_4.setText('')
        self.pocht_index = ''


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
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_pocht = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']["postal_code"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates, toponym_address, toponym_pocht
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