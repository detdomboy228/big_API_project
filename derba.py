import os
import sys
import pygame
import requests
import pprint
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
        try:
            if self.name_l.text() != '':
                ex.label_6.setText('')
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
        except Exception:
            pass

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
        self.label_6.setText('')
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
    ex.label_6.setText('')
    chislo_govna = ((12756 * 3.14) / ((4 ** z) ** 0.5))
    chislo_govna1 = ((12714 * 3.14) / ((4 ** z) ** 0.5)) / 2
    x, y = pos
    if x < 300:
        raznx = 300 - x
        a -= ((raznx / 300) * chislo_govna) / 95
    else:
        raznx = x - 300
        a += ((raznx / 300) * chislo_govna) / 95
    if y < 225:
        razny = 225 - y
        b += ((razny / 225) * chislo_govna1) / 111
    else:
        razny = y - 225
        b -= ((razny / 225) * chislo_govna1) / 111
    if '{a},{b}' not in pts:
        pts.append(f'{a},{b}')
    ex.run()


def org_find(pos):
    global z, a, b
    ex.label_6.setText('')
    x, y = pos
    chislo_govna = ((12756 * 3.14) / ((4 ** z) ** 0.5))
    chislo_govna1 = ((12714 * 3.14) / ((4 ** z) ** 0.5)) / 2
    if x < 300:
        raznx = 300 - x
        a = a - ((raznx / 300) * chislo_govna) / 95
    else:
        raznx = x - 300
        a = a + ((raznx / 300) * chislo_govna) / 95
    if y < 225:
        razny = 225 - y
        b = b + ((razny / 225) * chislo_govna1) / 111
    else:
        razny = y - 225
        b = b - ((razny / 225) * chislo_govna1) / 111
    adr = find_coords(f'{a}, {b}')[1]
    s = [e for e in adr.split()]
    s = '+'.join(s)
    req = f'https://search-maps.yandex.ru/v1/?text={s}&ll={a},{b}&spn=0.00000045,0.00000045&type=biz&lang=ru_RU&apikey=dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    if x < 300:
        a = a + ((raznx / 300) * chislo_govna) / 95
    else:
        a = a - ((raznx / 300) * chislo_govna) / 95
    if y < 225:
        b = b - ((razny / 225) * chislo_govna1) / 111
    else:
        b = b + ((razny / 225) * chislo_govna1) / 111
    resp = requests.get(req)
    cn = {}
    try:
        res = resp.json()
        for e in res["features"]:
            coord = e['properties']['boundedBy']
            cc1 = ((coord[0][0] + coord[1][0] / 2) ** 2 + ((coord[0][1] + coord[1][1]) / 2) ** 2) ** 0.5
            name = e['properties']['name']
            cn[name] = cc1
        cn = {k: cn[k] for k in sorted(cn, key=cn.get)}
        ex.label_6.setText(list(cn.keys())[-1])
    except Exception:
        ex.label_6.setText('')


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
                if z < 19:
                    z += 1
            if e.key == pygame.K_PAGEDOWN:
                if z > 3:
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
            elif e.button == 3:
                org_find(e.pos)
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
