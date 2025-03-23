import pygame as pg
import subprocess
import time

pg.init()
pg.font.init()

from src.utils.values import BACKGROUND_IMAGE,HEALTH_FONT,WIDTH,HEIGHT,BLACK,WHITE,MAIN_THEME,CLICK_SOUND


WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Game Menu")


class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.callback = callback

    def draw(self, win):
        pg.draw.rect(win, WHITE, self.rect, border_radius=10)
        text_surf = HEALTH_FONT.render(self.text, True, BLACK)
        win.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                              self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

def start_singleplayer():
    subprocess.Popen(["python", "src/singleplayer.py"])

def start_multiplayer():
    subprocess.Popen(["python","src/multiplayer.py"])

def play_main_theme():
    MAIN_THEME.set_volume(1.0)
    MAIN_THEME.play(-1)


def game_menu():
    run = True
    buttons = [
        Button("Singleplayer", WIDTH // 2.5, HEIGHT // 3, 250, 60, start_singleplayer),
        Button("Multiplayer", WIDTH // 2.5, HEIGHT // 2, 250, 60, start_multiplayer)
    ]

    while run:
        WIN.blit(BACKGROUND_IMAGE,(-450,-250))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                CLICK_SOUND.play()
                time.sleep(1)
                MAIN_THEME.stop()
                for button in buttons:
                    button.check_click(event.pos)

            if event.type==pg.KEYDOWN:
                if event.key==pg.K_BACKSPACE:
                    run=False
                    pg.quit()

        for button in buttons:
            button.draw(WIN)
        
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    play_main_theme()
    game_menu()