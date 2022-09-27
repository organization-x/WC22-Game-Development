#World Runner

# CONTROLS:
# Right Arrow - Move Right
# Left Arrow - Move Left
# Up Arrow - Jump
# W - Music Fades Out
# E - Music Fades In/Music Restarts

#IMPORTS & PREINITS:

import pygame, sys, os
from pygame.locals import *
import random

clock=pygame.time.Clock() #Keeps track of time in the game, important for FPS

pygame.mixer.pre_init(44100, -16, 2, 2048) #Pre-inits sound mixer so there is no delay in sound effects/music
pygame.init()

pygame.display.set_caption('    World Runner')

WINDOW_SIZE= (600,400) #In pixels

screen =pygame.display.set_mode(WINDOW_SIZE)

display = pygame.Surface((300,200))

#GAME FUNCTIONS:

def generate_chunk(x,y):
  """
  Randomly generates chunks within view of the player.

  Inputs:
  x: int x location of desired chunk generation
  y: int y location of desired chunk generation

  Outputs:
  chunk_data: list of tiles for generated chunk
  """
  
  chunk_data=[]
  for y_pos in range(chunk_size):
    for x_pos in range(chunk_size):
      target_x=x*chunk_size+x_pos
      target_y=y*chunk_size+y_pos
      tile_type=0
      if target_y >10: #Makes it lava below set y-val
        tile_type=2
      elif target_y==10: #Makes it grass at set y-val
        tile_type=1
        if random.randint(1,5)==2: #Randomly generates holes in the ground
          tile_type=0
      elif target_y==9: #Randomly generates grass
        if random.randint(1,5)==1:
          tile_type=3
      if tile_type!=0: #Appends all tiles that were just generated
        chunk_data.append([[target_x,target_y],tile_type])
  return chunk_data

def load_animation(path,frame_durations):
    """
    Readies the correct animation(s) based on input.

    Inputs:
    path: str of the folder location where the animation is stored
    frame_durations: int of how many frames each img of animation should be

    Outputs:
    animation_frame_data: list of the paths of each frame animation
    """
  
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 1
    for frame in frame_durations: #Creates path for each frame in the animation
        animation_frame_id = animation_name  + str(n)
        img_loc = path + '/' + animation_frame_id + '.jpg'
        animation_image = pygame.image.load(img_loc).convert_alpha()
        animation_image=pygame.transform.scale(animation_image,(25,30))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame): #Adds the frame to master list
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    """
    Switches player action animation (ex. running to idle)

    Inputs:
    action_var: str of current action
    frame: int of what frame of the animation is current playing
    new_value: str of desired new action
      
    Outputs:
    action_var: str of desired new action
    frame: int of what frame of the animation to be on (autoresets to 0 when action changes)
    
    """
    if action_var != new_value: #Switches old action to new
        action_var = new_value
        frame = 0
    return action_var,frame
        
def collision_check(rect, tiles):
    """
    Checks if a rect (which is just the player in this game) collides with any tiles

    Inputs:
    rect: pygame Rect object that should be checked for collisions 
    tiles: list of Rect objects to be checked for collision 

    Outputs:
    hit_list: list of tiles in the input tiles, that the input rect had collided with.
    """
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile): #If the rects collided, add the tile to hit_list
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    """
    Allows for character movement

    Inputs:
    rect: pygame Rect object of the player rect
    movement: List of desired movement ([x,y])
    tiles: List of tiles (Rects) to check with for collision
    
    Outputs:
    rect: pygame Rect object with the new location of the player rect
    collision_types: Dictionary of what type of collision the player had (top, bottom, etc.)
    """
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_check(rect, tiles)
    for tile in hit_list: #Checking for hz. (right/left) collisions 
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_check(rect, tiles)
    for tile in hit_list: #Checking for vt. (top/bottom) collisions
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def game_over():
    """
    Resets player position to (0,0) when they die.

    No I/O
    """
    player_rect.y=0 #Resets player pos.
    player_rect.x=0
  

#CONSTANTS & VARIABLE CREATION:

player_image = (pygame.image.load('player_animations/idle/idle1.jpg').convert_alpha())

