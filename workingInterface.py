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
train = AudioSegment.from_wav("Audio/TrainTest.wav")
sign = AudioSegment.from_wav("Audio/swinging.wav")
coin = AudioSegment.from_wav("Audio/shimmer.wav")

#Determines the playback chop of the audio, must be specified for different machines 
sampleRate = 200

#Bread and butter of audio processing
def trainAudioProcessing(ty, tTheta):
    global tTime, sampleRate
    #Is calculated for each object, determined by object's distance from character's head
    volume = max(0, min(1, (ty + 700) / 1500)) * 2
    
    #Only plays audio if in bounds of user hearing
    if (ty > -700) & (ty < 1000):
        #Creates chunk of audio file at a specific point in time with sampleRate length
        tHRTF = train[tTime:(tTime + sampleRate)]
        
        #Takes array from streamed audio chunk
        tHRTF = np.array(tHRTF.get_array_of_samples(), dtype=np.float32)
        tHRTF /= np.max(np.abs(tHRTF))
        
        #Determines HRTF choice from azimuth calculation given by theta
        trounded = round(tTheta / 5)
        tvalue = int(round((tTheta / 5)))
        
        [tLHRTF, sample] = sf.read(KEMAR[tvalue])
        [tRHRTF, sample] = sf.read(KEMAR[tvalue + 72])
        
        #Convolution step
        tL = np.convolve(tHRTF, tLHRTF)
        tR = np.convolve(tHRTF, tRHRTF)
        
        #Transposition step 
        tBin_Mix = np.vstack([tL,tR]).transpose()
        
        #Scales binaural mix to specs required by pygame to create sound object from numpy array
        tBin_Mix_scaled = (tBin_Mix * 32767 * volume).astype(np.int16)
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
    
    if (sy > -500) & (sy < 1000): 
        sHRTF = sign[sTime:(sTime + sampleRate)]
        
        sHRTF = np.array(sHRTF.get_array_of_samples(), dtype=np.float32)
        sHRTF /= np.max(np.abs(sHRTF))
        
        srounded = round(sTheta / 5)
        svalue = int(round((sTheta / 5)))
        
        [sLHRTF, sample] = sf.read(KEMAR[svalue])
        [sRHRTF, sample] = sf.read(KEMAR[svalue + 72])
        sL = np.convolve(sHRTF, sLHRTF)
        sR = np.convolve(sHRTF, sRHRTF)
        
        sBin_Mix = np.vstack([sL,sR]).transpose()
        sBin_Mix_scaled = (sBin_Mix * volume * 32767).astype(np.int16)
        
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
    
    if (cy > -500) & (cy < 1000): 
        cHRTF = coin[cTime:(cTime + sampleRate)]
        
        cHRTF = np.array(cHRTF.get_array_of_samples(), dtype=np.float32)
        cHRTF /= np.max(np.abs(cHRTF))
        
        crounded = round(cTheta / 5)
        cvalue = int(round((cTheta / 5)))
        
        [cLHRTF, sample] = sf.read(KEMAR[cvalue])
        [cRHRTF, sample] = sf.read(KEMAR[cvalue + 72])
        cL = np.convolve(cHRTF, cLHRTF)
        cR = np.convolve(cHRTF, cRHRTF)
        
        cBin_Mix = np.vstack([cL,cR]).transpose()
        
        cBin_Mix_scaled = (cBin_Mix * volume * 32767).astype(np.int16)
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
pygame.mixer.pre_init(88200)
pygame.mixer.init()
pygame.init()

#game constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 50
FPS = 60
OBS_SPEED = .75
TRAIN_SPEED = 1.5

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
train1_y = -HEIGHT * 1

train2_x = RIGHT
train2_y = -HEIGHT * 3

coin1_x = CENTER
coin1_y = -HEIGHT * 3

train3_x = CENTER
train3_y = -HEIGHT * 9

sign1_x = LEFT
sign1_y = -HEIGHT * 6

sign2_x = RIGHT
sign2_y = -HEIGHT * 8

coin2_x = CENTER
coin2_y = -HEIGHT * 10

train4_x = CENTER
train4_y = -HEIGHT * 14

#Defines set of obstacles used for reference by audio processing
t = 0
tMax = 3
trackedTrain_x = train1_x
trackedTrain_y = train1_y

s = 0
sMax = 1
trackedSign_x = sign1_x
trackedSign_y = sign1_y

c = 0
cMax = 1
trackedCoin_x = coin1_x
trackedCoin_y = coin1_y

#Creates separate audio channel for character inputs / movements
userAction_channel = pygame.mixer.Channel(1)

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("BlackOUT")

