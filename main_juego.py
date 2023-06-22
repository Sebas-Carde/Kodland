import pygame
import sys

from button import Button
import snake_game
import snake_game2

pygame.init()

SCREEN = pygame.display.set_mode((680, 600))
pygame.display.set_caption("Menu")

# Otras variables globales...

BG = pygame.image.load("assets/Background.png")
SNAKE = pygame.image.load("assets/sanke.png")



# ------------------------------MENU------------------------------
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(SNAKE, (400, 225))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(85).render("SNAKE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(340, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(200, 250), 
                            text_input="SNAKE LIBRE", font=get_font(25), base_color="White", hovering_color="#d7fcd4")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(200, 350), 
                            text_input="SNAKE LIBRE 2.0", font=get_font(25), base_color="White", hovering_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(200, 450), 
                            text_input="QUIT", font=get_font(25), base_color="White", hovering_color="#d7fcd4")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    snake_game.play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    snake_game2.play2()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
  
main_menu()