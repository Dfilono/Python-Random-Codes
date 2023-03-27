import pygame as pg
from settings import *
from random import choice

class Player(pg.sprite.Sprite):
    def __init__(self, groups, surfacemaker):
        super().__init__(groups)

        # setup
        self.suracemaker = surfacemaker
        self.image = surfacemaker.get_surf('player', (WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        #self.image.fill('red')

        # position
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))
        self.old_rect = self.rect.copy()
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.vel = 300

    def controls(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction.x = 1
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def screen_bounds(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.pos.x = self.rect.x
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.controls()
        self.pos.x += self.direction.x * self.vel * dt
        self.rect.x = round(self.pos.x)
        self.screen_bounds()

class Ball(pg.sprite.Sprite):
    def __init__(self, groups, player, blocks):
        super().__init__(groups)

        # collision objs
        self.player = player
        self.blocks = blocks

        # graphics
        self.image = pg.image.load('../graphics/other/ball.png').convert_alpha()

        # position
        self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        self.old_rect = self.rect.copy()
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2((choice((1, -1)), -1))
        self.vel = 400

        # active
        self.active = False

    def collision(self, direction):
        overlap_sprites = pg.sprite.spritecollide(self, self.blocks, False)
        
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)

        if overlap_sprites:
            if direction == 'horizontal':
                for sprite in overlap_sprites:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left - 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1

                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1

                    if getattr(sprite, 'health', None):
                        sprite.get_damage(1)

            if direction == 'vertical':
                for sprite in overlap_sprites:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.pos.y = self.rect.y - 1
                        self.direction.y *= -1

                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.pos.y = self.rect.y + 1
                        self.direction.y *= -1

                    if getattr(sprite, 'health', None):
                        sprite.get_damage(1)

    def window_collision(self, direction):
        if direction == 'horizontal':
            if self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1
            
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1

        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1

            if self.rect.bottom > WINDOW_HEIGHT:
                self.active = False
                self.direction.y = -1

    def update(self, dt):
        if self.active:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.old_rect = self.rect.copy()
            
            self.pos.x += self.direction.x * self.vel * dt
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.window_collision('horizontal')
        
            self.pos.y += self.direction.y * self.vel * dt
            self.rect.y = round(self.pos.y)
            self.collision('vertical')
            self.window_collision('vertical')

        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pg.math.Vector2(self.rect.topleft)

class Block(pg.sprite.Sprite):
    def __init__(self, block_type, pos, groups, surfacemaker):
        super().__init__(groups)
        
        self.surfacemaker = surfacemaker
        self.image = self.surfacemaker.get_surf(COLOR_LEGEND[block_type], (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        # damage
        self.health = int(block_type)

    def get_damage(self, amount):
        self.health -= amount

        if self.health > 0:
            self.image = self.surfacemaker.get_surf(COLOR_LEGEND[str(self.health)], (BLOCK_WIDTH, BLOCK_HEIGHT))
        else:
            self.kill()