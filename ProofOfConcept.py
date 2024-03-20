import numpy as np
import soundfile as sf
import playsound 
import sys, glob


#Loads list of KEMAR angles to be used by player
kemar = '.\KEMAR\diffuse\elev0\*.wav'
KEMAR = glob.glob(kemar)
for s in (range(len(KEMAR))):
    print(KEMAR[s])

#44100 sample of hemisphere around KEMAR at elevation 0, location chosen randomly
[HRTF, sample] = sf.read(KEMAR[15])

#TODO: translate stereo sounds to mono; boing track is only inherent mono track available so far

#Gathers attributes from 
[BoingHRTF, boingSample] = sf.read(".\Sounds\Boing.wav")
print(boingSample)
print(BoingHRTF.shape)

#Convolves the audio file with each column of KEMAR HRTF representing left and right inputs
L = np.convolve(BoingHRTF, HRTF[:,0])
R = np.convolve(BoingHRTF, HRTF[:,1])
Bin_Mix = np.vstack([L,R]).transpose()

#Saves binaural mix as .wav to be played by playsound
sf.write('SpatializedBoing.wav', Bin_Mix, boingSample)
print(Bin_Mix.shape)

playsound.playsound('SpatializedBoing.wav')