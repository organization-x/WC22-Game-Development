import pygame
import sys

clock=pygame.time.Clock()

from pygame.locals import *

import random

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('    World Runner')

WINDOW_SIZE= (600,400)

screen =pygame.display.set_mode(WINDOW_SIZE)

display = pygame.Surface((300,200))

player_image = (pygame.image.load('player_animations/idle/idle1.jpg').convert_alpha())

grass_image = pygame.image.load('map_files/grass.jpg').convert_alpha()
grass_image= pygame.transform.scale(grass_image,(16,16))
TILE_SIZE = grass_image.get_width()
lava_image=pygame.image.load('map_files/lava.png').convert_alpha()
lava_image= pygame.transform.scale(lava_image,(16,16))
plant_image=pygame.image.load('map_files/plant.png').convert_alpha()
plant_image= pygame.transform.scale(plant_image,(16,16))

tile_index={1:grass_image,2:lava_image,3:plant_image}

chunk_size=8

def generate_chunk(x,y):
  chunk_data=[]
  for y_pos in range(chunk_size):
    for x_pos in range(chunk_size):
      target_x=x*chunk_size+x_pos
      target_y=y*chunk_size+y_pos
      tile_type=0
      if target_y >10:
        tile_type=2
      elif target_y==10:
        tile_type=1
        if random.randint(1,5)==2:
          tile_type=0
      elif target_y==9:
        if random.randint(1,5)==1:
          tile_type=3
      if tile_type!=0:
        chunk_data.append([[target_x,target_y],tile_type])
  return chunk_data
   
game_map={}


global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 1
    for frame in frame_durations:
        animation_frame_id = animation_name  + str(n)
        img_loc = path + '/' + animation_frame_id + '.jpg'
        animation_image = pygame.image.load(img_loc).convert_alpha()
        animation_image=pygame.transform.scale(animation_image,(25,30))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        

animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[40,40,40])

grass_sound=pygame.mixer.Sound('grass.wav')
grass_sound.set_volume(0.4)

pygame.mixer.music.load('music.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

player_action='idle'
player_frame=0
player_flip=False

grass_sound_timer=0

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
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
    return rect, collision_types

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

tru_scroll=[0,0]

player_rect = pygame.Rect(50, 0, 12, 25)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


def game_over():
    player_rect.y=0
    player_rect.x=0
  
while True: # game loop
    display.fill((146,244,255))

    if grass_sound_timer>0:
      grass_sound_timer-=1
  
    tru_scroll[0] += (player_rect.x-tru_scroll[0]-146)/20
    tru_scroll[1] += (player_rect.y-tru_scroll[1]-110)/20
    scroll=tru_scroll.copy()
    scroll[0]=int(scroll[0])
    scroll[1]=int(scroll[1])

    pygame.draw.rect(display,(65,80,151),pygame.Rect(0,120,300,80))
    for background_obj in background_objects:
      obj_rect = pygame.Rect(background_obj[1][0]-scroll[0]*background_obj[0],background_obj[1][1]-scroll[1]*background_obj[0],background_obj[1][2],background_obj[1][3])
      if background_obj[0]==0.5:
         pygame.draw.rect(display,(14,222,150),obj_rect)
      else:
         pygame.draw.rect(display,(9,91,85),obj_rect)
  
    tile_rects = []
    for y in range(2):
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

  
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0]!=0:
          if grass_sound_timer==0:
            grass_sound_timer=30
            grass_sound.play()
    else:
        air_timer += 1

    if collisions['top']:
        player_y_momentum = 0

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    if player_rect.y > 145:
      game_over()

    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key ==K_w:
              pygame.mixer.music.fadeout(1000)
            if event.key ==K_e:
              pygame.mixer.music.play(-1)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                  player_y_momentum = -4
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps