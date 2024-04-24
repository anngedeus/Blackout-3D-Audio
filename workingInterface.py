# Working BLACKOUT interface 

# Import and initialize the pygame library
import pygame, glob, sys, math
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import threading

#Establishes and sets necessary globals 
global tTime, sTime, cTime, sampleRate, collected 
tTime = 0
sTime = 0
cTime = 0
collected = False

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

#Finds the slope between two points, used for azimuth angle calculation 
#Reference: https://www.geeksforgeeks.org/program-find-slope-line/
def slope(x1, y1, x2, y2): 
    if(x2 - x1 != 0): 
      return (float)(y2-y1)/(x2-x1) 
    return sys.maxsize

#Finds azimuth angle between lines with specified slopes
#Reference: https://www.geeksforgeeks.org/angle-between-a-pair-of-lines/
def findAngle(m1, m2, objectX, objectY):
    angle = math.atan2(m2 - m1, 1 + m1 * m2)
    
    angle_degrees = math.degrees(angle)
    
    #Degrees must be highly specified in reference to player's orientation to work with automated HRTF selection 
    if player_x == objectX:
        if player_y < objectY:
            angle_degrees = 0
        else:
            angle_degrees = 180
    elif objectX == CENTER: 
        if player_x == LEFT:
            angle_degrees += 180 
        elif player_x == RIGHT: 
            angle_degrees += 360
    elif objectX == LEFT: 
        angle_degrees += 360
    elif objectX == RIGHT:
        angle_degrees += 180
        
    return angle_degrees

#Loads HRTFs into array 
kemar = './ProofOfConcept/KEMAR/full/elev0/*.wav'
KEMAR = glob.glob(kemar)

#Creates basic audio objects 
train = AudioSegment.from_wav("Audio/TrainTest22050.wav")
sign = AudioSegment.from_wav("Audio/swinging22050.wav")
coin = AudioSegment.from_wav("Audio/shimmer22050.wav")

#Determines the playback chop of the audio, must be specified for different machines 
sampleRate = 150

#Bread and butter of audio processing
def trainAudioProcessing(ty, tTheta):
    global tTime, sampleRate
    
    #Is calculated for each object, determined by object's distance from character's head
    volume = max(0, min(1, (ty + 700) / 1500)) * 2
    
    #Only plays audio if in bounds of user hearing
    if (ty > -1000) & (ty < 1200):
        #Creates chunk of audio file at a specific point in time with sampleRate length
        tHRTF = train[tTime:(tTime + sampleRate)]
        
        #Takes array from streamed audio chunk
        tHRTF = np.array(tHRTF.get_array_of_samples(), dtype=np.float32)
        tHRTF /= np.max(np.abs(tHRTF))
        
        #Determines HRTF choice from azimuth calculation given by theta
        tvalue = int(round((tTheta / 5)))
        
        [tLHRTF, sample] = sf.read(KEMAR[tvalue])
        [tRHRTF, sample] = sf.read(KEMAR[tvalue + 72])
        
        #Convolution step
        tL = np.convolve(tHRTF, tLHRTF)
        tR = np.convolve(tHRTF, tRHRTF)
        
        #Transposition step 
        tBin_Mix = np.vstack([tL,tR]).transpose()
        
        #Scales binaural mix to specs required by pygame to create sound object from numpy array
        tBin_Mix_scaled = (tBin_Mix * 32767 * volume * 0.5).astype(np.int16)
        tBin_Mix_scaled = np.ascontiguousarray(tBin_Mix_scaled)
        
        #Create pygame object out of numpy array
        tsound = pygame.mixer.Sound(tBin_Mix_scaled)
        
        #Play sound
        tsound.play()
        
        tTime += 1
    else: 
        tTime = 0

