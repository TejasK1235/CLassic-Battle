import pygame as pg
pg.font.init()
pg.mixer.init()
from utils.values import (WIDTH,HEIGHT,SPACESHIP_HEIGHT,SPACESHIP_WIDTH,YELLOW_SPACESHIP_IMAGE,RED_SPACESHIP_IMAGE,
                    BACKGROUND_IMAGE,EXPLOSION_IMAGE,EXPLOSION_SOUND,WHITE,BLACK,RED,YELLOW,HEALTH_FONT,
                    WINNER_FONT,FPS,SPEED,X_OFFSET,Y_OFFSET,BORDER,MAX_BULLETS,BULLET_SPEED,BULLET_HIT_SOUND,
                    BULLET_FIRE_SOUND,MULTIPLAYER_THEME)

WIN=pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Star Battle")

red_bullets=[]
yellow_bullets=[]
RED_IS_HIT=pg.USEREVENT + 1
YELLOW_IS_HIT=pg.USEREVENT + 2


def handle_bullets(red,yellow,red_bullets,yellow_bullets):
    for bullet in red_bullets:
        bullet.x+=BULLET_SPEED
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_IS_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x-=BULLET_SPEED
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_IS_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(BACKGROUND_IMAGE,(-450,-250))
    pg.draw.rect(WIN,BLACK,BORDER)

    red_health_text=HEALTH_FONT.render("HP: "+str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("HP: "+str(yellow_health),1,WHITE)
    WIN.blit(red_health_text,(10,10))
    WIN.blit(yellow_health_text,(WIDTH-red_health_text.get_width()-10,10))

    WIN.blit(YELLOW_SPACESHIP_IMAGE,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE,(red.x,red.y))

    for bullet in red_bullets:
        pg.draw.rect(WIN,RED,bullet)
    
    for bullet in yellow_bullets:
        pg.draw.rect(WIN,YELLOW,bullet)
        
    pg.display.update()


def draw_winner(text,loser):
    WIN.blit(EXPLOSION_IMAGE,(loser.x,loser.y))

    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2, HEIGHT/2-draw_text.get_height()/2))
    pg.display.update()
    EXPLOSION_SOUND.play()

    red_bullets.clear()
    yellow_bullets.clear()
    pg.time.delay(5000)


def handle_red_moves(key_pressed,red):   
        key_pressed=pg.key.get_pressed()
        if key_pressed[pg.K_w] and red.y-SPEED > 0:
            red.y-=SPEED
        if key_pressed[pg.K_a] and red.x > 0:
            red.x-=SPEED
        if key_pressed[pg.K_s] and red.y + SPEED + red.height + Y_OFFSET < HEIGHT:
            red.y+=SPEED
        if key_pressed[pg.K_d] and red.x + SPEED + red.width - X_OFFSET < BORDER.x:
            red.x+=SPEED
            
            
def handle_yellow_moves(key_pressed,yellow):   
        key_pressed=pg.key.get_pressed()
        if key_pressed[pg.K_UP] and yellow.y-SPEED>0:
            yellow.y-=SPEED
        if key_pressed[pg.K_LEFT] and yellow.x - SPEED - X_OFFSET +7 > BORDER.x:
            yellow.x-=SPEED
        if key_pressed[pg.K_DOWN] and yellow.y + SPEED + yellow.height + Y_OFFSET< HEIGHT:
            yellow.y+=SPEED
        if key_pressed[pg.K_RIGHT] and yellow.x + SPEED + yellow.width - X_OFFSET < WIDTH:
            yellow.x+=SPEED

def play_main_theme():
    MULTIPLAYER_THEME.set_volume(1.0)
    MULTIPLAYER_THEME.play(-1)

def main():
    red=pg.Rect((WIDTH-BORDER.x)//2,HEIGHT//2,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pg.Rect(WIDTH-BORDER.x//2,HEIGHT//2,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    red_health=10
    yellow_health=10

    clock=pg.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
                pg.quit()              
            

            if event.type==pg.KEYDOWN:
                if event.key==pg.K_BACKSPACE:
                    run=False
                    pg.quit()

                if event.key==pg.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet=pg.Rect(red.x+red.width,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.set_volume(0.2)
                    BULLET_FIRE_SOUND.play()
                
                if event.key==pg.K_KP0 and len(yellow_bullets) < MAX_BULLETS:
                    bullet=pg.Rect(yellow.x,yellow.y+yellow.height//2-2,10,5) 
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.set_volume(0.2)
                    BULLET_FIRE_SOUND.play()
       
            if event.type== RED_IS_HIT:
                red_health-=1
                BULLET_HIT_SOUND.set_volume(0.2)
                BULLET_HIT_SOUND.play()

            if event.type==YELLOW_IS_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.set_volume(0.2)
                BULLET_HIT_SOUND.play()
            
        winner_text=""
        if red_health <= 0:
            winner_text="Yellow Wins"
            draw_winner(winner_text,red)
            break

        if yellow_health <= 0:
            winner_text="Red Wins"
            draw_winner(winner_text,yellow)
            break

        key_pressed=pg.key.get_pressed()
        handle_red_moves(key_pressed,red)
        handle_yellow_moves(key_pressed,yellow)

        handle_bullets(red,yellow,red_bullets,yellow_bullets)

        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)

    main()

if __name__=="__main__":
    play_main_theme()
    main()