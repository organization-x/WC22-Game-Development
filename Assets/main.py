#Chirag & Aidan

import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

import math

pygame.init()

pygame.font.init()

pygame.display.set_caption('   Blazingboy and Aquagirl ')

WIDTH, HEIGHT = 600, 400

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

display = pygame.Surface((510, 470))

# Colors
white = (255, 255, 255)

#Defining all images used 
fireboy_image = (pygame.image.load('fb.webp').convert_alpha())
fireboy_image = pygame.transform.scale(fireboy_image, (15, 40))

watergirl_image = (pygame.image.load('wg.webp').convert_alpha())
watergirl_image = pygame.transform.scale(watergirl_image, (15, 40))

brick = pygame.image.load('brick.png').convert_alpha()
brick = pygame.transform.scale(brick, (16, 8))

lava = pygame.image.load('lava.png').convert_alpha()
lava = pygame.transform.scale(lava, (16, 8))

water = pygame.image.load('water.png').convert_alpha()
water = pygame.transform.scale(water, (16, 8))

toxic = pygame.image.load('toxic.png').convert_alpha()
toxic = pygame.transform.scale(toxic, (16, 8))

blue_gem=pygame.image.load('gem_blue.png').convert_alpha()
blue_gem = pygame.transform.scale(blue_gem, (10, 10))

red_gem=pygame.image.load('gem_red.png').convert_alpha()
red_gem = pygame.transform.scale(red_gem, (12, 12))

fireboy_door = pygame.image.load('FB_door.png').convert_alpha()
fireboy_door = pygame.transform.scale(fireboy_door, (28, 35))

watergirl_door = pygame.image.load('WG_door.png').convert_alpha()
watergirl_door = pygame.transform.scale(watergirl_door, (28, 35))

winner_font = pygame.font.SysFont('calibri', 50)

#Function to load the map file and split it into a list
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

#Loads file
game_map = load_map('map')

#Function to test if one rect collides with another, and return it
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#Function that allows characters to move without walking thru walls
def move(rect, movement, tiles, kill):
    collision_types = {
        'top': False,
        'bottom': False,
        'right': False,
        'left': False
    }
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    touch_poison=collision_test(rect,kill)
    for tile in touch_poison:
      if movement[1] > 0:
        rect.x=60
        rect.y=400
    
    return rect, collision_types


# Level Completion Text
def draw_winner(text):
  draw_text = winner_font.render(text, 1, white)
  screen.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
  pygame.display.update()
  pygame.time.delay(1000)
  
  
#Presets values for fireboy and watergirls movement/jumping
fbmoving_right = False
fbmoving_left = False

wgmoving_right = False
wgmoving_left = False

fireboy_y_momentum = 0
fireboy_air_timer = 0

watergirl_y_momentum = 0
watergirl_air_timer = 0

fireboy_rect = pygame.Rect(60, 400, fireboy_image.get_width(),
                           fireboy_image.get_height())

watergirl_rect = pygame.Rect(30, 400, watergirl_image.get_width(),
                             watergirl_image.get_height())


#Sets position for gems
red_gem_rects=[pygame.Rect(323,400,12,12),pygame.Rect(115,300,12,12),pygame.Rect(238,220,12,12),pygame.Rect(170,125,12,12),pygame.Rect(337,25,12,12)]

blue_gem_rects=[pygame.Rect(163,400,12,12),pygame.Rect(275,300,12,12),pygame.Rect(115,220,12,12),pygame.Rect(337,125,12,12),pygame.Rect(158,25,12,12)]

# Positions for Doors
fireboy_door_rect = pygame.Rect(400, 25, fireboy_door.get_width(), fireboy_door.get_height())

watergirl_door_rect = pygame.Rect(450, 25, watergirl_door.get_width(), watergirl_door.get_height())


