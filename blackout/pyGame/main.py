# Simple pygame program ----- An example for now --- for testing interface

# Import and initialize the pygame library
import pygame
pygame.init()

#game constants
WIDTH, HEIGHT = 800, 400
GROUND_HEIGHT = 50
FPS = 60
OBS_SPEED = 3
#lane 
LEFT = -1
CENTER = 0
RIGHT = 1

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("BlackOUT")

#load assests
player_img = pygame.image.load('runner.jpg')
coin_img = pygame.image.load('coin.png')
sign_img = pygame.image.load('sign.png')
train_img = pygame.image.load('train.jpg')

#player variables
#define player variables
player_x = WIDTH // 2
player_y = HEIGHT - GROUND_HEIGHT - player_img.get_height()
player_speed = 5
#player state
player_jump = False
jump_height = 20
player_slide = False
slide_height = -20
#lane state
player_lane = CENTER

sign_x = WIDTH
sign_y = HEIGHT - GROUND_HEIGHT - sign_img.get_height()
sign_speed = OBS_SPEED



# Run until the user asks to quit
running = True
#clock = pygame.time.Clock()

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #handle player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if player_lane != -1: 
                player_lane -= 1
                player_x = WIDTH * .75
        if keys[pygame.K_RIGHT]:
            if player_lane != 1: 
                player_lane +=1
                player_x = WIDTH * .25
        if keys[pygame.K_UP] and not player_jump:
            player_jump = True
        if keys[pygame.K_DOWN] and not player_slide:
            player_slide = True
                
        #player jump and fall
        if player_jump:
            player_y -= jump_height
            jump_height -= 1
            if jump_height < -15:
                player_jump = False
                jump_height = 15
        else:
            if player_y < HEIGHT - GROUND_HEIGHT -player_img.get_height():
                player_y += jump_height
                jump_height += 1
            else:
                player_y = HEIGHT -GROUND_HEIGHT - player_img.get_height()
                jump_height = 15

    #obstacle movements
    sign_y -= OBS_SPEED
    

    #collision check
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    sign_rect = pygame.Rect(sign_x, sign_y, sign_img.get_width(), sign_img.get_height())

    if player_rect.colliderect(sign_rect):
        running = False

    #Draw everything
    screen.fill((255, 255, 255))
#screen.blit(player_img, (player_x, player_y))    
#screen.blit(sign_img, (sign_x, sign_y))
    pygame.draw.circle(screen, (0,0,255), (250,250), 75)
    # Flip the display
    pygame.display.flip()
    

    #clock.tick(FPS)
    # Done! Time to quit.
pygame.quit()