#Loads imgs for each tile
grass_image = pygame.image.load('map_files/grass.jpg').convert_alpha() 
grass_image= pygame.transform.scale(grass_image,(16,16))
TILE_SIZE = grass_image.get_width()
lava_image=pygame.image.load('map_files/lava.png').convert_alpha()
lava_image= pygame.transform.scale(lava_image,(16,16))
plant_image=pygame.image.load('map_files/plant.png').convert_alpha()
plant_image= pygame.transform.scale(plant_image,(16,16))

tile_index={1:grass_image,2:lava_image,3:plant_image}

chunk_size=8

game_map={} #Dict for all currently loaded tiles and tiles that have been loaded in the past. 

animation_frames = {} #Dict of which animation frames to cycle thru

animation_database = {} #Dict of all animation frames

animation_database['run'] = load_animation('player_animations/run',[7,7]) #Sets animation frames and durations for run action
animation_database['idle'] = load_animation('player_animations/idle',[40,40,40]) #Sets animation frames and durations for idle action

#Initializes the music and sound effects
grass_sound=pygame.mixer.Sound('grass.wav')
grass_sound.set_volume(0.4)
pygame.mixer.music.load('music.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

player_action='idle' #Default player action is idle
player_frame=0
player_flip=False

grass_sound_timer=0 

moving_right = False
moving_left = False

#Variable for vt. movement and time in air
player_y_momentum = 0
air_timer = 0

tru_scroll=[0,0]

player_rect = pygame.Rect(50, 0, 12, 25)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]] #List of speed, position, and size of each building in the background

#MAIN GAME LOOP:

while True: 
    display.fill((146,244,255)) #Makes background sky blue

    if grass_sound_timer>0: #Makes sure grass sound doesn't play for too long
      grass_sound_timer-=1
  
    tru_scroll[0] += (player_rect.x-tru_scroll[0]-146)/20 #Decides what the player sees based on location
    tru_scroll[1] += (player_rect.y-tru_scroll[1]-110)/20
    scroll=tru_scroll.copy()
    scroll[0]=int(scroll[0])
    scroll[1]=int(scroll[1])

    pygame.draw.rect(display,(65,80,151),pygame.Rect(0,120,300,80)) #Makes the background with buildings
    for background_obj in background_objects:
      obj_rect = pygame.Rect(background_obj[1][0]-scroll[0]*background_obj[0],background_obj[1][1]-scroll[1]*background_obj[0],background_obj[1][2],background_obj[1][3])
      if background_obj[0]==0.5:
         pygame.draw.rect(display,(14,222,150),obj_rect)
      else:
         pygame.draw.rect(display,(9,91,85),obj_rect)
  
    tile_rects = []
    for y in range(2): #Inf. World Generation in chunks:
      for x in range(3):
        target_x=x+int(round(scroll[0]/(chunk_size*16)))
        target_y=y+int(round(scroll[1]/(chunk_size*16)))
        target_chunk=str(target_x)+';'+str(target_y)
        if target_chunk not in game_map:
          game_map[target_chunk]= generate_chunk(target_x,target_y)
        for tile in game_map[target_chunk]:
          display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
          if tile[1] in [1,2]:
            tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))

  
    player_movement = [0, 0] #Sets up movement
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    #If player x isn't moving they are idle, otherwise they are running
    if player_movement[0] == 0: 
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0: #Flips player img if running opposite direction
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom']: #Checks if player is on ground
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0]!=0:
          if grass_sound_timer==0:#Plays grass running effect
            grass_sound_timer=30
            grass_sound.play()
    else:
        air_timer += 1

    if collisions['top']: #Resets vt. velocity when the player jumps and hits something above it.
        player_y_momentum = 0

    player_frame += 1
    if player_frame >= len(animation_database[player_action]): #Cycles thru player animations
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1])) #Displays character (flipped if running left)

    if player_rect.y > 145: #If the player falls below y=145, they are tp'ed back to start
      game_over()

    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN: #Checks if keys are pressed down
            if event.key ==K_w:
              pygame.mixer.music.fadeout(1000)
            if event.key ==K_e:
              pygame.mixer.music.play(-1)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6: #Player starts to decrease in vertical vel. and eventually fall after 6 frames of positive vertical vel.
                  player_y_momentum = -4
        if event.type == KEYUP: #Checks if keys are released
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0)) #Displays everything to screen
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps