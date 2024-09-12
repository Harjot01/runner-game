import pygame
import sys
from random import randint

# Adding music
pygame.mixer.init()
bg_sound = pygame.mixer.Sound('audio/music.wav')
bg_sound.play(loops=-1)


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list

    else:
        return []


def collision(player_rect, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player_rect.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 300:

        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# Font
font = pygame.font.Font('font/Pixeltype.ttf', 64)

# Game Images

# Sky
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Snail
snail_index = 0
snail_walk1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_walk2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_walk = [snail_walk1, snail_walk2]
snail_surface = snail_walk[snail_index]

# FLy
fly_index = 0
fly_walk1 = pygame.image.load('graphics/Fly/Fly1.png')
fly_walk2 = pygame.image.load('graphics/Fly/Fly2.png')
fly_walk = [fly_walk1, fly_walk2]
fly_surface = fly_walk[fly_index]

# Player
player_walk1 = pygame.image.load(
    'graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load(
    'graphics/Player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_index = 0
player_walk = [player_walk1, player_walk2]
player_surface = player_walk[player_index]

player_rect = player_surface.get_rect(midbottom=(100, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png')
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_text = font.render('Pixel Runner', False, (111, 196, 169))
game_text_rect = game_text.get_rect(topleft=(280, 50))

play_button = pygame.image.load('graphics/play_button.png').convert_alpha()
play_button = pygame.transform.scale(play_button, (67, 76))
play_button_rect = play_button.get_rect(bottomleft=(370, 375))


# Game specific variables
game_active = False
start_time = 0
score = 0

obstacle_rect_list = []

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(pygame.mouse.get_pos()) and player_rect.bottom >= 300:
                    jump_sound = pygame.mixer.Sound('audio/jump.mp3')
                    jump_sound.play()
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    jump_sound = pygame.mixer.Sound('audio/jump.mp3')
                    jump_sound.play()
                    player_gravity = -20
        else:
            game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_active = True
                    # snail_rect.left = 800
                    start_time = int(pygame.time.get_ticks()/1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(
                        bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(
                        bottomright=(randint(900, 1100), 210)))
            if event.type == snail_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_walk[snail_index]

            if event.type == fly_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_walk[fly_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        # Player animation
        player_animation()
        screen.blit(player_surface, player_rect)

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_gravity = 0
        player_rect.midbottom = (100, 300)

        screen.blit(game_text, game_text_rect)
        screen.blit(play_button, play_button_rect)
    pygame.display.update()
    clock.tick(60)
