import glob
import numpy as np
import soundfile as sf
import librosa
import sounddevice as sd
import os

# Loads list of KEMAR angles to be used by player
kemar = './KEMAR/full/elev0/*.wav'
KEMAR = glob.glob(kemar)

# After splitting file, loop through each KEMAR angle and create a binaural mix to give the illusion of moving sound clockwise
for i in range(0, len(KEMAR) // 2):
    t1 = i * 1300
    t2 = t1 + 1300
    
    # Load audio file and snippet that is to be convolved 
    snippet, sr = librosa.load("./Sounds/BackOnMyBS.wav", sr=None, offset=t1/1000, duration=1300/1000)
    
    # HRTF in clockwise circle gathered and convolved with current snippet
    LHRTF, sr = librosa.load(KEMAR[i], sr=None)
    RHRTF, sr = librosa.load(KEMAR[i + 72], sr=None)
    L = np.convolve(snippet, LHRTF)
    R = np.convolve(snippet, RHRTF)
    
    # Binaural mix NumPy array is created, this is the desired final audio data 
    Bin_Mix = np.vstack([L, R]).transpose()
    
    # Play audio using sounddevice
    sd.play(Bin_Mix, samplerate=sr)
    sd.wait()

# Delete chunk files from local OS
for i in range(len(KEMAR) // 2):
    os.remove(f"rotate{i}.wav")
