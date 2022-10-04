#Chirag & Aidan

# Import Libaries 
import pygame, sys
from pygame.locals import *
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
# Creates window for the game
pygame.display.set_caption('   Blazingboy and Aquagirl ')
WINDOW_SIZE = (510, 470)
screen = pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE)

# Colors
white = (255, 255, 255)

#Defining all images used and scales them to fit on screen
fireboy_image = (pygame.image.load('fb.webp').convert_alpha())
watergirl_image = (pygame.image.load('wg.webp').convert_alpha())


brick = pygame.image.load('brick.png').convert_alpha()
lava = pygame.image.load('lava.png').convert_alpha()
water = pygame.image.load('water.png').convert_alpha()
toxic = pygame.image.load('toxic.png').convert_alpha()

blue_gem=pygame.image.load('gem_blue.png').convert_alpha()
red_gem=pygame.image.load('gem_red.png').convert_alpha()

fireboy_door = pygame.image.load('FB_door.png').convert_alpha()
watergirl_door = pygame.image.load('WG_door.png').convert_alpha()

character_size=(int(WINDOW_SIZE[0]*(3/50)), int(WINDOW_SIZE[1]*(3/32)))
fireboy_image = pygame.transform.scale(fireboy_image, character_size)
watergirl_image = pygame.transform.scale(watergirl_image, character_size)

tile_size=(int(WINDOW_SIZE[0]*(8/255)), int(WINDOW_SIZE[1]*(4/235)))
brick = pygame.transform.scale(brick, tile_size)
lava = pygame.transform.scale(lava, tile_size)
water = pygame.transform.scale(water, tile_size)
toxic = pygame.transform.scale(toxic, tile_size)

gem_size=(int(WINDOW_SIZE[0]*(1/51)),int(WINDOW_SIZE[1]*(1/47)))
blue_gem = pygame.transform.scale(blue_gem, gem_size)
red_gem = pygame.transform.scale(red_gem, gem_size)

door_size=(int(WINDOW_SIZE[0]*(14/255)),int(WINDOW_SIZE[1]*(7/94)))
watergirl_door = pygame.transform.scale(watergirl_door, door_size)
fireboy_door = pygame.transform.scale(fireboy_door, door_size)

winner_font = pygame.font.SysFont('calibri', 20)


def load_map(path):
    '''Function to load the map file and split it into list.

    Inputs:
    path: the folder where the map is stored

    Outputs:
    game_map: the map on the screen
    
    '''
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

#Loads map file
game_map = load_map('map')


def collision_test(rect, tiles):
    '''Function to test if one rect collides with another, and return it.

    Imputs:
    rect: an objects rectangle that is going to be checked for collision
    tiles: a set of images used to make the map that is being checked for collison

    Outputs:
    hit_list: a list of tiles an object collides with
    
    '''
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles, kill):
    '''Function that allows characters to move without walking thru walls.

    Inputs:
    rect: the rectangle of the player
    movement: a list of movements for the player
    tiles: a set of images used to make the map that is being checked for collison
    kill: resets the player if it touches a hazard

    Outputs:
    rect: the rect of the player
    collision_types: what the player rect collides with
    
    '''
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


def draw_winner(text):
  '''Function that draw the level completion text.

  Inputs:
  text: words that appear on the screen

  Outputs:
  draw_text: draws the "level complete" text on the screen
  
  '''
  draw_text = winner_font.render(text, 1, white)
  screen.blit(draw_text, (screen.get_width()/2 - draw_text.get_width()/2, screen.get_height()/2 - draw_text.get_height()/2))
  pygame.display.update()
  pygame.time.delay(1000) #In milliseconds 1000 = 1 second. How long until it shows on screen
  
  
#Presets values for fireboy and watergirls movement/jumping
fbmoving_right = False
fbmoving_left = False

wgmoving_right = False
wgmoving_left = False

fireboy_y_momentum = 0
fireboy_air_timer = 0

watergirl_y_momentum = 0
watergirl_air_timer = 0
# Defines the rectangle for fireboy and watergirl
fireboy_rect = pygame.Rect(60, 400, fireboy_image.get_width(),
                           fireboy_image.get_height())

watergirl_rect = pygame.Rect(30, 400, watergirl_image.get_width(),
                             watergirl_image.get_height())


red_gem_rects=[pygame.Rect((int(WINDOW_SIZE[0]*(323/510))),(int(WINDOW_SIZE[1]*(400/470))),red_gem.get_width(),red_gem.get_height()),pygame.Rect((int(WINDOW_SIZE[0]*(115/510))),(int(WINDOW_SIZE[1]*(300/470))),red_gem.get_width(),red_gem.get_height()),pygame.Rect((int(WINDOW_SIZE[0]*(323/510))),(int(WINDOW_SIZE[1]*(220/470))),red_gem.get_width(),red_gem.get_height()),pygame.Rect((int(WINDOW_SIZE[0]*(238/510))),(int(WINDOW_SIZE[1]*(125/470))),red_gem.get_width(),red_gem.get_height()),pygame.Rect((int(WINDOW_SIZE[0]*(337/510))),(int(WINDOW_SIZE[1]*(25/470))),red_gem.get_width(),red_gem.get_height())]
  
