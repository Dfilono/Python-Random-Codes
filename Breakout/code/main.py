import pygame as pg
import sys
import time
from settings import *
from sprites import Player, Ball, Block
from surfacemaker import SurfaceMaker
from random import choices
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

        # setup
        self.surfacemaker = SurfaceMaker()
        self.player = Player(self.all_sprites, self.surfacemaker)
        self.ball = Ball(self.all_sprites, self.player, self.block_sprites)
        self.stage_setup()

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
                    y = row_idx * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    Block(col, (x, y),[self.all_sprites, self.block_sprites], self.surfacemaker)


    def run(self):
        t = time.time()

        while True:
            dt = time.time() - t
            t = time.time()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.ball.active = True

            # update game
            self.all_sprites.update(dt)

            # draw frame
            self.display_surface.blit(self.bg, (0, 0))
            self.all_sprites.draw(self.display_surface)

            pg.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()