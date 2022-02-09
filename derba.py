import os
import sys
import pygame
import requests

a = input()
b = input()
z = 17
map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={z}&l=sat"


def bebra(map_r):
    response = requests.get(map_r)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


pygame.init()
map = bebra(map_request)
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map), (0, 0))
pygame.display.flip()
while 3:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            os.remove(map)
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_PAGEUP:
                z += 1
            elif e.key == pygame.K_PAGEDOWN:
                z -= 1
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={z}&l=map"
    map = bebra(map_request)
    try:
        screen.blit(pygame.image.load(map), (0, 0))
    except Exception:
        pass
    pygame.display.flip()
