# Import Libaries
from turtle import width
import pygame
import os

# Imports Fonts and the ability to use sounds
pygame.font.init()
pygame.mixer.init()

# Setting the display height and 
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!!!")

# Defining colors that will be used in the game 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Creating a border so the spaceships can't fly off the display
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Defining a name for each sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# Defining fonts for health and winner screen
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60 # Defining FPS (frames per second)
VEL = 5 # Velocity which is how fast things move on the screen
BULLET_VEL = 7 # Defining how fast the bullets move
MAX_BULLETS = 3

# Defining the variables for how big the image of the spaceship is
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# This creates 2 separate events so when one gets hit it doesn't effect the other
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT =pygame.USEREVENT + 2

# Importing Yellow Spacehip image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
# Rotates the spaceship so that they are facing eachother
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Importing Yellow Spacehip image
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
# Rotates the spaceship so that they are facing eachother
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Importing the background image
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0)) # Inserts the background image to the background
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Assigns a variable for the visable health box 
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    # Draws the health on the screen and assigning the location for the health
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Draws the spaceships on the screen
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Draws the bullets on the screen
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update() # Updates the display so that the changes show up on the display

# Assigns yellows movement to keys 
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #Right
        yellow.x += VEL 
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #Up 
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10: #Down
        yellow.y += VEL

# Assigns reds movement to keys
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #Right
        red.x += VEL 
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #Up 
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10: #Down
        red.y += VEL 

# Collisions with bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
# If the yellow bullet collides with the red ship it will take reds health
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet) # Removes the bullets after a collision
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet) # Removes the bullets if they go off the screen
          
# If the red bullet collides with the yellow ship it will take yellows health
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet) # Removes the bullets after a collision
        elif bullet.x < 0:
            red_bullets.remove(bullet) # Removes the bullets if they go off the screen

# Defines where and how long the winner's name is on the screen 
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2)) # Center Winner Name
    pygame.display.update() # Updates changes
    pygame.time.delay(5000) #In milliseconds 5000 = 5 seconds. How long it's on screen

# Our main game loop
def main():
    # Creates rectangle for the red and yellow spaceship
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    # Defined red and yellow's health
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock() # defines time in pygame
    run = True # when the loop is running
    while run:
        clock.tick(FPS) # sets 60 frames per second
        # Makes it so your abe to quit the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
              # Draws yellow bullets on the screen
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

              # Draws red bullets on the screen
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # When red is hit it subtracts it health by one
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play() # plays sound when red is hit

            # When yellow is hit it subtracts it health by one
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play() # plays sound when yellow is hit

        winner_text = ""
        if red_health <= 0: # If red's health is equal to 0 then display yellow wins
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:# If yellow's health is equal to 0 then display red wins
            winner_text = "Red Wins!"
        # Draws Winner
        if winner_text != "":
            draw_winner(winner_text)
            break # Ends the loop

        # Inserts movements
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # Inserts bullets
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Draws window
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main() # Calls the main loop and restarts it

if __name__ == "__main__":
    main()