running = True

#Play royalty-free music (a must)
pygame.mixer.music.load("Audio/Grifting-in-Vegas_AdobeStock.wav")
pygame.mixer.music.play()

while running:
    #Update all of the closest obstacles of each type to the player
    tx = [train1_x, train2_x, train3_x, train4_x]
    ty = [train1_y, train2_y, train3_y, train4_y]
    sx = [sign1_x, sign2_x]
    sy = [sign1_y, sign2_y]
    cx = [coin1_x, coin2_x]
    cy = [coin1_y, coin2_y]
    
    #Quitting event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        footsteps.play()

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
            footsteps.stop()
            player_img = pygame.transform.scale(player_img, (50, 100))
            screen.blit(player_img, (player_x, player_y))
            player_y -= jump_height
            jump_height -=2
            if jump_height < -10:
                player_jump = False
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
    coin2_y += OBS_SPEED
    train1_y += TRAIN_SPEED
    train2_y += TRAIN_SPEED
    train3_y += TRAIN_SPEED
    train4_y += TRAIN_SPEED
    
    #collision detection 
    if player_invulnerable_frames >0: player_invulnerable_frames -=1      
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    sign1_rect = pygame.Rect(sign1_x, sign1_y, sign_img.get_width(), sign_img.get_height())
    sign2_rect = pygame.Rect(sign2_x, sign2_y, sign_img.get_width(), sign_img.get_height())
    coin1_rect = pygame.Rect(coin1_x, coin1_y, coin_img.get_width(), coin_img.get_height())
    coin2_rect = pygame.Rect(coin2_x, coin2_y, coin_img.get_width(), coin_img.get_height())
    train1_rect = pygame.Rect(train1_x, train1_y, train_img.get_width(), train_img.get_height())
    train2_rect = pygame.Rect(train2_x, train2_y, train_img.get_width(), train_img.get_height())
    train3_rect = pygame.Rect(train3_x, train3_y, train_img.get_width(), train_img.get_height())
    train4_rect = pygame.Rect(train4_x, train4_y, train_img.get_width(), train_img.get_height())
    
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
    elif player_rect.colliderect(train2_rect) and player_invulnerable_frames ==0:
        player_hit_sound.play()
        LIVES -= 1
        player_invulnerable_frames = 2100
    elif player_rect.colliderect(train3_rect) and player_invulnerable_frames ==0:
        player_hit_sound.play()
        LIVES -= 1
        player_invulnerable_frames = 2100
    elif player_rect.colliderect(train4_rect) and player_invulnerable_frames ==0:
        player_hit_sound.play()
        LIVES -= 1
        player_invulnerable_frames = 2100
    #COINSE
    if player_rect.colliderect(coin1_rect) and player_invulnerable_frames ==0 and player_jump == True:
        SCORE +=1
        player_invulnerable_frames = 1800
        userAction_channel.play(collect)
        collected = True
    elif player_rect.colliderect(coin2_rect) and player_invulnerable_frames ==0 and player_jump == True:
        SCORE +=1
        player_invulnerable_frames = 1800
        userAction_channel.play(collect)
        collected = True
    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 155), (WIDTH /2, 150), 50)

    #display assets
    screen.blit(player_img, (player_x, player_y)) 
    screen.blit(sign_img, (sign1_x, sign1_y))
    screen.blit(sign_img, (sign2_x, sign2_y))
    screen.blit(coin_img, (coin1_x, coin1_y))
    screen.blit(coin_img, (coin2_x, coin2_y))
    screen.blit(train_img, (train1_x, train1_y))
    screen.blit(train_img, (train2_x, train2_y))
    screen.blit(train_img, (train3_x, train3_y))
    screen.blit(train_img, (train4_x, train4_y))
    #display score/lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {SCORE}", True, (0,0,0))
    lives_text = font.render(f"Lives: {LIVES}", True, (0,0,0))
    screen.blit(score_text, (20,10))
    screen.blit(lives_text, (20, 40))
    # Flip the display
    pygame.display.flip()
    if LIVES == 0: running = False
    
    #RENDER AUDIO 
    #Updates tracked objects of each type
    if(trackedTrain_y > 1000) & (t < tMax):
        t += 1
    trackedTrain_x = tx[t]
    trackedTrain_y = ty[t]

    if(trackedSign_y > 600) & (s < sMax):
        s += 1
    trackedSign_x = sx[s]
    trackedSign_y = sy[s] 
       
    if(trackedCoin_y > 600) & (c < cMax):
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
    
# Done! Time to quit.
pygame.quit()