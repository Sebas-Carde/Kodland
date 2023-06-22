import pygame
import sys
import random
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((680, 600))

collision = False  # Variable para controlar la ventana de colisión
puntaje = 0
FONDO = pygame.image.load("assets/Fondo_Snake.png")

# ------------------------------JUEGO-----------------------------
class Cuerpo:
    def __init__(self, SCREEN):
        self.x = 0
        self.y = 40
        self.SCREEN = SCREEN
        self.dir = 0  # 0 right, 1 left, 2 down, 3 up

    def draw(self):
        pygame.draw.rect(self.SCREEN, (255, 224, 0), (self.x, self.y, 40, 40))

    def movement(self):
        if self.dir == 0:
            self.x += 40
        elif self.dir == 1:
            self.x -= 40
        elif self.dir == 2:
            self.y += 40
        elif self.dir == 3:
            self.y -= 40


class Food:
    def __init__(self, SCREEN):
        self.x = random.randrange(0, 680, 40)
        self.y = random.randrange(40, 600, 40)
        self.SCREEN = SCREEN
        
    def draw(self):
        pygame.draw.rect(self.SCREEN, (255, 0, 0), (self.x, self.y, 40, 40))

    def relocate(self):
        self.x = random.randrange(0, 680, 40)
        self.y = random.randrange(40, 600, 40)


class Wall:
    def __init__(self, SCREEN, comida):
        while True:
            self.x = random.randrange(0, 680, 40)
            self.y = random.randrange(40, 600, 40)
            if self.x != comida.x or self.y != comida.y:
                collision_with_snake = False
                for cuerpo in snake:
                    if self.x == cuerpo.x and self.y == cuerpo.y:
                        collision_with_snake = True
                        break
                if not collision_with_snake:
                    break
        self.SCREEN = SCREEN

    def draw(self):
        pygame.draw.rect(self.SCREEN, (87, 138, 52), (self.x, self.y, 40, 40))

    def relocate(self, comida):
        while True:
            self.x = random.randrange(0, 680, 40)
            self.y = random.randrange(40, 600, 40)
            if self.x != comida.x or self.y != comida.y:
                collision_with_snake = False
                for cuerpo in snake:
                    if self.x == cuerpo.x and self.y == cuerpo.y:
                        collision_with_snake = True
                        break
                if not collision_with_snake:
                    break

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def redraw(SCREEN):
    SCREEN.fill("black")
    SCREEN.blit(FONDO, (0, 40))
    SCREEN.blit(BACK_TEXT, BACK_RECT)
    comida.draw()
    for obstaculo in obstaculos:
        obstaculo.draw()
    texto_puntaje = "Puntaje: {}".format(puntaje)
    texto_puntaje_superficie = get_font(26).render(texto_puntaje, True, (255, 255, 255))
    texto_puntaje_rect = texto_puntaje_superficie.get_rect()
    texto_puntaje_rect.center = (400, 20)
    SCREEN.blit(texto_puntaje_superficie, texto_puntaje_rect)
    for i in range(len(snake)):
        snake[i].draw()

def snake_ubicacion():
    if len(snake) > 1:
        for i in range(len(snake) - 1):
            snake[len(snake) - i - 1].x = snake[len(snake) - i - 2].x
            snake[len(snake) - i - 1].y = snake[len(snake) - i - 2].y


def Colision():
    global puntaje, collision
    hit = False
    if len(snake) > 1:
        for i in range(len(snake) - 1):
            if snake[0].x == snake[i + 1].x and snake[0].y == snake[i + 1].y:
                hit = True
    for obstaculo in obstaculos:
        if snake[0].x == obstaculo.x and snake[0].y == obstaculo.y:
            hit = True
    if hit:
        puntaje_aux = puntaje
        puntaje = 0
        collision = True
        if show_collision_window(puntaje_aux):
            return True
    return hit

def show_collision_window(puntaje_aux):
    global collision

    while collision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(pygame.mouse.get_pos()):
                    collision = False  # Establecer collision en False para salir del bucle
                    return True  # Indica que el jugador desea volver al menú principal

        SCREEN.fill("black")
        texto_puntaje = "Puntaje obtenido: {}".format(puntaje_aux)
        texto_puntaje_superficie = get_font(26).render(texto_puntaje, True, (255, 255, 255))
        texto_puntaje_rect = texto_puntaje_superficie.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 50))
        SCREEN.blit(texto_puntaje_superficie, texto_puntaje_rect)

        OPTIONS_BACK.changeColor(pygame.mouse.get_pos())
        OPTIONS_BACK.update(SCREEN)

        pygame.display.update()

def play2():
    global puntaje, comida, snake, obstaculos
    
    while True:
        SCREEN.fill("black")
        SCREEN.blit(FONDO, (0, 40))

        pygame.display.set_caption("Snake")
        snake = [Cuerpo(SCREEN)]
        snake[0].draw()
        comida = Food(SCREEN)
        obstaculos = []
        for _ in range(10):  # Generar 10 bloques sólidos aleatorios
            obstaculo = Wall(SCREEN, comida)
            obstaculos.append(obstaculo)
            obstaculo.draw()
        redraw(SCREEN)
        run = True
        velocidad = 100

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        snake[0].dir = 2
                    if event.key == pygame.K_LEFT:
                        snake[0].dir = 1
                    if event.key == pygame.K_RIGHT:
                        snake[0].dir = 0
                    if event.key == pygame.K_UP:
                        snake[0].dir = 3
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(pygame.mouse.get_pos()):
                        return  # Regresar al menú principal

            snake_ubicacion()
            redraw(SCREEN)
            snake[0].movement()
            redraw(SCREEN)
            pygame.display.update()
            pygame.time.delay(velocidad)

            if snake[0].x >= 680:
                snake[0].x = 0
            elif snake[0].x < 0:
                snake[0].x = 680

            if snake[0].y >= 600:
                snake[0].y = 40
            elif snake[0].y < 40:
                snake[0].y = 600

            if Colision():
                snake = [Cuerpo(SCREEN)]
                comida.relocate()
                obstaculos = []
                for _ in range(10):  # Generar 10 bloques sólidos aleatorios
                    obstaculo = Wall(SCREEN, comida)
                    obstaculos.append(obstaculo)
                    obstaculo.draw()
                velocidad = 100

            if snake[0].x == comida.x and snake[0].y == comida.y:
                puntaje += 1
                if velocidad > 35:
                    velocidad -= 5
                comida.relocate()
                snake.append(Cuerpo(SCREEN))
                snake_ubicacion()

        pygame.display.update()
        # -----

# Definir OPTIONS_BACK como una variable global
OPTIONS_BACK = Button(image=None, pos=(40, 20), 
                          text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")
BACK_TEXT = get_font(20).render("MENU", True, "White")
BACK_RECT = BACK_TEXT.get_rect(center=(40, 20))  