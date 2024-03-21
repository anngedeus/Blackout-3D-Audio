Platform: VS Code 
Python Environment Version: 3.11.8
Python Dependencies: glob, pygame, os, numpy, soundfile, pydub, scipy (Installed via "pip install [dependency]")

Steps: 
1. Unzip File
2. Open ProofOfConcept folder
3. Create 3.11.8 Python Environment
4. Download dependencies via pip in console 
5. Run via VS Code w/ ProofOfConcept as default workspace folder

*Path Dependencies are handled in program, no further action required*

DISCLAIMER: I am aware that this is not the most optimal way to recreate 3D audio, as I would have preferred to do convolutions of chunks of streamed data and played directly to make the process as quick as possible.
However, I did not find a way to accomplish this in Python after attempting to use practically every audio library in the language such as sounddevice, playsound, pyaudio, pydub, winsound, and many others. 
This is reflected in the small auditory silence between each chunk of rendered data; the illusion of spatial sound is still present, but the transition between them is choppy at best. 
This could be due to many things, such as the time it takes to sample the audio file, the limitations of play modules in Python, lack of specs on the system, and many more. 
My ultimate goal is to stream the audio, do my operations, and queue the processed chunk while continuing, but I could not find a homogenous way to achieve this in Python. 
We will have to come up with other ways to achieve this task, as I fear that using this approach during our app development will have major problems with updating audio. 