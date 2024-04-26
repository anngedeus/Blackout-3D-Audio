# Blackout-3D-Audio
Welcome to BlackOUT! 
This is a 3D Audio Python game where players must navigate between three lanes to avoid trains and swinging signs while collecting coins but with no visual aid. 
Players must rely on what they hear to decide when to switch lanes, jump, or slide. 

## Features
* Simple yet addictive gameplay
* Coin collection system to earn points
* 3D Audio integration for an immersive experience

## Technologies and Databases Used
* Python 3
* Pygame Library
* Pydub
* KEMAR HRTF

## Installation
1. clone the repository: 'git clone https://github.com/anngedeus/Blackout-3D-Audio.git'
2. Install Pygame if not already installed: 'pip install pygame'
3. Install pydub is not already installed: 'pip install pydub'
4. Run 'startScene.py' to start the game

## How to Play
* Use the left and right arrow keys to move between lanes, you will hear a whooshing sound when this happens
* Use the down arrow to slide, you will hear a gravel sliding sound; this will come in handy to avoid swinging signs that are creaking
* Use the up arrow to jump, boing sound, which will help collect coins, shimmer sound
* There are a total of 3 lives that can be lost anytime you hit a train or sign followed by an umph sound
* When all three lives are lost or there are no more coins to earn, the game will end

## Three Design Decisions Made as a Perceptual Consideration for the user 
1. Distinct audio cues: Players can differentiate between switching lanes, sliding, and jumping with a distinct sound cue allowing them to navigate the game effectively and know what action they are doing
2. Consistent audio feedback: Players can quickly recognize events such as collisions with trains or signs and collecting coins with consistent audio feedback. These sounds include a low pitch "umph" sound when a player is hit and a high pitch beam sound when a coin is collected. 
3. Sound Volume and Choices: To avoid overstimulation and confusion, the volume of the background track and other sounds have been adjusted so that players can hear and distinguish the different sounds in this game. The sound of running footsteps has been removed to alleviate confusion about distinct sounds during gameplay.
