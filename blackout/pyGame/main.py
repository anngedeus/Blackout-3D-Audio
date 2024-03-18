import pygame


#Code credit to Code Nust on YouTube
#initilize engine
pygame.init()

#game constants
WIDTH, HEIGHT = 800, 400
GROUND_HEIGHT = 100
FPS = 60
#lane 
LEFT = -1
CENTER = 0
RIGHT = 1

#colors
WHITE = (255, 255, 255)

#create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlackOut")

#load asset images
player_img = pygame.image.load('runner.jpg')
coin_img = pygame.image.load('coin.png')
sign_img = pygame.image.load('sign.png')
train_img = pygame.image.load('train.jpg')

#define player variables
player_x = WIDTH //2
player_y = HEIGHT - GROUND_HEIGHT - player_img.get_height()
player_speed= 5
#player state
player_jump = False
jump_height = 20
player_slide = False
slide_height = -20
#lane state


