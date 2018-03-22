import pygame, sys
from pygame.locals import *
from random import randint, choice

FPS = 15
WHYT = (242, 242, 242)


class MovingThings:
    spid = 40  # it has nothing to do with speed


class Cake(MovingThings):
    def __init__(self):
        self.x = randint(0, 19) * self.spid
        self.y = randint(0, 14) * self.spid

    def draw(self, surf, img):
        surf.blit(img, (self.x, self.y))


class Playa(MovingThings):
    def __init__(self):
        self.dire = choice(['rite', 'left', 'down', 'up'])  # more random for!.. i dunno, some random god
        starx = randint(4, 16) * self.spid
        stary = randint(4, 11) * self.spid
        if self.dire == 'rite':
            self.curds = [{'x': starx, 'y': stary},
                          {'x': starx - 1 * self.spid, 'y': stary},
                          {'x': starx - 2 * self.spid, 'y': stary}]
        if self.dire == 'left':
            self.curds = [{'x': starx, 'y': stary},
                          {'x': starx + 1 * self.spid, 'y': stary},
                          {'x': starx + 2 * self.spid, 'y': stary}]
        if self.dire == 'up':
            self.curds = [{'x': starx, 'y': stary},
                          {'x': starx, 'y': stary + 1 * self.spid},
                          {'x': starx, 'y': stary + 2 * self.spid}]
        if self.dire == 'down':
            self.curds = [{'x': starx, 'y': stary},
                          {'x': starx, 'y': stary - 1 * self.spid},
                          {'x': starx, 'y': stary - 2 * self.spid}]

        self.dire_tail = self.dire

    def sliding(self):  # it's not really sliding, it gets destroyed and recreated for new position! LIFE IS PAIN
        newhead = 0
        if self.dire == 'rite':
            newhead = {'x': self.curds[0]['x'] + 1 * self.spid, 'y': self.curds[0]['y']}
        elif self.dire == 'left':
            newhead = {'x': self.curds[0]['x'] - 1 * self.spid, 'y': self.curds[0]['y']}
        elif self.dire == 'down':
            newhead = {'x': self.curds[0]['x'], 'y': self.curds[0]['y'] + 1 * self.spid}
        elif self.dire == 'up':
            newhead = {'x': self.curds[0]['x'], 'y': self.curds[0]['y'] - 1 * self.spid}
        assert newhead != 0, 'Lost my head!'
        self.curds.insert(0, newhead)

    def move_rite(self):
        self.dire = 'rite'

    def move_left(self):
        self.dire = 'left'

    def move_down(self):
        self.dire = 'down'

    def move_up(self):
        self.dire = 'up'

    def draw(self, surf, body, head, tail):
        for i in range(1,len(self.curds)-1):
            surf.blit(body, (self.curds[i]['x'], self.curds[i]['y']))
        if self.dire == 'up':
            surf.blit(head, (self.curds[0]['x'], self.curds[0]['y']))
        elif self.dire == 'down':
            surf.blit(pygame.transform.flip(head, False, True), (self.curds[0]['x'], self.curds[0]['y']))
        elif self.dire == 'rite':
            surf.blit(pygame.transform.rotate(head, -90), (self.curds[0]['x'], self.curds[0]['y']))
        elif self.dire == 'left':
            surf.blit(pygame.transform.rotate(head, 90), (self.curds[0]['x'], self.curds[0]['y']))
        if self.curds[-1]['x'] == self.curds[-2]['x']:
            if self.curds[-1]['y'] > self.curds[-2]['y']:
                self.dire_tail = 'up'
            else:
                self.dire_tail = 'down'
        else:
            if self.curds[-1]['x'] > self.curds[-2]['x']:
                self.dire_tail = 'left'
            else:
                self.dire_tail = 'rite'
        if self.dire_tail == 'up':
            surf.blit(tail, (self.curds[-1]['x'], self.curds[-1]['y']))
        elif self.dire_tail == 'down':
            surf.blit(pygame.transform.flip(tail, False, True), (self.curds[-1]['x'], self.curds[-1]['y']))
        elif self.dire_tail == 'rite':
            surf.blit(pygame.transform.rotate(tail, -90), (self.curds[-1]['x'], self.curds[-1]['y']))
        elif self.dire_tail == 'left':
            surf.blit(pygame.transform.rotate(tail, 90), (self.curds[-1]['x'], self.curds[-1]['y']))


    def body_parts(self):
        for i in range(1, len(self.curds)):
            yield self.curds[i]


class Logic:
    def __init__(self):
        self.playa = Playa()