#Plays the BG Music
pygame.mixer.music.load('music.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

#Sets up score vals
score=7500
score_counter=0

while True:  # game loop
    display.fill((51, 51, 26))

    score_counter+=1
    score-=((90/score_counter)+1)
    
    tile_rects = []
    harmwg=[]
    harmfb=[]

  #Makes map from the map.txt file
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(brick, (x * 16, y * 8))
            elif tile == '2':
                display.blit(lava, (x * 16, y * 8))
                harmwg.append(pygame.Rect(x * 16, y * 8, 16, 8))
            elif tile == '3':
                display.blit(water, (x * 16, y * 8))
                harmfb.append(pygame.Rect(x * 16, y * 8, 16, 8))
            elif tile == '4':
                display.blit(toxic, (x * 16, y * 8))
                harmfb.append(pygame.Rect(x * 16, y * 8, 16, 8))
                harmwg.append(pygame.Rect(x * 16, y * 8, 16, 8))
            if tile == '1':
                tile_rects.append(pygame.Rect(x * 16, y * 8, 16, 8))

            x += 1
        y += 1

    #Moving Parts: Doors, Elevators, & Buttons
    button1=pygame.Rect(336,155,15,5)
    button2=pygame.Rect(236,250,15,5)
    button1draw=pygame.draw.rect(display,(153,0,153),button1)
    button2draw=pygame.draw.rect(display,(153,0,153),button2)
    if (collision_test(fireboy_rect,[button1,button2]) != []) or collision_test(watergirl_rect,[button1,button2]) != []:
      elevator=pygame.draw.rect(display,(0,0,0),pygame.Rect(425,235,70,18))
    else:
      elevator=pygame.draw.rect(display,(0,0,0),pygame.Rect(425,159,70,18))
    tile_rects.append(elevator)  

    button3=pygame.Rect(336,59,15,5)
    button4=pygame.Rect(156,59,15,5)
    button3draw=pygame.draw.rect(display,(153,0,153),button3)
    button4draw=pygame.draw.rect(display,(153,0,153),button4)
    if  (collision_test(fireboy_rect,[button3,button4]) != []) or collision_test(watergirl_rect,[button3,button4]) != []:
      door=pygame.draw.rect(display,(0,0,0),pygame.Rect(250,-50,10,68))
    else:
      door=pygame.draw.rect(display,(0,0,0),pygame.Rect(250,0,10,68))
    tile_rects.append(door)

  # Door Collisions 
    if (collision_test(fireboy_rect,[fireboy_door_rect]) != []) or collision_test(watergirl_rect, [watergirl_door_rect]):
      winner_text = "Level Complete!"
      draw_winner(winner_text)
      break
  
  #Draws Gems
    for gem in red_gem_rects:
      display.blit(red_gem,(gem[0],gem[1]))
      if collision_test(fireboy_rect,[gem]) !=[]:
        red_gem_rects.remove(gem)
        score+=50
      
    for gem in blue_gem_rects:
      display.blit(blue_gem,(gem[0],gem[1]))
      if collision_test(watergirl_rect,[gem]) !=[]:
        blue_gem_rects.remove(gem)
        score+=50
        
  # Draws Doors
    for door in fireboy_door_rect:
      display.blit(fireboy_door, (400, 30))

    for door in watergirl_rect:
      display.blit(watergirl_door, (450, 30))

        
  #Fire Boy movement & collisions
    fireboy_movement = [0, 0]
    if fbmoving_right:
        fireboy_movement[0] += 2
    if fbmoving_left:
        fireboy_movement[0] -= 2
    fireboy_movement[1] += fireboy_y_momentum
    fireboy_y_momentum += 0.15
    if fireboy_y_momentum > 3:
        fireboy_y_momentum = 3

    fireboy_rect, fireboy_collisions = move(fireboy_rect, fireboy_movement,
                                            tile_rects,harmfb)

    if fireboy_collisions['bottom']:
        fireboy_y_momentum = 0
        fireboy_air_timer = 0
    else:
        fireboy_air_timer += 1

    if fireboy_collisions['top']:
        fireboy_y_momentum = 0

  #Watergirl movement & collisions
    watergirl_movement = [0, 0]
    if wgmoving_right:
        watergirl_movement[0] += 2
    if wgmoving_left:
        watergirl_movement[0] -= 2
    watergirl_movement[1] += watergirl_y_momentum
    watergirl_y_momentum += 0.15
    if watergirl_y_momentum > 3:
        watergirl_y_momentum = 3

    watergirl_rect, watergirl_collisions = move(watergirl_rect,
                                                watergirl_movement,
                                                tile_rects,harmwg)

    if watergirl_collisions['bottom']:
        watergirl_y_momentum = 0
        watergirl_air_timer = 0
    else:
        watergirl_air_timer += 1

    if watergirl_collisions['top']:
        watergirl_y_momentum = 0

    display.blit(fireboy_image, (fireboy_rect.x, fireboy_rect.y))
    display.blit(watergirl_image, (watergirl_rect.x, watergirl_rect.y))
    
    score=round(score)
  #Links with Keyboard 
    for event in pygame.event.get():
        if event.type == QUIT:
            print(score)  
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                fbmoving_right = True
            if event.key == K_LEFT:
                fbmoving_left = True
            if event.key == K_UP:
                if fireboy_air_timer < 10:
                    fireboy_y_momentum = -5
            if event.key == K_d:
                wgmoving_right = True
            if event.key == K_a:
                wgmoving_left = True
            if event.key == K_w:
                if watergirl_air_timer < 10:
                    watergirl_y_momentum = -5
            if event.key ==K_q:
              pygame.mixer.music.fadeout(1000)
            if event.key ==K_e:
              pygame.mixer.music.play(-1)
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                fbmoving_right = False
            if event.key == K_LEFT:
                fbmoving_left = False
            if event.key == K_d:
                wgmoving_right = False
            if event.key == K_a:
                wgmoving_left = False
  
    #Projects everything onto the screen
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)