# Simple pygame program ----- An example for now --- for testing interface

# Import and initialize the pygame library
import pygame, glob
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import librosa

pygame.init()

#game constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 50
FPS = 60
OBS_SPEED = .1
TRAIN_SPEED = .7

SCORE = 0
LIVES = 3
#lane 
LEFT = WIDTH * .25
CENTER = WIDTH /2
RIGHT = WIDTH * .75

#load assests
player_img = pygame.image.load('assets/runner.png')
player_img = pygame.transform.scale(player_img, (50, 100))
coin_img = pygame.image.load('assets/coin.png')
coin_img = pygame.transform.scale(coin_img, (50, 50))
sign_img = pygame.image.load('assets/sign.png')
sign_img = pygame.transform.scale(sign_img, (50, 100))
train_img = pygame.image.load('assets/train.jpg')
train_img = pygame.transform.scale(train_img, (70, 70))

#load player sounds
footsteps = pygame.mixer.Sound("Audio/footsteps.wav")
jump = pygame.mixer.Sound("Audio/cartoon-jump.wav")
player_hit_sound = pygame.mixer.Sound("Audio/umph.wav")
slide = pygame.mixer.Sound("Audio/sliding.wav")

#load object sounds
#coin_sound = pygame.mixer.Sound("Audio/sparkle.wav")
#train_sound = pygame.mixer.Sound("Audio/train.wav")
#sign_sound = pygame.mixer.Sound("Audio/creakingnoise.wav")

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

train1_x = CENTER
train1_y = -HEIGHT * 3
# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("BlackOUT")

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        footsteps.play()

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
            player_img = pygame.image.load('assets/jump.png')
            footsteps.stop()
            jump.play()
            player_img = pygame.transform.scale(player_img, (50, 100))
            screen.blit(player_img, (player_x, player_y))
            player_y -= jump_height
            jump_height -=2
            if jump_height < -10:
                player_jump = False
                jump.stop()
                footsteps.play()
                player_img = pygame.image.load('assets/runner.png')
                player_img = pygame.transform.scale(player_img, (50, 100))
                jump_height = 10
                #player_y += 55
        else:
            if player_y < HEIGHT - GROUND_HEIGHT - player_img.get_height():
                player_y += jump_height
                jump_height += 2
            if player_slide: 
                player_img = pygame.image.load('assets/slide.png')
                footsteps.stop()
                slide.play()
                player_img = pygame.transform.scale(player_img, (50, 100))
                screen.blit(player_img, (player_x, player_y))
                player_y -= slide_height
                slide_height +=2
                if slide_height > 10:
                    player_slide = False
                    slide.stop()
                    footsteps.play()
                    player_img = pygame.image.load('assets/runner.png')
                    player_img = pygame.transform.scale(player_img, (50, 100))
                    slide_height = -10
            if player_y > HEIGHT - GROUND_HEIGHT + player_img.get_height():
                    player_y += slide_height
                    slide_height -= 2
                    #player_y -= 55
            else:
                player_y = HEIGHT - GROUND_HEIGHT - player_img.get_height()

    #obstacle movements
    sign1_y += OBS_SPEED
    sign2_y += OBS_SPEED
    coin1_y += OBS_SPEED
    train1_y += TRAIN_SPEED
    
    #collision detection 
    if player_invulnerable_frames >0: player_invulnerable_frames -=1      
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    sign1_rect = pygame.Rect(sign1_x, sign1_y, sign_img.get_width(), sign_img.get_height())
    sign2_rect = pygame.Rect(sign2_x, sign2_y, sign_img.get_width(), sign_img.get_height())
    coin1_rect = pygame.Rect(coin1_x, coin1_y, coin_img.get_width(), coin_img.get_height())
    train1_rect = pygame.Rect(train1_x, train1_y, train_img.get_width(), train_img.get_height())
    #SIGNS
    if player_rect.colliderect(sign1_rect) and player_invulnerable_frames ==0 and player_slide == False:
        player_hit_sound.play()
        LIVES -= 1
        player_invulnerable_frames = 2100
    if player_rect.colliderect(sign2_rect) and player_invulnerable_frames ==0 and player_slide == False:
        player_hit_sound.play()
        LIVES -= 1
        player_invulnerable_frames = 2100
    #TRAINS
    if player_rect.colliderect(train1_rect) and player_invulnerable_frames ==0:
        player_hit_sound.play()
        LIVES -= 1
        player_invulnerable_frames = 2100

    #COINSE
    if player_rect.colliderect(coin1_rect) and player_invulnerable_frames ==0 and player_jump == True:
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
    screen.blit(train_img, (train1_x, train1_y))
    #display score/lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {SCORE}", True, (0,0,0))
    lives_text = font.render(f"Lives: {LIVES}", True, (0,0,0))
    screen.blit(score_text, (20,10))
    screen.blit(lives_text, (20, 40))
    # Flip the display
    pygame.display.flip()
    if LIVES == 0: running = False
# Done! Time to quit.
pygame.quit()