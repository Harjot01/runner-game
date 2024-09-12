import pygame
import sys

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = score_font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# Font
score_font = pygame.font.Font('font/Pixeltype.ttf', 64)


# Game Images

# Sky
sky_surface = pygame.image.load('graphics/Sky.png').convert()

# Ground
ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(bottomleft = (0, 467))


# Snail
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright=(600, 300))

# Player
player_surface = pygame.image.load('graphics/Player/player_walk_1.png')
player_rect = player_surface.get_rect(midbottom=(100, 300))
player_gravity = 0


# Game specific variables
game_active = True
start_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(pygame.mouse.get_pos()) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 800
                    start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        
        # Sky
        screen.blit(sky_surface, (0, 0))

        # Ground
        screen.blit(ground_surface, ground_rect)
        ground_rect.left -= 4
        display_score()

        # Snail
        snail_rect.x -= 4
        if snail_rect.x < -72:
            snail_rect.x = 872
        screen.blit(snail_surface, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)
        

        # Collision
        if player_rect.colliderect(snail_rect):
            game_active = False
    else:
        screen.fill('Black')

    pygame.display.update()
    clock.tick(60)
