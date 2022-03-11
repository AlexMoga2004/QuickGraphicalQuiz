# import the libraries
import pygame
import random

pygame.init()
pygame.font.init()

# create the main pygame window
(width, height) = (852, 852)
display = pygame.display.set_mode((width, height))
cars = [pygame.image.load("redCar.png"), pygame.image.load("greenCar.png")]
carSprites = []
backgroundSprites = []
buttons = []

# define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
gui_font = pygame.font.SysFont("Comic Sans MS", 50)

# set the initial values for the program
running = True
newQuestion = True
answeredQuestions = []
selection = -1
correctChoice = -1
currentMessage = ""
player1Score = 0
player2Score = 0
player1Turn = False


# Class button reference : https://github.com/clear-code-projects/elevatedButton
class Button:
    def __init__(self, text, width, height, pos, elevation, id):
        # Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.id = id

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(display, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(display, self.top_color, self.top_rect, border_radius=12)
        display.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global selection
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed:
                    selection = self.id
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'


# Sprite for the background
class Background(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos):
        super().__init__()
        self.image = pygame.image.load("track.gif").convert()
        self.rect = self.image.get_rect()
        self.xPos = xPos
        self.yPos = yPos

    def draw(self):
        display.blit(self.image, (self.xPos, self.yPos))

    def scroll(self, amount):
        self.yPos += amount


# Function to create the background
def createBackground(xPos, yPos):
    backgroundSprites.append(Background(xPos, yPos))


# Create a pygame sprite for the cars
class Car(pygame.sprite.Sprite):
    xPos = 0
    yPos = 0
    vel = 0
    acc = 0

    # Constructor for the class
    def __init__(self, number):
        super().__init__()
        self.image = random.choice(cars).convert_alpha()
        if number == 1:
            self.xPos = 240
        else:
            self.xPos = 500
        self.id = number
        self.yPos = 400
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect()

    def draw(self):
        global player1Score
        global player2Score
        self.vel += self.acc
        if self.vel > 0:
            self.acc -= 1
        elif self.vel < 0:
            self.acc += 1
        else:
            self.acc = 0
        self.yPos += self.vel

        display.blit(self.image, (self.xPos, self.yPos,))


# A function to create new car sprite (1 = main player, 2 = AI)
def createCar(number):
    global carSprites
    carSprites.append(Car(number))


# Create one player and one AI car

createCar(1)
createCar(2)
createBackground(0, 0)
createBackground(0, 480)
createBackground(0, -480)
createBackground(0, -480 * 2)
# Main game loop
while running:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if newQuestion:
        f = open("Questions.txt", "r")
        line = f.readlines()
        numLines = len(line)
        buttons.clear()
        # Ensure that the question has not been asked already
        while True:
            index = random.randint(0, numLines - 1)
            if index not in answeredQuestions:
                break
        answeredQuestions.append(index)
        splitLine = line[index].split(", ")
        currentMessage = splitLine[0]
        buttons.append(Button(splitLine[1], 200, 40, (200, 650), 5, 1))
        buttons.append(Button(splitLine[2], 200, 40, (452, 650), 5, 2))
        buttons.append(Button(splitLine[3], 200, 40, (200, 750), 5, 3))
        buttons.append(Button(splitLine[4], 200, 40, (452, 750), 5, 4))
        correctChoice = int(splitLine[5])
        print(correctChoice)
        newQuestion = False
        selection = -1

    if 1 <= selection <= 4:
        player1Turn = not player1Turn
        if selection == correctChoice:
            print("correct")
            if player1Turn:
                player1Score += 1
                for car in carSprites:
                    if car.id == 1:
                        car.acc = -4
            else:
                player2Score += 1
                for car in carSprites:
                    if car.id == 2:
                        car.acc = -4
        else:
            print("wrong")
            if player1Turn:
                player1Score -= 1
                for car in carSprites:
                    if car.id == 1:
                        car.acc = 5
            else:
                player2Score -= 1
                for car in carSprites:
                    if car.id == 2:
                        car.acc = 5

        selection = -1
        newQuestion = True

    # Clear the display
    display.fill(white)

    # Draw the current backgrounds
    for background in backgroundSprites:
        background.scroll(3)
        # Stop rendering backgrounds that are no longer available
        if background.yPos >= 480 * 3:
            backgroundSprites.remove(background)
        if len(backgroundSprites) < 4:
            createBackground(0, -480)

        background.draw()

    # Draw the buttons and replace the question if necessary
    textsurface = gui_font.render(currentMessage, False, black)
    display.blit(textsurface, (100, 550))
    for button in buttons:
        button.draw()

    # Draw the current cars
    for car in carSprites:
        car.draw()

    pygame.display.flip()

# Once the game has completed
pygame.quit()
