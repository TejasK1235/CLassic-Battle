import os
import pygame as pg


WIDTH,HEIGHT=1200,600
WIN=pg.display.set_mode((WIDTH,HEIGHT))

SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,45

HEALTH_FONT=pg.font.SysFont("comicsans",40)
WINNER_FONT=pg.font.SysFont("comicsans",100)


YELLOW_SPACESHIP_IMAGE=pg.image.load(os.path.join("ASSets","spaceship_yellow.png"))
YELLOW_SPACESHIP_IMAGE=pg.transform.rotate(pg.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

RED_SPACESHIP_IMAGE=pg.image.load(os.path.join("ASSets","spaceship_red.png"))
RED_SPACESHIP_IMAGE=pg.transform.rotate(pg.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)

BACKGROUND_IMAGE=pg.image.load(os.path.join("Assets","background_image.jpg"))
EXPLOSION_IMAGE=pg.image.load(os.path.join("Assets","explosion.png"))
EXPLOSION_IMAGE=pg.transform.scale(EXPLOSION_IMAGE,(SPACESHIP_WIDTH+5,SPACESHIP_HEIGHT+5))

FPS=60
SPEED=5
X_OFFSET=14
Y_OFFSET=10


BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)

BORDER=pg.Rect(WIDTH//2-4,0,8,HEIGHT)

MAX_BULLETS_SINGLEPLAYER=50
MAX_BULLETS=4
BULLET_SPEED=9
red_bullets=[]
yellow_bullets=[]

RED_IS_HIT=pg.USEREVENT + 1
YELLOW_IS_HIT=pg.USEREVENT + 2

BULLET_FIRE_SOUND=pg.mixer.Sound(os.path.join("Assets","Gun+Silencer.mp3"))
BULLET_HIT_SOUND=pg.mixer.Sound(os.path.join("Assets","Grenade+1.mp3"))
EXPLOSION_SOUND=pg.mixer.Sound(os.path.join("Assets","explosion_sound.mp3"))
MULTIPLAYER_THEME=pg.mixer.Sound(os.path.join("Assets","multiplayer_theme.mp3"))
SINGLEPLAYER_THEME=pg.mixer.Sound(os.path.join("Assets","singleplayer_theme.mp3"))
MAIN_THEME=pg.mixer.Sound(os.path.join("Assets","main_menu_theme.mp3"))
CLICK_SOUND=pg.mixer.Sound(os.path.join("Assets","button_click.mp3"))

