import pygame, sys
from pygame.locals import *
from random import randint, choice

FPS = 8
WHYT = (242, 242, 242)


class MovingThings:
    spid = 40  # it has nothing to do with speed


class Cake(MovingThings):
    def __init__(self):
        self.curds = {'x': randint(0, 19) * self.spid, 'y': randint(0, 14) * self.spid}

    def draw(self, surf, img):
        surf.blit(img, (self.curds['x'], self.curds['y']))


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

    def draw(self, surf, body, head, tail):
        for i in range(1, len(self.curds) - 1):
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
        self.ending = 'no'

    def on_init(self):
        pygame.init()
        self._motherfucking_surf = pygame.display.set_mode((self.winWid, self.winHey), pygame.HWSURFACE)
        pygame.display.set_caption("Snake 'n' Cake")
        self._basic_font = pygame.font.Font('terminal.ttf', 18)
        self._big_font = pygame.font.Font('terminal.ttf', 42)
        self._biger_font = pygame.font.Font('terminal.ttf', 65)
        self._running = True
        self._snak_surf = pygame.image.load('piccolini\\snak.png')
        self._snak_head_surf = pygame.image.load('piccolini\\snak_head.png')
        self._snak_tail_surf = pygame.image.load('piccolini\\snak_tail.png')
        self._cake_surf = pygame.image.load('piccolini\\cake.png')
        self.state = 'start'

    def show_score(self, surf, font):
        skr_surf = font.render('Skr: %s' % self.skr, True, WHYT)
        skr_rect = skr_surf.get_rect()
        skr_rect.topleft = (self.winWid - 110, 10)
        surf.blit(skr_surf, skr_rect)

    def show_star_scr(self, surf, title_font, other_font):
        title_surf = title_font.render("SNAKE 'N' CAKE", True, WHYT)
        insert_surf = other_font.render("INSERT COIN TO PLAY", True, WHYT)
        exit_surf = other_font.render("OR PLUCK THE CORD TO EXIT", True, WHYT)
        title_rect = title_surf.get_rect()
        insert_rect = insert_surf.get_rect()
        exit_rect = exit_surf.get_rect()
        title_rect.midtop = (self.winWid / 2, self.winHey * 0.21)
        insert_rect.midtop = (self.winWid / 2, self.winHey * 0.21 + title_rect.height + 42)
        exit_rect.midtop = (self.winWid / 2, self.winHey * 0.21 + title_rect.height + 42 + insert_rect.height + 21)
        surf.blit(title_surf, title_rect)
        surf.blit(insert_surf, insert_rect)
        surf.blit(exit_surf, exit_rect)

    def end_game(self):
        self.gg = True
        self.state = 'gg'
        self.playa = Playa()
        self.cake = Cake()

    def show_gg_scr(self, surf, other_font, font, ending_font):
        gg_surf = other_font.render('GG NOOB', True, WHYT)
        skr_surf = other_font.render('ur skr is %s' % self.skr, True, WHYT)
        retart_surf = font.render('INSERT A COIN TO [R]ETARD:', True, WHYT)
        if self.ending == 'broken neck':
            ending_surf = ending_font.render('U BROKE UR NECK', True, WHYT)
        elif self.ending == 'wall breaker':
            ending_surf = ending_font.render('U CANT BREAK WALLS', True, WHYT)
        else:
            ending_surf = ending_font.render('U ATE UR OWN INNERS', True, WHYT)
        gg_rect = gg_surf.get_rect()
        skr_rect = skr_surf.get_rect()
        retart_rect = retart_surf.get_rect()
        ending_rect = ending_surf.get_rect()
        gg_rect.midtop = (self.winWid / 2, self.winHey * 0.32 - 21 - ending_rect.height)
        ending_rect.midtop = (self.winWid / 2, self.winHey * 0.32 + 21)
        skr_rect.midtop = (self.winWid / 2, self.winHey * 0.32 + gg_rect.height)
        retart_rect.midtop = (self.winWid / 2, self.winHey * 0.65)
        surf.blit(gg_surf, gg_rect)
        surf.blit(ending_surf, ending_rect)
        surf.blit(skr_surf, skr_rect)
        surf.blit(retart_surf, retart_rect)

    def on_event(self, events):
        for event in events:
            if event.type == QUIT:
                self._running = False

            if self.state == 'start':
                pygame.event.clear()
                if event.type == KEYDOWN:
                    if event.key is K_ESCAPE:
                        self._running = False
                    else:
                        self.state = 'game'

            elif self.state == 'gg':
                pygame.event.clear()
                if event.type == KEYDOWN:
                    if event.key is K_ESCAPE:
                        self.state = 'start'
                    elif event.key is K_r:
                        self.state = 'game'

            else:
                if event.type == KEYDOWN:  # for some reason it's possible to turn backward if smash buttons fast enough
                    if event.key in (K_RIGHT, K_d) and self.playa.dire != 'left':
                        self.playa.dire = 'rite'

                    if event.key in (K_LEFT, K_a) and self.playa.dire != 'rite':
                        self.playa.dire = 'left'

                    if event.key in (K_DOWN, K_s) and self.playa.dire != 'up':
                        self.playa.dire = 'down'

                    if event.key in (K_UP, K_w) and self.playa.dire != 'down':
                        self.playa.dire = 'up'

                    if event.key is K_ESCAPE:
                        self.state = 'start'

    def on_loop(self):
        if self.state == 'game':
            if self.gg is True:
                self.skr = 0
                self.gg = False
            self.playa.sliding()

            if self.playa.curds[0] == self.cake.curds:
                self.cake = Cake()
                if self.cake.curds == self.playa.curds[0] or self.cake.curds in self.playa.body_parts():
                    self.cake = Cake()  # Cake must not spawn inside of Snak! but it does >_>
                self.skr += 1
            else:
                del self.playa.curds[-1]

            if self.playa.curds[0]['x'] == -1 * self.playa.spid or \
                    self.playa.curds[0]['x'] == 20 * self.playa.spid or \
                    self.playa.curds[0]['y'] == -1 * self.playa.spid or \
                    self.playa.curds[0]['y'] == 15 * self.playa.spid:
                self.ending = 'wall breaker'
                self.end_game()

            if self.playa.curds[0] in self.playa.body_parts():
                if self.playa.curds[0] in (self.playa.curds[1], self.playa.curds[2]):
                    self.ending = 'broken neck'
                else:
                    self.ending = 'self eater'
                self.end_game()

    def on_render(self):
        self._motherfucking_surf.fill((0, 0, 0))

        if self.state == 'start':
            self.show_star_scr(self._motherfucking_surf, self._biger_font, self._basic_font)

        elif self.state == 'game':
            self.playa.draw(self._motherfucking_surf, self._snak_surf, self._snak_head_surf, self._snak_tail_surf)
            self.cake.draw(self._motherfucking_surf, self._cake_surf)
            self.show_score(self._motherfucking_surf, self._basic_font)

        elif self.state == 'gg':
            self.show_gg_scr(self._motherfucking_surf, self._biger_font, self._basic_font, self._big_font)
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