#Same structure as trainAudioProcessing
def signAudioProcessing(sy, sTheta):
    global sTime, sampleRate
    volume = max(0, min(1, (sy + 700) / 1500))
    
    if (sy > -800) & (sy < 1000): 
        sHRTF = sign[sTime:(sTime + sampleRate)]
        
        sHRTF = np.array(sHRTF.get_array_of_samples(), dtype=np.float32)
        sHRTF /= np.max(np.abs(sHRTF))
        
        svalue = int(round((sTheta / 5)))
        
        [sLHRTF, sample] = sf.read(KEMAR[svalue])
        [sRHRTF, sample] = sf.read(KEMAR[svalue + 72])
        sL = np.convolve(sHRTF, sLHRTF)
        sR = np.convolve(sHRTF, sRHRTF)
        
        sBin_Mix = np.vstack([sL,sR]).transpose()
        sBin_Mix_scaled = (sBin_Mix * 32767 * volume * 0.25).astype(np.int16)
        
        sBin_Mix_scaled = np.ascontiguousarray(sBin_Mix_scaled)
        
        ssound = pygame.mixer.Sound(sBin_Mix_scaled)
        ssound.play()
        
        sTime += 1
    else: 
        sTime = 0

#Same structure as trainAudioProcessing
def coinAudioProcessing(cy, cTheta):
    global cTime, sampleRate, collected
    volume = max(0, min(1, (cy + 700) / 1500))
    
    if (cy > -800) & (cy < 1000):
        cHRTF = coin[cTime:(cTime + sampleRate)]
        
        cHRTF = np.array(cHRTF.get_array_of_samples(), dtype=np.float32)
        cHRTF /= np.max(np.abs(cHRTF))
        
        cvalue = int(round((cTheta / 5)))
        
        [cLHRTF, sample] = sf.read(KEMAR[cvalue])
        [cRHRTF, sample] = sf.read(KEMAR[cvalue + 72])
        cL = np.convolve(cHRTF, cLHRTF)
        cR = np.convolve(cHRTF, cRHRTF)
        
        cBin_Mix = np.vstack([cL,cR]).transpose()
        
        cBin_Mix_scaled = (cBin_Mix * 32767 * volume * 0.25).astype(np.int16)
        cBin_Mix_scaled = np.ascontiguousarray(cBin_Mix_scaled)
        
        csound = pygame.mixer.Sound(cBin_Mix_scaled)
        #Will only play sparkle if coin has not been collected, will continue if missed
        if (not collected):
            csound.play()
        
        cTime += 1
    else:
        collected = False
        cTime = 0

#Establishes all mixers 
pygame.mixer.pre_init(44100)
pygame.mixer.init()
pygame.init()

font = pygame.font.Font(None, 36)

#game constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 50
FPS = 60
OBS_SPEED = .75
TRAIN_SPEED = 1.25

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
dash = pygame.mixer.Sound("Audio/Woosh.wav")
collect = pygame.mixer.Sound("Audio/collect.wav")
tada = pygame.mixer.Sound("Audio/tada.wav")

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

#List of obstacles
train1_x = LEFT
train1_y = -HEIGHT * 3

train2_x = RIGHT
train2_y = -HEIGHT * 6

coin1_x = CENTER
coin1_y = -HEIGHT * 5

train3_x = CENTER
train3_y = -HEIGHT * 12

sign1_x = LEFT
sign1_y = -HEIGHT * 6

sign2_x = RIGHT
sign2_y = -HEIGHT * 9

coin2_x = LEFT
coin2_y = -HEIGHT * 10

train4_x = CENTER
train4_y = -HEIGHT * 16

train5_x = LEFT 
train5_y = -HEIGHT * 20 

train6_x = CENTER 
train6_y = -HEIGHT * 23 

train7_x = RIGHT 
train7_y = -HEIGHT * 26

coin3_x = RIGHT 
coin3_y = -HEIGHT * 15

sign3_x = CENTER
sign3_y = -HEIGHT * 16

coin4_x = RIGHT 
coin4_y = -HEIGHT * 18

sign4_x = CENTER
sign4_y = -HEIGHT * 19

train8_x = LEFT 
train8_y = -HEIGHT * 29

coin5_x = LEFT
coin5_y = -HEIGHT * 20

sign5_x = CENTER
sign5_y = -HEIGHT * 22

sign6_x = LEFT
sign6_y = -HEIGHT * 24

train9_x = LEFT 
train9_y = -HEIGHT * 33

coin6_x = CENTER 
coin6_y = -HEIGHT * 27

train10_x = RIGHT 
train10_y = -HEIGHT * 36

#Defines set of obstacles used for reference by audio processing
t = 0
tMax = 9
trackedTrain_x = train1_x
trackedTrain_y = train1_y

