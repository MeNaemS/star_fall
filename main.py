import os
import sys
from random import choice
import pygame as pg

pg.init()
SIZE = WIDTH, HEIGHT = 800, 800
screen = pg.display.set_mode(SIZE)
pg.display.set_caption('Game_stars')
FPS = 60
GRAVITY = 0.25
screen_rect = (0, 0, WIDTH, HEIGHT)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не существует')
        sys.exit()
    image = pg.image.load(fullname)
    if color_key is not None:
        image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image.convert_alpha()
    return image


class Particle(pg.sprite.Sprite):
    stars = [load_image('star.png', color_key=-1)]
    for scale in {5, 10, 20}:
        stars.append(pg.transform.scale(stars[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = choice(self.stars)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY
        if not self.rect.colliderect(screen_rect):
            self.kill()

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


def generate_particles(position):
    particle_count = 20
    velocities = range(-5, 6)
    {Particle(position, choice(velocities), choice(velocities)) for _ in range(particle_count)}


clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            generate_particles(pg.mouse.get_pos())
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pg.display.flip()
    clock.tick(FPS)
pg.quit()
