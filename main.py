from os import path, listdir

import pygame as pg


from game import create_level

WIDTH = 1200
HEIGHT = 800
FPS = 60
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('CITADEL')
clock = pg.time.Clock()
all_buttons = list()
game_foler = path.dirname(__file__)
img_folder = path.join(game_foler, 'images')
active_list = sorted(listdir(path.join(img_folder, 'active')), key=lambda x: len(x))
anactive_list = sorted(listdir(path.join(img_folder, 'anactive')), key=lambda x: len(x))


class Button:
    def __init__(self, width, height, active_img, anactive_img, level_number, number):
        self.width = width
        self.number = number
        self.level = level_number
        self.height = height
        self.active_img = pg.image.load(fr'images\active\\{active_img}')
        self.anactive_img = pg.image.load(fr'images\anactive\\{anactive_img}')
        self.active_img.set_colorkey((255, 255, 255))
        self.anactive_img.set_colorkey((255, 255, 255))

    def draw(self, x, y):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and \
                y < mouse[1] < y + self.height:
            screen.blit(self.active_img, (x, y))
            if click[0] == 1:
                result = create_level(self.level)
                if result == True:
                    while result:
                        result = create_level(self.level)
                if result != None:
                    return result
        else:
            screen.blit(self.anactive_img, (x, y))


for i in range(1, 16):
    button_1 = Button(100, 100, active_list[i - 1], anactive_list[i - 1], i + 2, i)
    all_buttons.append(button_1)

def run_game():
    running = True
    while running:
        now_x = 150
        now_y = 150
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill((124, 152, 250))
        for i in all_buttons:
            if i.number % 5 != 0:
                result = i.draw(now_x, now_y)
                if result == False:
                    running = result
                now_x += 200
            else:
                result = i.draw(now_x, now_y)
                if result == False:
                    running = result
                elif result == True:
                    create_level(i.level)
                now_x = 150
                now_y += 250
        pg.display.flip()


run_game()
