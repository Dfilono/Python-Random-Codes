import pygame as pg
import sys
import time
from settings import *
from sprites import Player, Ball, Block, PowerUp, Projectile
from surfacemaker import SurfaceMaker
from random import choices, choice, randint
from string import digits

class Game:
    def __init__(self):
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Breakout')

        # background
        self.bg = self.create_bg()

        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.block_sprites = pg.sprite.Group()
        self.powerup_sprites = pg.sprite.Group()
        self.projectile_spirtes = pg.sprite.Group()

        # setup
        self.surfacemaker = SurfaceMaker()
        self.player = Player(self.all_sprites, self.surfacemaker)
        self.ball = Ball(self.all_sprites, self.player, self.block_sprites)
        self.stage_setup()

        # lives
        self.lives_surf = pg.image.load('../graphics/other/heart.png').convert_alpha()

        # projectile
        self.projectile_surf = pg.image.load('../graphics/other/projectile.png').convert_alpha()
        self.can_shoot = True
        self.shoot_time = 0

        # crt
        self.crt = CRT()

        # audio
        self.laser_sound = pg.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.1)

        self.powerup_sound = pg.mixer.Sound('../audio/powerup.wav')
        self.powerup_sound.set_volume(0.1)

        self.laserhit = pg.mixer.Sound('../audio/laser_hit.wav')
        self.laserhit.set_volume(0.02)

        self.music = pg.mixer.Sound('../audio/music.wav')
        self.music.set_volume(0.1)
        self.music.play(loops = -1)


    def create_powerup(self, pos):
        powerup_type = choice(POWERUPS)
        PowerUp(pos, powerup_type, [self.all_sprites, self.powerup_sprites])

    def create_bg(self):
        bg_og = pg.image.load('../graphics/other/bg.png').convert()
        scale_factor = WINDOW_HEIGHT / bg_og.get_height()
        scale_bg = pg.transform.scale(bg_og, (bg_og.get_width() * scale_factor, bg_og.get_height() * scale_factor))

        return scale_bg

    def stage_setup(self):
        # randomly generates block map
        new_block_map = []
        final_block_map = []
        for i in range(len(BLOCK_MAP)):
            new_row = ''.join(choices(digits[1:7] + ' ', k = len(BLOCK_MAP[i])))
            new_block_map.append(new_row)

            if len(new_block_map) == len(BLOCK_MAP):
                final_block_map = new_block_map[0:5]

                for j in range(4):
                    final_block_map.append('            ')

        # creates block positions
        for row_idx, row in enumerate(final_block_map):
            for col_idx, col in enumerate(row):
                if col != ' ':
                    x = col_idx * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    y = TOP_OFFSET + row_idx * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    Block(col, (x, y),[self.all_sprites, self.block_sprites], self.surfacemaker, self.create_powerup)

    def display_lives(self):
        for i in range(self.player.lives):
            x = 2 + i * (self.lives_surf.get_width() + 2)
            self.display_surface.blit(self.lives_surf, (x, 4))

    def powerup_collision(self):
        overlap_sprites = pg.sprite.spritecollide(self.player, self.powerup_sprites, True)

        for sprite in overlap_sprites:
            self.player.powerup(sprite.powerup_type)
            self.powerup_sound.play()

    def create_projectile(self):
        self.laser_sound.play()
        for projectile in self.player.laser_rects:
            Projectile(projectile.midtop - pg.math.Vector2(0, 30), self.projectile_surf, [self.all_sprites, self.projectile_spirtes])

    def projectile_timer(self):
        if pg.time.get_ticks() - self.shoot_time >= 500:
            self.can_shoot = True

    def projectile_collisions(self):
        for projectile in self.projectile_spirtes:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.block_sprites, False)

            if overlap_sprites:
                for sprite in overlap_sprites:
                    sprite.get_damage(1)
                projectile.kill()
                self.laserhit.play()
    def run(self):
        t = time.time()

        while True:
            dt = time.time() - t
            t = time.time()

            for event in pg.event.get():
                if event.type == pg.QUIT or self.player.lives <= 0 or len(self.block_sprites) == 0:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.ball.active = True

                        if self.can_shoot:
                            self.create_projectile()
                            self.can_shoot = False
                            self.shoot_time = pg.time.get_ticks()
                    
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

            self.display_surface.blit(self.bg, (0, 0))
            
            # update game
            self.all_sprites.update(dt)
            self.powerup_collision()
            self.projectile_timer()
            self.projectile_collisions()

            # draw frame
            
            self.all_sprites.draw(self.display_surface)
            self.display_lives()

            # crt
            self.crt.draw()

            pg.display.update()

class CRT:
    def __init__(self):
        vig = pg.image.load('../graphics/other/tv.png').convert_alpha()
        self.scaled_vig = pg.transform.scale(vig, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface = pg.display.get_surface()
        self.create_lines()

    def draw(self):
        self.scaled_vig.set_alpha(randint(60, 70))
        self.display_surface.blit(self.scaled_vig, (0, 0))

    def create_lines(self):
        line_height = 4
        line_amount = WINDOW_HEIGHT // line_height

        for line in range(line_amount):
            y = line * line_height
            pg.draw.line(self.scaled_vig, (20, 20, 20), (0, y), (WINDOW_WIDTH, y), 1)

if __name__ == '__main__':
    game = Game()
    game.run()