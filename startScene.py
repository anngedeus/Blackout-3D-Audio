import pygame
import sys
import subprocess

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlackOUT")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)
def start_blackout_game():
    try:
        subprocess.run(['python3', './workingInterface.py'])
    except FileNotFoundError:
        print("Error: Could not find 'workingInterface.py'.")

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Welcome to Blackout!', font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('Click the play button to begin', font, BLACK, screen, WIDTH // 2, HEIGHT // 3)
        play_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
        pygame.draw.rect(screen, BLACK, play_button)
        draw_text('Play', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    start_blackout_game()
                    print("Starting the game!")
        
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