class App:
    winWid = 800
    winHey = 600

    def __init__(self):
        self._running = False
        self._motherfucking_surf = None
        self._basic_font = None
        self._big_font = None
        self._biger_font = None
        self._snak_surf = None
        self._snak_head_surf = None
        self._snak_tail_surf = None
        self._cake_surf = None
        self.logic = Logic()
        self.playa = Playa()
        self.cake = Cake()
        self.state = 'no'
        self.gg = False
        self.skr = 0

    def on_init(self):
        pygame.init()
        self._motherfucking_surf = pygame.display.set_mode((self.winWid, self.winHey), pygame.HWSURFACE)
        pygame.display.set_caption("Snake 'n' Cake")
        self._basic_font = pygame.font.Font('terminal.ttf', 18)
        self._big_font = pygame.font.Font('terminal.ttf', 42)
        self._biger_font = pygame.font.Font('terminal.ttf', 65)
        self._running = True
        self._snak_surf = pygame.image.load('snak.png').convert()
        self._snak_head_surf = pygame.image.load('snak_head.png').convert()
        self._snak_tail_surf = pygame.image.load('snak_tail.png').convert()
        self._cake_surf = pygame.image.load('cake.png').convert()
        self.state = 'start'

    def show_score(self, surf, font):
        skr_surf = font.render('Skr: %s' % self.skr, True, WHYT)
        skr_rect = skr_surf.get_rect()
        skr_rect.topleft = (self.winWid - 110, 10)
        surf.blit(skr_surf, skr_rect)

    def show_star_scr(self, surf, title_font, other_font):
        titleSurf = title_font.render("SNAKE 'N' CAKE", True, WHYT)
        insertSurf = other_font.render("INSERT COIN TO PLAY", True, WHYT)
        exitSurf = other_font.render("OR PLUCK THE CORD TO EXIT", True, WHYT)
        titleRect = titleSurf.get_rect()
        insertRect = insertSurf.get_rect()
        exitRect = exitSurf.get_rect()
        titleRect.midtop = (self.winWid / 2, self.winHey * 0.21)
        insertRect.midtop = (self.winWid / 2, self.winHey * 0.21 + titleRect.height + 42)
        exitRect.midtop = (self.winWid / 2, self.winHey * 0.21 + titleRect.height + 42 + insertRect.height + 21)
        surf.blit(titleSurf, titleRect)
        surf.blit(insertSurf, insertRect)
        surf.blit(exitSurf, exitRect)

    def show_gg_scr(self, surf, other_font):
        ggSurf = other_font.render('GG NOOB', True, WHYT)
        skrSurf = other_font.render('ur skr is %s' % self.skr, True, WHYT)
        ggRect = ggSurf.get_rect()
        skrRect = skrSurf.get_rect()
        ggRect.midtop = (self.winWid / 2, self.winHey * 0.32 + 21)
        skrRect.midtop = (self.winWid / 2, self.winHey * 0.32 - ggRect.height - 21)
        surf.blit(ggSurf, ggRect)
        surf.blit(skrSurf, skrRect)

    def on_event(self, events):
        for event in events:
            if event.type == QUIT:
                self._running = False

            if self.state in ('start', 'gg'):
                pygame.event.clear()
                if event.type == KEYDOWN:
                    if event.key is K_ESCAPE:
                        if self.state != 'start':
                            self.state = 'start'
                        else:
                            self._running = False
                    else:
                        self.state = 'game'

            else:
                if event.type == KEYDOWN:
                    if event.key in (K_RIGHT, K_d) and self.playa.dire != 'left':
                        self.playa.move_rite()

                    if event.key in (K_LEFT, K_a) and self.playa.dire != 'rite':
                        self.playa.move_left()

                    if event.key in (K_DOWN, K_s) and self.playa.dire != 'up':
                        self.playa.move_down()

                    if event.key in (K_UP, K_w) and self.playa.dire != 'down':
                        self.playa.move_up()

                    if event.key is K_ESCAPE:
                        self.state = 'start'

    def on_loop(self):
        if self.state == 'game':
            if self.gg is True:
                self.skr = 0
                self.gg = False
            self.playa.sliding()

            if self.playa.curds[0]['x'] == self.cake.x and self.playa.curds[0]['y'] == self.cake.y:
                self.cake = Cake()
                self.skr += 1
            else:
                del self.playa.curds[-1]

            if self.playa.curds[0]['x'] == -1 * self.playa.spid or \
                    self.playa.curds[0]['x'] == 20 * self.playa.spid or \
                    self.playa.curds[0]['y'] == -1 * self.playa.spid or \
                    self.playa.curds[0]['y'] == 15 * self.playa.spid or \
                    self.playa.curds[0] in self.playa.body_parts():
                self.gg = True
                self.state = 'gg'
                self.playa = Playa()
                self.cake = Cake()

    def on_render(self):
        self._motherfucking_surf.fill((0, 0, 0))

        if self.state == 'start':
            self.show_star_scr(self._motherfucking_surf, self._biger_font, self._basic_font)

        elif self.state == 'game':
            self.playa.draw(self._motherfucking_surf, self._snak_surf, self._snak_head_surf, self._snak_tail_surf)
            self.cake.draw(self._motherfucking_surf, self._cake_surf)
            self.show_score(self._motherfucking_surf, self._basic_font)

        elif self.state == 'gg':
            self.show_gg_scr(self._motherfucking_surf, self._biger_font)
            pygame.time.wait(420)
        pygame.display.flip()
        if self.state == 'gg':
            pygame.time.wait(420)

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() is False:  # it's supposed to check if on_init works. i hope it does what it's supposed to do
            self._running = False

        while self._running:
            self.on_event(pygame.event.get())
            self.on_loop()
            self.on_render()
            pygame.time.Clock().tick(FPS)
        self.on_cleanup()


if __name__ == '__main__':
    App().on_execute()