blue_gem_rects=[pygame.Rect((int(WINDOW_SIZE[0]*(163/510))),(int(WINDOW_SIZE[1]*(400/470))),blue_gem.get_width(),blue_gem.get_height()),pygame.Rect((int(WINDOW_SIZE[0]*(275/510))),(int(WINDOW_SIZE[1]*(300/470))),blue_gem.get_width(),blue_gem.get_height()),pygame.Rect((int(WINDOW_SIZE[0]*(115/510))),(int(WINDOW_SIZE[1]*(220/470))),blue_gem.get_width(),blue_gem.get_height()),pygame.Rect((int(WINDOW_SIZE[0]*(337/510))),(int(WINDOW_SIZE[1]*(125/470))),blue_gem.get_width(),blue_gem.get_height()),pygame.Rect((int(WINDOW_SIZE[0]*(158/510))),(int(WINDOW_SIZE[1]*(25/470))),blue_gem.get_width(),blue_gem.get_height())]


#Plays the BG Music
pygame.mixer.music.load('music.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

#Sets up score vals
score=7500
score_counter=0
while True:  # game loop
    screen.fill((51, 51, 26))

    score_counter+=1
    score-=((90/score_counter)+1)
    
    tile_rects = []
    harmwg=[]
    harmfb=[]


    # Sets the positions and rectangles for the doors
    fireboy_door_rect = pygame.Rect((int(WINDOW_SIZE[0]*(400/510))), (int(WINDOW_SIZE[1]*(25/470))), fireboy_door.get_width(), fireboy_door.get_height())
  
    watergirl_door_rect = pygame.Rect((int(WINDOW_SIZE[0]*(450/510))), (int(WINDOW_SIZE[1]*(25/470))), watergirl_door.get_width(), watergirl_door.get_height())
    
  #Makes map from the map.txt file
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(brick, (x * tile_size[0], y * tile_size[1]))
            elif tile == '2':
                screen.blit(lava, (x * tile_size[0], y * tile_size[1]))
                harmwg.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))
            elif tile == '3':
                screen.blit(water, (x * tile_size[0], y * tile_size[1]))
                harmfb.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))
            elif tile == '4':
                screen.blit(toxic, (x * tile_size[0], y * tile_size[1]))
                harmfb.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))
                harmwg.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))
            if tile == '1':
                tile_rects.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))

            x += 1
        y += 1

    #Moving Parts: Doors, Elevators, & Buttons
    button1pos=()
    button1=pygame.Rect(336,155,15,5)
    button2=pygame.Rect(236,250,15,5)
    button1draw=pygame.draw.rect(screen,(153,0,153),button1)
    button2draw=pygame.draw.rect(screen,(153,0,153),button2)
    if (collision_test(fireboy_rect,[button1,button2]) != []) or collision_test(watergirl_rect,[button1,button2]) != []:
      elevator=pygame.draw.rect(screen,(0,0,0),pygame.Rect(425,235,70,18))
    else:
      elevator=pygame.draw.rect(screen,(0,0,0),pygame.Rect(425,159,70,18))
    tile_rects.append(elevator)  

    button3=pygame.Rect(336,59,15,5)
    button4=pygame.Rect(156,59,15,5)
    button3draw=pygame.draw.rect(screen,(153,0,153),button3)
    button4draw=pygame.draw.rect(screen,(153,0,153),button4)
    if  (collision_test(fireboy_rect,[button3,button4]) != []) or collision_test(watergirl_rect,[button3,button4]) != []:
      door=pygame.draw.rect(screen,(0,0,0),pygame.Rect(250,-50,10,68))
    else:
      door=pygame.draw.rect(screen,(0,0,0),pygame.Rect(250,0,10,68))
    tile_rects.append(door)

  # Door Collisions 
    if (collision_test(fireboy_rect,[fireboy_door_rect]) != []) and collision_test(watergirl_rect, [watergirl_door_rect]):
      winner_text = f"Level Complete! Score: {round(score)}"
      draw_winner(winner_text)
      break
  
  #Draws Gems
    for gem in red_gem_rects:
      screen.blit(red_gem,(gem[0],gem[1]))
      if collision_test(fireboy_rect,[gem]) !=[]:
        red_gem_rects.remove(gem)
        score+=50
      
    for gem in blue_gem_rects:
      screen.blit(blue_gem,(gem[0],gem[1]))
      if collision_test(watergirl_rect,[gem]) !=[]:
        blue_gem_rects.remove(gem)
        score+=50
        
  # Draws Doors
    for door in fireboy_door_rect:
      screen.blit(fireboy_door, (400, 30))

    for door in watergirl_rect:
      screen.blit(watergirl_door, (450, 30))

        
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

    screen.blit(fireboy_image, (fireboy_rect.x, fireboy_rect.y))
    screen.blit(watergirl_image, (watergirl_rect.x, watergirl_rect.y))
    
    score=round(score)
  #Defines which keys move the characters 
    for event in pygame.event.get():
        if event.type == QUIT:
            print(score)  
            pygame.quit()
            sys.exit()
        if event.type==pygame.VIDEORESIZE:
            screen=pygame.display.set_mode(event.size,pygame.RESIZABLE)

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
    WINDOW_SIZE=(screen.get_width(),screen.get_height())
    pygame.display.update()
    clock.tick(60)