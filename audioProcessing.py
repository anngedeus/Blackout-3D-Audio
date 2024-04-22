import glob, pygame, os
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import time

pygame.mixer.pre_init(88200, -16, 2, 4096)
pygame.mixer.init()
pygame.init()

kemar = './KEMAR/full/elev0/*.wav'
KEMAR = glob.glob(kemar)

audio = AudioSegment.from_mp3("Audio/TrainFinal.wav")

sampleRate = 200

j = 0
for i in range(0, len(audio), sampleRate):
    #Creates sample based on audio length and sample rate variable
    HRTF = audio[i:i + sampleRate]
    
    #Takes array from audio chunk streamed 
    HRTF = np.array(HRTF.get_array_of_samples(), dtype=np.float32)
    HRTF /= np.max(np.abs(HRTF))
    
    #HRTF  convolved with current snippet
    [LHRTF, sample] = sf.read(KEMAR[j])
    [RHRTF, sample] = sf.read(KEMAR[j + 72])
    
    #Logic check for what HRTF to use 
    j += 1
    if j == 36:
        j = 0
    L = np.convolve(HRTF, LHRTF)
    R = np.convolve(HRTF, RHRTF)
    
    #Binaural mix NumPY array is created, this is the desired final audio data 
    Bin_Mix = np.vstack([L,R]).transpose()
    
    #Scales Binary Mix and makes it a contiguous array 
    Bin_Mix_scaled = (Bin_Mix * 32767).astype(np.int16)
    Bin_Mix_scaled = np.ascontiguousarray(Bin_Mix_scaled)

    #Creates and plays sound based on array
    sound = pygame.sndarray.make_sound(Bin_Mix_scaled)
    sound = pygame.mixer.Sound(sound)
    sound.play()
    #Toy around with time for time.sleep to work properly on different system 
    time.sleep(0.195)
    


pygame.quit()
