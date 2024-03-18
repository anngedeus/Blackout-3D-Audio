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
#player state
player_jump = False
jump_height = 20
player_slide = False
slide_height = -20
player_lane = 0
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

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 155), (WIDTH /2, 150), 50)

    screen.blit(player_img, (player_x, player_y)) 
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()