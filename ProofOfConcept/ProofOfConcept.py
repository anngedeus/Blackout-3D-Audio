import glob, pygame, os
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from scipy.io.wavfile import write

#Loads list of KEMAR angles to be used by player
kemar = './KEMAR/full/elev0/*.wav'
KEMAR = glob.glob(kemar)

#After splitting file, loop through each KEMAR angle and create a binaural mix to give the illusion of moving sound clockwise
for i in (range(0, int((len(KEMAR) / 2) - 1), 1)):
    t1 = i * 1300
    t2 = t1 + 1300
    
    #Loads audio file and snippet that is to be convolved 
    snippet = AudioSegment.from_wav("./Sounds/BackOnMyBS.wav")
    snippet = snippet[t1:t2]
    
    #Must export snippet as .wav file to read NumPY array 
    snippet.export("rotate.wav", format="wav")
    [bsHRTF, bsSample] = sf.read("rotate.wav")
    bsHRTF = np.mean(bsHRTF, axis=1)
    
    #HRTF in clockwise circle gathered and convolved with current snippet
    [LHRTF, sample] = sf.read(KEMAR[i])
    [RHRTF, sample] = sf.read(KEMAR[i + 72])
    L = np.convolve(bsHRTF, LHRTF)
    R = np.convolve(bsHRTF, RHRTF)
    
    #Binaural mix NumPY array is created, this is the desired final audio data 
    Bin_Mix = np.vstack([L,R]).transpose()
    
    #NOTE: The original idea was to be streaming this audio and have the binaural mix play directly here, but the lag time in the audio was so severe that it was not possiible. 
    #I am not sure if a library that can play NumPy arrays such as what is required even exists in Python:
    # - Sounddevice is not allowed to queue audio, so there are major gaps in the produced sound
    # - Playsound does not allow for NumPy arrays 
    # - PyAudio does not allow for NumPy arrays 
    #Instead, my approach was to save each chunk and play them directly as .wav files, deleting them after use: 
    name = "rotate" + str(i) + ".wav"
    write(name, 44611, Bin_Mix.astype(np.float32))
    

#Establish pygame mixer queue to load audio quicker than other libraries in Python
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

#Load each chunk into pygame mixer and play through queue
j = 1
for i in range(0, 70, 2):
    name1 = "rotate" + str(i) + ".wav"
    name2 = "rotate" + str(j) + ".wav"
    j += 2
    
    pygame.mixer.music.load(name1)
    pygame.mixer.music.queue(name2)
    pygame.mixer.music.play()
    
    #Loop makes sure the mixer does not skip any parts of queue, could be leading to the delay of audio chunks
    while pygame.mixer.music.get_busy():
        clock.tick(30)

#Cleanup 
pygame.quit()
os.remove("rotate.wav")

#Delete chunk files from local OS
for i in range(0, 71, 1):
    name = "rotate" + str(i) + ".wav"
    os.remove(name)