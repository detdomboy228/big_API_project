import os
import sys
import pygame
import requests

a = float(input())
b = float(input())
z = 17
map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={z}&l=sat"


# 123
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
running = True
mode = 'sat'
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            os.remove(map)
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
    map = bebra(map_request)
    try:
        screen.blit(pygame.image.load(map), (0, 0))
    except Exception:
        pass

    pygame.display.flip()
pygame.quit()
