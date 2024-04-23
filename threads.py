import threading
import pygame
import time

def run_blackoutinterface():
    exec(open("./blackoutInterface.py").read())

def run_audioprocessing():
    exec(open("./audioProcessing.py").read())

def main():
    pygame.init()
    
    thread1 = threading.Thread(target=run_blackoutinterface)
    thread2 = threading.Thread(target=run_audioprocessing)
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    pygame.quit()

if __name__ == "__main__":
    main()
