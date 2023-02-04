from os import path, listdir

import pygame as pg

WIDTH = 1200
HEIGHT = 800
FPS = 60
time = [0, 0, 0, 0]
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('CITADEL')
clock = pg.time.Clock()
move = list()
game_foler = path.dirname(__file__)
img_folder = path.join(game_foler, 'images')
curcles_list = sorted(listdir(path.join(img_folder, 'curcles')), key=lambda x: len(x))
time_img = pg.image.load(r'images\time.png')
time_img.set_colorkey((254, 255, 255))
moves_img = pg.image.load(r'images\moves.png')
moves_img.set_colorkey((254, 255, 255))


class Curcle(pg.sprite.Sprite):
    def __init__(self, x, y, digit, img):
        pg.sprite.Sprite.__init__(self)
        self.number = digit
        self.image = pg.image.load(fr'images\curcles\\{img}')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.need_x = 0
        self.need_y = 0

    def move(self, x, y, need_x=None, need_y=None):
        self.rect.center = (x, y)
        if need_y is not None and \
                need_x is not None:
            self.need_x = need_x
            self.need_y = need_y

    def chek_fall(self):
        now_x, now_y = self.rect.center
        if (now_x, now_y) != (self.need_x, self.need_y):
            self.rect.center = (now_x, now_y + 10)
            return True
        return False


class Tower_button:
    def __init__(self, width, height, sprites, x):
        self.width = width
        self.height = height
        self.sprites = pg.sprite.Group()
        self.list_sprites = list()
        self.digits_list = list()
        self.img = pg.image.load(r'images\tower.png')
        self.img.set_colorkey((254, 255, 255))
        self.x = x
        for sprite in sprites:
            self.sprites.add(sprite)
            self.list_sprites.append(sprite)
            self.digits_list.append(sprite.number)

    def draw(self, x, y):
        global FPS_counter, last, move, count_moves
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        screen.blit(self.img, (x, y))
        if move[0] == True and move[-1] == True:
            move[-1] = move[1].chek_fall()
            move[0] = move[-1]
        if x < mouse[0] < x + self.width and \
                y < mouse[1] < y + self.height and \
                FPS_counter % 15 == 1:
            if click[0] == 1:
                if move[0] == False and \
                        len(self.list_sprites) > 0:
                    to_move = self.list_sprites[-1]
                    move[0], move[1] = True, to_move
                    to_move.move(to_move.rect.x + 50, 400)
                    last = len(self.list_sprites), self
                elif move[0] == True:
                    if len(self.list_sprites) > 0 and \
                            self.list_sprites[-1].number < move[1].number:
                        move[0] = False
                        move[-1] = False
                        move[1].move(last[-1].x, 780 - (last[0] * 20))
                        move[1].move(last[-1].x, 780 - (last[0] * 20))
                    else:
                        last[-1].list_sprites.pop()
                        last[-1].digits_list.pop()
                        move[1].kill()
                        self.list_sprites.append(move[1])
                        self.sprites.add(move[1])
                        self.digits_list.append(move[1].number)
                        if len(self.list_sprites) != 0:
                            move[1].move(self.x, 400, self.x, 780 - (len(self.list_sprites) * 20))
                        else:
                            move[1].move(self.x, 400, self.x, 780)
                        move[-1] = True
                        count_moves += 1

        self.sprites.draw(screen)


class Exit_button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.img = pg.image.load(r'images\home.png')
        self.img.set_colorkey((254, 255, 255))

    def draw(self, x, y):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and \
                y < mouse[1] < y + self.height:
            screen.blit(self.img, (x, y))
            if click[0] == 1:
                return False
            else:
                return True
        else:
            screen.blit(self.img, (x, y))
            return True


class Retry_button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.img = pg.image.load(r'images\restatr.png')
        self.img.set_colorkey((255, 255, 255))
        self.last_retry = False

    def draw(self, x, y):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and \
                y < mouse[1] < y + self.height:
            screen.blit(self.img, (x, y))
            if click[0] == 1 and \
                    self.last_retry == False:
                self.last_retry = True
                return True
            else:
                self.last_retry = False
                return False
        else:
            screen.blit(self.img, (x, y))
            self.last_retry = False
            return False


exit_button = Exit_button(40, 40)
retry_button = Retry_button(40, 40)


def create_level(digit):
    global move, time, count_moves
    time = [0, 0, 0, 0]
    count_moves = 0
    move = [False, '', False]
    sprites = [], [], []
    now_x = 300
    now_y = 780
    for i in range(digit, 0, -1):
        Curcle_1 = Curcle(now_x, now_y, i, curcles_list[i - 1])
        now_y -= 20
        sprites[0].append(Curcle_1)
    towers = [Tower_button(200, 500, sprites[0], 300), Tower_button(200, 500, sprites[1], 600),
              Tower_button(200, 500, sprites[-1], 900)]
    to_return = run_level(towers)
    if to_return != None:
        return to_return


def run_level(towers):
    global FPS_counter
    FPS_counter = 0
    running = True
    target = tuple(towers[0].digits_list)
    while running:
        tower_x = 200
        clock.tick(FPS)
        screen.fill((124, 152, 250))
        font_1 = pg.font.SysFont('Times new Roman', 36)
        if towers[-1].digits_list == list(target):
            win_text = font_1.render('YOU WON', True, (0, 0, 0))
            screen.blit(win_text, (500, 400))
            running = exit_button.draw(600, 500)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
        else:
            running = exit_button.draw(1160, 0)
            retry = retry_button.draw(0, 0)
            if retry == True:
                return True
            for tower in towers:
                tower.draw(tower_x, 300)
                tower.sprites.update()
                tower_x += 300
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
            if time[-1] >= 60:
                time[-1] = 0
                time[2] += 1
            if time[1] >= 60:
                time[1] = 0
                time[0] += 1
            if time[2] >= 60:
                time[2] = 0
                time[1] += 1
            time[-1] += 1
            screen.blit(time_img, (246, 5))
            screen.blit(moves_img, (585, -3))
            text_1 = font_1.render(f'{time[0]}:{time[1]}:{time[2]}', True, (0, 0, 0))
            text_2 = font_1.render(f'{count_moves}', True, (0, 0, 0))
            screen.blit(text_1, (375, 0))
            screen.blit(text_2, (600, 0))
        pg.display.flip()
        FPS_counter += 1
