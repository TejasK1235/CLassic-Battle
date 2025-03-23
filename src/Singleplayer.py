import pygame as pg
pg.font.init()
pg.mixer.init()
from utils.values import (WIDTH,HEIGHT,SPACESHIP_HEIGHT,SPACESHIP_WIDTH,YELLOW_SPACESHIP_IMAGE,RED_SPACESHIP_IMAGE,
                    BACKGROUND_IMAGE,EXPLOSION_IMAGE,EXPLOSION_SOUND,WHITE,BLACK,RED,YELLOW,HEALTH_FONT,
                    WINNER_FONT,FPS,SPEED,X_OFFSET,Y_OFFSET,BORDER,MAX_BULLETS_SINGLEPLAYER,BULLET_SPEED,BULLET_HIT_SOUND,
                    BULLET_FIRE_SOUND,SINGLEPLAYER_THEME)
import random

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Star Battle")

health_boost = 0
red_bullets = []
bot_bullets = []
explosions = []
RED_IS_HIT = pg.USEREVENT + 1
BOT_IS_HIT = pg.USEREVENT + 2
red_health = 10

NUMBER_OF_BOTS = 5
bots = []

def check_ship_collisions(red, bots):
    for bot in bots[:]:
        if red.colliderect(bot):
            bots.remove(bot)
            return True
    return False

def handle_bullets(red, bots, red_bullets, bot_bullets):
    global health_boost, red_health
    for bullet in red_bullets[:]:
        bullet.x += BULLET_SPEED
        if bullet.x > WIDTH:
            red_bullets.remove(bullet)
            continue

        for bot in bots[:]:
            if bot.colliderect(bullet):
                explosions.append({"pos": (bot.x, bot.y), "timer": pg.time.get_ticks()})
                bots.remove(bot)
                red_bullets.remove(bullet)
                pg.event.post(pg.event.Event(BOT_IS_HIT))
                break
    
    for bullet in bot_bullets[:]:
        bullet.x -= SPEED
        if bullet.x < 0:
            bot_bullets.remove(bullet)
            continue
    
        if red.colliderect(bullet):
            health_boost += 1
            if health_boost == 5:
                red_health += 1
                health_boost = 0
            pg.event.post(pg.event.Event(RED_IS_HIT))
            bot_bullets.remove(bullet)


def fire_bot_bullet(bot):
    if random.random() < 0.01:
        bullet = pg.Rect(bot.x, bot.y + bot.height // 2 - 2, 10, 5)
        bot_bullets.append(bullet)
        BULLET_FIRE_SOUND.set_volume(0.2)
        BULLET_FIRE_SOUND.play()

def draw_window(red, bots, red_bullets, bot_bullets, red_health):
    WIN.blit(BACKGROUND_IMAGE, (-450, -250))
    pg.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("HP: " + str(red_health), 1, WHITE)
    WIN.blit(red_health_text, (10, 10))

    for bot in bots:
        WIN.blit(YELLOW_SPACESHIP_IMAGE, (bot.x, bot.y))

    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullet in red_bullets:
        pg.draw.rect(WIN, RED, bullet)
    
    for bullet in bot_bullets:
        pg.draw.rect(WIN, YELLOW, bullet)

    for explosion in explosions[:]:
        WIN.blit(EXPLOSION_IMAGE, explosion["pos"])
        if pg.time.get_ticks() - explosion["timer"] > 500:
            explosions.remove(explosion)
        
    pg.display.update()


def draw_winner(text, red):
    if text == "You Lose":
        WIN.blit(EXPLOSION_IMAGE, (red.x, red.y))

    if text == "Red Wins":
        for bot in bots:
            WIN.blit(EXPLOSION_IMAGE, (bot.x, bot.y))

    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pg.display.update()
    EXPLOSION_SOUND.play()

    red_bullets.clear()
    bot_bullets.clear()
    pg.time.delay(5000)

def handle_red_moves(key_pressed, red):
    if key_pressed[pg.K_w] and red.y - SPEED > 0:
        red.y -= SPEED
    if key_pressed[pg.K_a] and red.x > 0:
        red.x -= SPEED
    if key_pressed[pg.K_s] and red.y + SPEED + red.height + Y_OFFSET < HEIGHT:
        red.y += SPEED
    if key_pressed[pg.K_d] and red.x + SPEED + red.width - X_OFFSET < BORDER.x:
        red.x += SPEED

def handle_yellow_moves(bots):
    for bot in bots:
        bot.x -= 1

def play_main_theme():
    SINGLEPLAYER_THEME.set_volume(1.0)
    SINGLEPLAYER_THEME.play(-1)

def main():
    global NUMBER_OF_BOTS, red_health
    bots.clear()
    red = pg.Rect((WIDTH - BORDER.x) // 2, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    for i in range(NUMBER_OF_BOTS):
        bot = pg.Rect(WIDTH - BORDER.x // 2 - random.randint(1, 200), HEIGHT - random.randint(50, 500), SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        bots.append(bot)

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    run = False
                    pg.quit()

                if event.key == pg.K_SPACE and len(red_bullets) < MAX_BULLETS_SINGLEPLAYER:
                    bullet = pg.Rect(red.x + red.width, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.set_volume(0.2)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_IS_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.set_volume(0.2)
                BULLET_HIT_SOUND.play()

            if event.type == BOT_IS_HIT:
                BULLET_HIT_SOUND.set_volume(0.2)
                BULLET_HIT_SOUND.play()

        if check_ship_collisions(red, bots):
            draw_winner("You Lose", red)
            break

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins"
            draw_winner(winner_text, red)
            break

        if len(bots) == 0:
            winner_text = "Red Wins"
            draw_winner(winner_text, red)
            break

        key_pressed = pg.key.get_pressed()
        handle_red_moves(key_pressed, red)
        handle_yellow_moves(bots)

        for bot in bots:
            fire_bot_bullet(bot)

        handle_bullets(red, bots, red_bullets, bot_bullets)

        draw_window(red, bots, red_bullets, bot_bullets, red_health)

    NUMBER_OF_BOTS += 1
    main()

if __name__ == "__main__":
    play_main_theme()
    main()
