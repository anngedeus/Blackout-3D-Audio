# Simple pygame program ----- An example for now --- for testing interface

# Import and initialize the pygame library
import pygame
pygame.init()

#game constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 50
FPS = 60
OBS_SPEED = .1

SCORE = 0
LIVES = 3
#lane 
LEFT = WIDTH * .25
CENTER = WIDTH /2
RIGHT = WIDTH * .75

#load assests
player_img = pygame.image.load('runner.png')
player_img = pygame.transform.scale(player_img, (50, 100))
coin_img = pygame.image.load('coin.png')
coin_img = pygame.transform.scale(coin_img, (50, 50))
sign_img = pygame.image.load('sign.png')
sign_img = pygame.transform.scale(sign_img, (50, 100))
train_img = pygame.image.load('train.jpg')
train_img = pygame.transform.scale(train_img, (70, 70))

#define player variables
player_x = WIDTH // 2
player_y = HEIGHT - GROUND_HEIGHT - player_img.get_height()
player_speed = 5
player_invulnerable_frames = 180
#player state
player_jump = False
jump_height = 10
player_slide = False
slide_height = -10
player_lane = 0

#obstacles
sign1_x = LEFT
sign1_y = -HEIGHT * .5

sign2_x = RIGHT
sign2_y = -HEIGHT * 1.5

coin1_x = CENTER
coin1_y = -HEIGHT * .7
# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("BlackOUT")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #handle player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if player_lane != -1: 
                player_lane -= 1
        if keys[pygame.K_RIGHT]:
            if player_lane != 1: 
                player_lane +=1       
        if keys[pygame.K_UP] and not player_jump:
            player_jump = True
        if keys[pygame.K_DOWN] and not player_slide:
            player_slide = True
        if player_lane == -1: player_x = LEFT
        if player_lane == 0: player_x = CENTER
        if player_lane == 1: player_x = RIGHT      

        if player_jump:
            player_img = pygame.image.load('jump.png')
            player_img = pygame.transform.scale(player_img, (50, 100))
            screen.blit(player_img, (player_x, player_y))
            player_y -= jump_height
            jump_height -=1
            if jump_height ==0:
                player_jump = False
                jump_height = 10
                player_y += 55
        else:
            if player_slide: 
                player_img = pygame.image.load('slide.png')
                player_img = pygame.transform.scale(player_img, (50, 100))
                screen.blit(player_img, (player_x, player_y))
                player_y -= slide_height
                slide_height +=1
                if slide_height ==0:
                    player_slide = False
                    slide_height = -10
                    player_y -= 55
            else:
                player_img = pygame.image.load('runner.png')
                player_img = pygame.transform.scale(player_img, (50, 100))

    #obstacle movements
    sign1_y += OBS_SPEED
    sign2_y += OBS_SPEED
    coin1_y += OBS_SPEED
    #collision detection 
    if player_invulnerable_frames >0: player_invulnerable_frames -=1      
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    sign1_rect = pygame.Rect(sign1_x, sign1_y, sign_img.get_width(), sign_img.get_height())
    coin1_rect = pygame.Rect(coin1_x, coin1_y, coin_img.get_width(), coin_img.get_height())
    if player_rect.colliderect(sign1_rect) and player_invulnerable_frames ==0:
        LIVES -= 1
        player_invulnerable_frames = 2100
    if player_rect.colliderect(coin1_rect) and player_invulnerable_frames ==0:
        SCORE +=1
        player_invulnerable_frames = 1800
    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 155), (WIDTH /2, 150), 50)

    #display assets
    screen.blit(player_img, (player_x, player_y)) 
    screen.blit(sign_img, (sign1_x, sign1_y))
    screen.blit(sign_img, (sign2_x, sign2_y))
    screen.blit(coin_img, (coin1_x, coin1_y))
    #display score/lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {SCORE}", True, (0,0,0))
    lives_text = font.render(f"Lives: {LIVES}", True, (0,0,0))
    screen.blit(score_text, (20,10))
    screen.blit(lives_text, (20, 40))
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()