s = 0
sMax = 5
trackedSign_x = sign1_x
trackedSign_y = sign1_y

c = 0
cMax = 5
trackedCoin_x = coin1_x
trackedCoin_y = coin1_y

#Creates separate audio channel for character inputs / movements
userAction_channel = pygame.mixer.Channel(1)
hitAction_channel = pygame.mixer.Channel(2)

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("BlackOUT")

clock = pygame.time.Clock()

#Draws initial image
imp = pygame.image.load("SS.jpg").convert()
imp = pygame.transform.scale(imp, (WIDTH, HEIGHT))
screen.blit(imp, (0, 0))
pygame.display.flip()

#Queue up audio and visuals before running begins 
pygame.mixer.music.load("Audio/GravelSounds.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
        clock.tick(30)
pygame.mixer.music.load("Audio/whistle.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
        clock.tick(30)
pygame.mixer.music.load("Audio/dog.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
        clock.tick(30)
pygame.mixer.music.load("Audio/GravelRunning.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
        clock.tick(30)

running = True

#Play royalty-free music (a must)
pygame.mixer.music.load("Audio/ROCK-IT_AdobeStock.wav")
pygame.mixer.music.play()

while running:
    #Update all of the closest obstacles of each type to the player
    tx = [train1_x, train2_x, train3_x, train4_x, train5_x, train6_x, train7_x, train8_x, train9_x, train10_x]
    ty = [train1_y, train2_y, train3_y, train4_y, train5_y, train6_y, train7_y, train8_y, train9_y, train10_y]
    sx = [sign1_x, sign2_x, sign3_x, sign4_x, sign5_x, sign6_x]
    sy = [sign1_y, sign2_y, sign3_y, sign4_y, sign5_y, sign6_y]
    cx = [coin1_x, coin2_x, coin3_x, coin4_x, coin5_x, coin6_x]
    cy = [coin1_y, coin2_y, coin3_y, coin4_y, coin5_y, coin6_y]
    
    #Quitting event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #handle player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if player_lane != -1: 
                player_lane -= 1
                userAction_channel.play(dash)
        if keys[pygame.K_RIGHT]:
            if player_lane != 1: 
                player_lane +=1  
                userAction_channel.play(dash)     
        if keys[pygame.K_UP] and not player_jump:
            player_jump = True
            userAction_channel.play(jump)
        if keys[pygame.K_DOWN] and not player_slide:
            player_slide = True
            userAction_channel.play(slide)
        if player_lane == -1: player_x = LEFT
        if player_lane == 0: player_x = CENTER
        if player_lane == 1: player_x = RIGHT      

        if player_jump:
            player_img = pygame.image.load('assets/jump.png')     
            player_img = pygame.transform.scale(player_img, (50, 100))
            screen.blit(player_img, (player_x, player_y))
            player_y -= jump_height
            jump_height -= 20
            if jump_height < -10:
                player_jump = False
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
                player_img = pygame.transform.scale(player_img, (50, 100))
                screen.blit(player_img, (player_x, player_y))
                player_y -= slide_height
                slide_height +=20
                if slide_height > 10:
                    player_slide = False
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
    sign3_y += OBS_SPEED
    sign4_y += OBS_SPEED
    sign5_y += OBS_SPEED
    sign6_y += OBS_SPEED
    coin1_y += OBS_SPEED
    coin2_y += OBS_SPEED
    coin3_y += OBS_SPEED
    coin4_y += OBS_SPEED
    coin5_y += OBS_SPEED
    coin6_y += OBS_SPEED
    train1_y += TRAIN_SPEED
    train2_y += TRAIN_SPEED
    train3_y += TRAIN_SPEED
    train4_y += TRAIN_SPEED
    train5_y += TRAIN_SPEED
    train6_y += TRAIN_SPEED
    train7_y += TRAIN_SPEED
    train8_y += TRAIN_SPEED
    train9_y += TRAIN_SPEED
    train10_y += TRAIN_SPEED
    
    #collision detection 
    if player_invulnerable_frames > 0: player_invulnerable_frames -=1      
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    sign1_rect = pygame.Rect(sign1_x, sign1_y, sign_img.get_width(), sign_img.get_height())
    sign2_rect = pygame.Rect(sign2_x, sign2_y, sign_img.get_width(), sign_img.get_height())
    sign3_rect = pygame.Rect(sign3_x, sign3_y, sign_img.get_width(), sign_img.get_height())
    sign4_rect = pygame.Rect(sign4_x, sign4_y, sign_img.get_width(), sign_img.get_height())
    sign5_rect = pygame.Rect(sign5_x, sign5_y, sign_img.get_width(), sign_img.get_height())
    sign6_rect = pygame.Rect(sign6_x, sign6_y, sign_img.get_width(), sign_img.get_height())
    coin1_rect = pygame.Rect(coin1_x, coin1_y, coin_img.get_width(), coin_img.get_height())
    coin2_rect = pygame.Rect(coin2_x, coin2_y, coin_img.get_width(), coin_img.get_height())
    coin3_rect = pygame.Rect(coin3_x, coin3_y, coin_img.get_width(), coin_img.get_height())
    coin4_rect = pygame.Rect(coin4_x, coin4_y, coin_img.get_width(), coin_img.get_height())
    coin5_rect = pygame.Rect(coin5_x, coin5_y, coin_img.get_width(), coin_img.get_height())
    coin6_rect = pygame.Rect(coin6_x, coin6_y, coin_img.get_width(), coin_img.get_height())
    train1_rect = pygame.Rect(train1_x, train1_y, train_img.get_width(), train_img.get_height())
    train2_rect = pygame.Rect(train2_x, train2_y, train_img.get_width(), train_img.get_height())
    train3_rect = pygame.Rect(train3_x, train3_y, train_img.get_width(), train_img.get_height())
    train4_rect = pygame.Rect(train4_x, train4_y, train_img.get_width(), train_img.get_height())
    train5_rect = pygame.Rect(train5_x, train5_y, train_img.get_width(), train_img.get_height())
    train6_rect = pygame.Rect(train6_x, train6_y, train_img.get_width(), train_img.get_height())
    train7_rect = pygame.Rect(train7_x, train7_y, train_img.get_width(), train_img.get_height())
    train8_rect = pygame.Rect(train8_x, train8_y, train_img.get_width(), train_img.get_height())
    train9_rect = pygame.Rect(train9_x, train9_y, train_img.get_width(), train_img.get_height())
    train10_rect = pygame.Rect(train10_x, train10_y, train_img.get_width(), train_img.get_height())
    
    #SIGNS
    if player_rect.colliderect(sign1_rect) and player_invulnerable_frames ==0 and player_slide == False:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(sign2_rect) and player_invulnerable_frames ==0 and player_slide == False:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(sign3_rect) and player_invulnerable_frames ==0 and player_slide == False:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(sign4_rect) and player_invulnerable_frames ==0 and player_slide == False:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(sign5_rect) and player_invulnerable_frames ==0 and player_slide == False:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(sign6_rect) and player_invulnerable_frames ==0 and player_slide == False:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    #TRAINS
    if player_rect.colliderect(train1_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train2_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train3_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train4_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train5_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train6_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train7_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train8_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train9_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    elif player_rect.colliderect(train10_rect) and player_invulnerable_frames ==0:
        hitAction_channel.play(player_hit_sound)
        LIVES -= 1
        player_invulnerable_frames = 800
    #COINSE
    if player_rect.colliderect(coin1_rect) and player_invulnerable_frames ==0 and player_jump == True:
        SCORE +=1
        player_invulnerable_frames = 350
        userAction_channel.play(collect)
        collected = True
    elif player_rect.colliderect(coin2_rect) and player_invulnerable_frames ==0 and player_jump == True:
        SCORE +=1
        player_invulnerable_frames = 350
        userAction_channel.play(collect)
        collected = True
    elif player_rect.colliderect(coin3_rect) and player_invulnerable_frames ==0 and player_jump == True:
        SCORE +=1
        player_invulnerable_frames = 8000
        userAction_channel.play(collect)
        collected = True
    elif player_rect.colliderect(coin4_rect) and player_invulnerable_frames ==0 and player_jump == True:
        SCORE +=1
        player_invulnerable_frames = 800
        userAction_channel.play(collect)
        collected = True
    elif player_rect.colliderect(coin5_rect) and player_invulnerable_frames ==0 and player_jump == True:
        SCORE +=1
        player_invulnerable_frames = 800
        userAction_channel.play(collect)
        collected = True
    elif player_rect.colliderect(coin6_rect) and player_invulnerable_frames ==0 and player_jump == True:
        SCORE +=1
        player_invulnerable_frames = 800
        userAction_channel.play(collect)
        collected = True
    
    #Fill the background with black
    screen.fill((0,0,0))
    
    '''
    #Removing visuals
    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 155), (WIDTH /2, 150), 50)

    #display assets
    screen.blit(player_img, (player_x, player_y)) 
    screen.blit(sign_img, (sign1_x, sign1_y))
    screen.blit(sign_img, (sign2_x, sign2_y))
    screen.blit(sign_img, (sign3_x, sign3_y))
    screen.blit(sign_img, (sign4_x, sign4_y))
    screen.blit(sign_img, (sign5_x, sign5_y))
    screen.blit(sign_img, (sign6_x, sign6_y))
    screen.blit(coin_img, (coin1_x, coin1_y))
    screen.blit(coin_img, (coin2_x, coin2_y))
    screen.blit(coin_img, (coin3_x, coin3_y))
    screen.blit(coin_img, (coin4_x, coin4_y))
    screen.blit(coin_img, (coin5_x, coin5_y))
    screen.blit(coin_img, (coin6_x, coin6_y))
    screen.blit(train_img, (train1_x, train1_y))
    screen.blit(train_img, (train2_x, train2_y))
    screen.blit(train_img, (train3_x, train3_y))
    screen.blit(train_img, (train4_x, train4_y))
    screen.blit(train_img, (train5_x, train5_y))
    screen.blit(train_img, (train6_x, train6_y))
    screen.blit(train_img, (train7_x, train7_y))
    screen.blit(train_img, (train8_x, train8_y))
    screen.blit(train_img, (train9_x, train9_y))
    screen.blit(train_img, (train10_x, train10_y))
    '''
    #display score/lives
    score_text = font.render(f"Score: {SCORE}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {LIVES}", True, (255, 255, 255))
    screen.blit(score_text, (20,10))
    screen.blit(lives_text, (20, 40))
    
    # Flip the display
    pygame.display.flip()
    if LIVES == 0: running = False
    
    #RENDER AUDIO 
    #Updates tracked objects of each type
    if(trackedTrain_y > 1200) & (t < tMax):
        t += 1
    trackedTrain_x = tx[t]
    trackedTrain_y = ty[t]

    if(trackedSign_y > 800) & (s < sMax):
        s += 1
    trackedSign_x = sx[s]
    trackedSign_y = sy[s] 
       
    if(trackedCoin_y > 800) & (c < cMax):
        c += 1
    trackedCoin_x = cx[c]
    trackedCoin_y = cy[c]
    
    #Finds azimuth angle of each closest object of each type to user 
    tSlope = slope(player_x, player_y, trackedTrain_x, trackedTrain_y)
    tTheta = findAngle(999, (tSlope * 1), trackedTrain_x, trackedTrain_y)
    sSlope = slope(player_x, player_y, trackedSign_x, trackedSign_y)
    sTheta = findAngle(999, (sSlope * 1), trackedSign_x, trackedSign_y)
    cSlope = slope(player_x, player_y, trackedCoin_x, trackedCoin_y)
    cTheta = findAngle(999, (cSlope * 1), trackedCoin_x, trackedCoin_y)
    
    #Initialize thread for each object audio being streamed, updating is done in threads 
    train_thread = threading.Thread(target=trainAudioProcessing, args=(trackedTrain_y, tTheta))
    train_thread.start()
    
    sign_thread = threading.Thread(target=signAudioProcessing, args=(trackedSign_y, sTheta))
    sign_thread.start()
    
    coin_thread = threading.Thread(target=coinAudioProcessing, args=(trackedCoin_y, cTheta))
    coin_thread.start()
    
    if (pygame.time.get_ticks() > 60000):
        tada.play()
        running = False
    
#Game Over functionality
while True: 
    screen.fill((0, 0, 0))
    draw_text('Game Over!', font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 4)
    draw_text('Score: ' + str(SCORE) + ' / 6', font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 3)
    pygame.mixer.music.stop()
    
    # Done! Time to quit.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    pygame.display.flip()