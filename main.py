import pygame as pg
import random
from noise import pnoise2
from settings import *

def get_color_surface(color, alpha=255):
    surf = pg.Surface((CELL_SIZE, CELL_SIZE), pg.SRCALPHA)
    surf.fill((*color, alpha))
    return surf.convert_alpha()

class Tile:
    __slots__ = ('type', 'overlay')
    def __init__(self, t_type=TILE_PLAIN, overlay=OVERLAY_NONE):
        self.type = t_type
        self.overlay = overlay

class World:
    def __init__(self, w, h, seed=None):
        self.w, self.h = w, h
        self.seed = seed if seed is not None else random.randint(0, 999999)
        self.tiles = [[Tile(TILE_DEEP_WATER) for _ in range(h)] for _ in range(w)]
        self.full_surf = pg.Surface((w * CELL_SIZE, h * CELL_SIZE))
        self.textures = [
            get_color_surface((10, 20, 80)), get_color_surface((40, 100, 200)),
            get_color_surface((230, 210, 160)), get_color_surface((50, 140, 50)),
            get_color_surface((110, 110, 110)), get_color_surface((240, 240, 240))
        ]
        self.overlays = [None, get_color_surface((20, 70, 20), 160)]
        self.generate()
        self.render_all()
        self.minimap_surf = pg.transform.smoothscale(self.full_surf, (MINIMAP_SIZE, MINIMAP_SIZE))

    def generate(self):
        ox, oy = self.seed % 10000, (self.seed // 1000) % 10000
        for x in range(self.w):
            for y in range(self.h):
                val = pnoise2((x + ox) / NOISE_SCALE, (y + oy) / NOISE_SCALE, octaves=NOISE_OCTAVES)
                if val < THRESHOLD_DEEP_WATER: self.tiles[x][y].type = TILE_DEEP_WATER
                elif val < THRESHOLD_WATER: self.tiles[x][y].type = TILE_WATER
                elif val < THRESHOLD_SAND: self.tiles[x][y].type = TILE_SAND
                elif val < THRESHOLD_PLAIN:
                    self.tiles[x][y].type = TILE_PLAIN
                    if pnoise2((x + ox + 777) / 25.0, (y + oy + 777) / 25.0) > 0.22:
                        self.tiles[x][y].overlay = OVERLAY_FOREST
                elif val < THRESHOLD_MOUNTAIN: self.tiles[x][y].type = TILE_MOUNTAIN
                else: self.tiles[x][y].type = TILE_SNOW

    def render_all(self):
        for y in range(self.h):
            for x in range(self.w):
                t = self.tiles[x][y]
                pos = (x * CELL_SIZE, y * CELL_SIZE)
                self.full_surf.blit(self.textures[t.type], pos)
                if t.overlay: self.full_surf.blit(self.overlays[t.overlay], pos)

    def draw_minimap(self, screen, cam_x, cam_y, zoom):
        mx, my = SCREEN_SIZE - MINIMAP_SIZE - MINIMAP_MARGIN, MINIMAP_MARGIN
        pg.draw.rect(screen, (50, 50, 50), (mx-2, my-2, MINIMAP_SIZE+4, MINIMAP_SIZE+4))
        pg.draw.rect(screen, (200, 200, 200), (mx-2, my-2, MINIMAP_SIZE+4, MINIMAP_SIZE+4), MINIMAP_BORDER)
        screen.blit(self.minimap_surf, (mx, my))
        fw, fh = self.w * CELL_SIZE * zoom, self.h * CELL_SIZE * zoom
        vw, vh = (SCREEN_SIZE / fw) * MINIMAP_SIZE, (SCREEN_SIZE / fh) * MINIMAP_SIZE
        vx, vy = (-cam_x / fw) * MINIMAP_SIZE, (-cam_y / fh) * MINIMAP_SIZE
        pg.draw.rect(screen, (255, 255, 255), (mx + vx, my + vy, vw, vh), 1)

    def draw_selector(self, screen, cam_x, cam_y, zoom):
        mx, my = pg.mouse.get_pos()
        tx, ty = int((mx - cam_x) / (CELL_SIZE * zoom)), int((my - cam_y) / (CELL_SIZE * zoom))
        if 0 <= tx < self.w and 0 <= ty < self.h:
            pg.draw.rect(screen, SELECT_COLOR, (tx * CELL_SIZE * zoom + cam_x, ty * CELL_SIZE * zoom + cam_y, CELL_SIZE * zoom, CELL_SIZE * zoom), 2)
            return tx, ty
        return None

    def update_view(self, zoom):
        return pg.transform.smoothscale(self.full_surf, (int(self.w * CELL_SIZE * zoom), int(self.h * CELL_SIZE * zoom)))

def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pg.time.Clock()
    world = World(W_TILES, H_TILES)
    zoom, cam_x, cam_y, dragging = MIN_ZOOM, 0, 0, False
    view_surf = world.update_view(zoom)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: pg.quit(); return
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3: dragging = True
                elif event.button in (4, 5):
                    mx, my = pg.mouse.get_pos()
                    wx, wy = (mx - cam_x) / zoom, (my - cam_y) / zoom
                    old_zoom = zoom
                    if event.button == 4: zoom = min(MAX_ZOOM, zoom + ZOOM_STEP)
                    else: zoom = max(MIN_ZOOM, zoom - ZOOM_STEP)
                    if old_zoom != zoom:
                        view_surf = world.update_view(zoom)
                        cam_x, cam_y = mx - wx * zoom, my - wy * zoom
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 3: dragging = False
            elif event.type == pg.MOUSEMOTION and dragging:
                cam_x += event.rel[0]; cam_y += event.rel[1]

        vw, vh = view_surf.get_size()
        if vw > SCREEN_SIZE: cam_x = min(0, max(cam_x, SCREEN_SIZE - vw))
        else: cam_x = (SCREEN_SIZE - vw) // 2
        if vh > SCREEN_SIZE: cam_y = min(0, max(cam_y, SCREEN_SIZE - vh))
        else: cam_y = (SCREEN_SIZE - vh) // 2

        screen.fill((10, 10, 15))
        screen.blit(view_surf, (cam_x, cam_y))
        world.draw_selector(screen, cam_x, cam_y, zoom)
        world.draw_minimap(screen, cam_x, cam_y, zoom)
        pg.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
