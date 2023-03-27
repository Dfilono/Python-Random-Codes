import pygame as pg
from settings import *
from random import choice, randint

class Player(pg.sprite.Sprite):
    def __init__(self, groups, surfacemaker):
        super().__init__(groups)

        # setup
        self.display_surface = pg.display.get_surface()
        self.surfacemaker = surfacemaker
        self.image = surfacemaker.get_surf('player', (WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        #self.image.fill('red')

        # position
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))
        self.old_rect = self.rect.copy()
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.vel = 300

        self.lives = 5

        # laser
        self.laser_amount = 0
        self.laser_surf = pg.image.load('../graphics/other/laser.png').convert_alpha()
        self.laser_rects = []

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

    def powerup(self, powerup_type):
        if powerup_type == 'speed':
            self.vel += 50
        
        if powerup_type == 'heart':
            self.lives += 1

        if powerup_type == 'size':
            new_w = self.rect.width * 1.1
            self.image = self.surfacemaker.get_surf('player', (new_w, self.rect.height))
            self.rect = self.image.get_rect(center = self.rect.center)
            self.pos.x = self.rect.x

        if powerup_type == 'laser':
            self.laser_amount += 1

    def display_laser(self):
        self.laser_rects = []
        if self.laser_amount > 0:
            divider_length = self.rect.width / (self.laser_amount + 1)

            for i in range(self.laser_amount):
                x = self.rect.left + divider_length * (i + 1)
                laser_rect = self.laser_surf.get_rect(midbottom = (x, self.rect.top))
                self.laser_rects.append(laser_rect)

            for laser_rect in self.laser_rects:
                self.display_surface.blit(self.laser_surf, laser_rect)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.controls()
        self.pos.x += self.direction.x * self.vel * dt
        self.rect.x = round(self.pos.x)
        self.screen_bounds()
        self.display_laser()

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

        # audio
        self.impact = pg.mixer.Sound('../audio/impact.wav')
        self.impact.set_volume(0.1)

        self.fail = pg.mixer.Sound('../audio/fail.wav')
        self.fail.set_volume(0.1)

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
                        self.impact.play()

                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.impact.play()

                    if getattr(sprite, 'health', None):
                        sprite.get_damage(1)

            if direction == 'vertical':
                for sprite in overlap_sprites:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.pos.y = self.rect.y - 1
                        self.direction.y *= -1
                        self.impact.play()

                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.pos.y = self.rect.y + 1
                        self.direction.y *= -1
                        self.impact.play()

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
                self.player.lives -= 1
                self.fail.play()

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
    def __init__(self, block_type, pos, groups, surfacemaker, create_powerup):
        super().__init__(groups)
        
        self.surfacemaker = surfacemaker
        self.image = self.surfacemaker.get_surf(COLOR_LEGEND[block_type], (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        # damage
        self.health = int(block_type)

        # power ups
        self.create_powerup = create_powerup
        self.prob = 30

    def get_damage(self, amount):
        self.health -= amount

        if self.health > 0:
            self.image = self.surfacemaker.get_surf(COLOR_LEGEND[str(self.health)], (BLOCK_WIDTH, BLOCK_HEIGHT))
        else:
            if randint(1, 100) >= self.prob:
                self.create_powerup(self.rect.center)
            self.kill()

class PowerUp(pg.sprite.Sprite):
    def __init__(self, pos, powerup_type, groups):
        super().__init__(groups)
        self.powerup_type = powerup_type
        self.image = pg.image.load(f'../graphics/upgrades/{powerup_type}.png').convert_alpha()
        self.rect = self.image.get_rect(midtop = pos)

        self.pos = pg.math.Vector2(self.rect.topleft)
        self.vel = 300

    def update(self, dt):
        self.pos.y += self.vel * dt
        self.rect.y = round(self.pos.y)

        if self.rect.top > WINDOW_HEIGHT + 100:
            self.kill()

class Projectile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom = pos)

        self.pos = pg.math. Vector2(self.rect.topleft)
        self.vel = 300

    def update(self, dt):
        self.pos.y -= self.vel * dt
        self.rect.y = round(self.pos.y)

        if self.rect.bottom <= -100:
            self.kill()