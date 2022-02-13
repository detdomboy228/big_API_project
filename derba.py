import os
import sys
import pygame
import requests
import traceback
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
a = 37.620070
b = 55.753630
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
        if self.name_l.text() != '':
            adress = self.name_l.text()
            try:
                result = str(find_coords(adress)[0])
                if (result.split()[0] + ',' + result.split()[1]) in pts:
                    del pts[pts.index((result.split()[0] + ',' + result.split()[1]))]
            except Exception:
                pass
            try:
                adress_doma = str(find_coords(adress)[1])
            except Exception:
                pass
            try:
                pocht_index = str(find_coords(adress)[2])
                self.pocht_index = pocht_index
                if self.flag_on_off:
                    self.label_5.setText(self.pocht_index)
                else:
                    self.label_5.setText('')
            except Exception:
                self.label_5.setText('-')
            try:
                self.label_3.setText(adress_doma)
            except Exception:
                pass
            if result != 'None':
                a = float(result.split()[0])
                b = float(result.split()[-1])
                pts.append(f'{a},{b}')
        else:
            self.label_3.setText(find_coords(f'{a},{b}')[1])
            if self.flag_on_off:
                try:
                    self.label_5.setText(find_coords(f'{a},{b}')[2])
                except Exception:
                    self.label_5.setText('-')

    def on_off_index_potch(self):
        if self.flag_on_off:
            self.flag_on_off = False
            self.label_5.setText('')
        else:
            self.flag_on_off = True
            try:
                self.pocht_index = str(find_coords(f'{a},{b}')[2])
            except Exception:
                pass
            self.label_5.setText(self.pocht_index)

    def delete(self):
        global pts
        del pts[-1]
        self.name_l.setText('')
        self.label_3.setText('')
        self.pocht_index = ''
        self.label_5.setText('')


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
    toponym_coodrinates, toponym_address, toponym_pocht = '', '', '-'
    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        try:
            toponym_pocht = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']["postal_code"]
        except Exception:
            pass
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates, toponym_address, toponym_pocht
    except Exception:
        return


def mouse_click(pos):
    global a, b, z
    chislo_govna = ((12756 * 3.14) / ((4 ** z) ** 0.5))
    chislo_govna1 = ((12714 * 3.14) / ((4 ** z) ** 0.5)) / 2
    x, y = pos
    if x < 300:
        raznx = 300 - x
        if a >= ((raznx / 300) * chislo_govna) / 100:
            a -= ((raznx / 300) * chislo_govna) / 100
        else:
            a -= ((raznx / 300) * chislo_govna) / 100
            a = abs(a)
    else:
        raznx = x - 300
        if (a + ((raznx / 300) * chislo_govna) / 100) <= 180:
            a += ((raznx / 300) * chislo_govna) / 100
        else:
            a += ((raznx / 300) * chislo_govna) / 100
            a = 180 - (a - 180)
    if y < 225:
        razny = 225 - y
        if b >= ((razny / 225) * chislo_govna1) / 111.11111:
            b += ((razny / 225) * chislo_govna1) / 111.11111
        else:
            b += ((razny / 225) * chislo_govna1) / 111.11111
            b = abs(b)
    else:
        razny = y - 225
        if (b - ((razny / 225) * chislo_govna1) / 111.11111) <= 180:
            b -= ((razny / 225) * chislo_govna1) / 111.11111
        else:
            b -= ((razny / 225) * chislo_govna1) / 111.11111
            b = 180 - (b - 180)
    if '{a},{b}' not in pts:
        pts.append(f'{a},{b}')
    ex.run()


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
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                ex.name_l.setText('')
                mouse_click(e.pos)
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
    try:
        screen.blit(mapp, (0, 0))
    except Exception:
        pass
    pygame.display.flip()
pygame.quit()
