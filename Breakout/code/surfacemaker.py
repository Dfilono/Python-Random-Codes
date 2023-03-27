import pygame as pg
from settings import *
from os import walk

class SurfaceMaker:
    # import graphics
    # create one surface with graphics for any size
    # return image to block or player

    def __init__(self):
        for idx, info in enumerate(walk('../graphics/blocks')):
            if idx == 0:
                self.assets = {color: {} for color in info[1]}
            
            else:
                for img_name in info[2]:
                    color_type = list(self.assets.keys())[idx - 1]
                    full_path = '../graphics/blocks' + f'/{color_type}/' + img_name
                    surf = pg.image.load(full_path).convert_alpha()
                    self.assets[color_type][img_name.split('.')[0]] = surf

    def get_surf(self, block_type, size):
        image = pg.Surface(size)
        image.set_colorkey((0, 0, 0))
        sides = self.assets[block_type]

        # Corners
        image.blit(sides['topleft'], (0, 0))
        image.blit(sides['topright'], (size[0] - sides['topright'].get_width(), 0))
        image.blit(sides['bottomleft'], (0, size[1] - sides['bottomleft'].get_height()))
        image.blit(sides['bottomright'], (size[0] - sides['bottomright'].get_width(), size[1] - sides['bottomleft'].get_height()))

        # Sides
        # top
        top_w = size[0] - sides['topleft'].get_width() - sides['topright'].get_width()
        scaled_top = pg.transform.scale(sides['top'], (top_w, sides['top'].get_height()))
        image.blit(scaled_top, (sides['topleft'].get_width(), 0))

        # left
        left_h = size[1] - sides['topleft'].get_height() - sides['bottomleft'].get_height()
        scaled_left = pg.transform.scale(sides['left'], (sides['left'].get_width(), left_h))
        image.blit(scaled_left, (0, sides['topleft'].get_height()))

        # right
        right_h = size[1] - sides['topright'].get_height() - sides['bottomright'].get_height()
        scaled_right = pg.transform.scale(sides['right'], (sides['right'].get_width(), right_h))
        image.blit(scaled_right, (size[0] - sides['right'].get_width(), sides['topright'].get_height()))

        # bottom
        bot_w = size[0] - sides['bottomleft'].get_width() - sides['bottomright'].get_width()
        scaled_bot = pg.transform.scale(sides['bottom'], (bot_w, sides['bottom'].get_height()))
        image.blit(scaled_bot, (sides['bottomleft'].get_width(), size[1] - sides['bottom'].get_height()))

        # Center
        center_w = size[0] - sides['left'].get_width() - sides['right'].get_width()
        center_h = size[1] - sides['top'].get_height() - sides['bottom'].get_height()
        scaled_center = pg.transform.scale(sides['center'], (center_w, center_h))
        image.blit(scaled_center, sides['topleft'].get_size())

        return image
