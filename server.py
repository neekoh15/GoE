import uuid
import random
import pygame

class Jugador:
    def __init__(self) -> None:
        print('CREATING NEW PLAYER INSTANCE')

        self.__id = uuid.uuid4()
        self.__x = 0
        self.__y = 0
        self.__map_id = 0

        self.__name = None

        self.__hp = None
        self.__mp = None
        self.__stamina = None

        self.__lvl = None
        
        self.__str = None
        self.__dex = None
        self.__vit = None
        self.__luk = None
        self.__mag = None
        self.__int = None
        
        self.__gold = None
        
        self.__velocity = 5

        self.__color = (255, 255, 255)
        self.__w, self.__h = 32, 32
        self.__rect = (self.__color, self.__w, self.__h)
        self.__collision_box = None 

        self.__near_creatures = []
        self.__near_entities = []

        self.__map = Map()
        self.__map_size = self.__map.get_size()

        self.atributes = {
            'ID': self.__id,
            'STATS': {
                'NAME': self.__name,
                'HP': self.__hp,
                'MP': self.__mp,
                'LVL': self.__lvl,
                'STR': self.__str,
                'DEX': self.__dex,
                'VIT': self.__vit,
                'LUK': self.__luk,
                'MAG': self.__mag,
                'INT': self.__int,
                'GOLD': self.__gold,
                'VELOCITY': self.__velocity,
                'STAMINA': self.__stamina,
            },

            'RECT': {
                'COLOR': self.__color,
                'WIDTH': self.__w,
                'HEIGHT': self.__h
            },

            'COORDS': {
                'X': self.__x,
                'Y': self.__y,
                'MAP_ID': self.__map_id,
                'MAP_SIZE': self.__map_size,
                'BACKGROUND_COLOR': (125, 125, 125)
            },

            'CREATURES': self.__near_creatures,
        }

    def update(self, window_size):

        self.__near_creatures = self.get_near_creatures(window_size)
        self.__near_entities = self.__near_creatures

        self.atributes = {
            'ID': self.__id,
            'STATS': {
                'NAME': self.__name,
                'HP': self.__hp,
                'MP': self.__mp,
                'LVL': self.__lvl,
                'STR': self.__str,
                'DEX': self.__dex,
                'VIT': self.__vit,
                'LUK': self.__luk,
                'MAG': self.__mag,
                'INT': self.__int,
                'GOLD': self.__gold,
                'VELOCITY': self.__velocity
            },

            'RECT': {
                'COLOR': self.__color,
                'WIDTH': self.__w,
                'HEIGHT': self.__h
            },

            'COORDS': {
                'X': self.__x,
                'Y': self.__y,
                'MAP_ID': self.__map_id,
                'MAP_SIZE': self.__map_size,
                'BACKGROUND_COLOR': (125, 125, 125)
            },

            'CREATURES': self.__near_creatures,
        }

        self.__map.update()

    def get_near_creatures(self, client_size):

        w,h = client_size
        near_creatures = []
        if self.__map:
            if self.__map.creatures:
                for creature in map.creatures:
                    c_x, c_y = creature.get_coords()
                    c_w, c_h = creature.get_size()
                    if (self.__x - w//2 - c_w < c_x < self.__x +w//2) and (self.__y - h//2 - c_h < c_y < self.__y +h//2):
                        near_creatures.append(creature)

        return near_creatures
    
    def get_rect(self):
        return self.__rect
    
    def get_collision_box(self):
        return self.__collision_box
    
    def get_id(self):
        return self.__id
    
    def analize_collision(self, dx=0, dy=0):
        """ 
        Check for every step of the movement if there is a collision or will be off map limits
        - If not collision found and within map limits, return dx, dy
        - Else return a new dx, dy previous to collision or map boundary
        """
        dir_x = abs(dx)//dx if dx else 0
        dir_y = abs(dy)//dy if dy else 0

        #print(f'{dir_x=},  {dir_y=}')

        delta_x = abs(dx)+1
        delta_y = abs(dy)+1

        collide_x = False
        collide_y = False
        for ent in self.__near_entities:
            col_box = []
            for i in range(delta_x):

                step_x = i * dir_x

                #check for map limits:
                if self.__x + step_x < 0 or self.__x + self.__w > self.__map.map_size[0]:
                    dx = step_x -1*dir_x
                    break
                
                collide_box = pygame.Rect((self.__x + step_x, self.__y, self.__w, self.__h))
                col_box.append((self.__x + step_x, self.__y, self.__w, self.__h))
                collide_x = collide_box.colliderect(ent.get_collision_box())

                within_map_limits_x = 0 <= self.__x + step_x < self.__map.map_size[0]-self.__w
                
                if collide_x or not within_map_limits_x:
                    dx = step_x -1*dir_x
                    break

            for j in range(delta_y):
                step_y = j * dir_y
                collide_box = pygame.Rect((self.__x, self.__y + step_y, self.__w, self.__h))
                collide_y = collide_box.colliderect(ent.get_collision_box())

                within_map_limits_y = 0 <= self.__y + step_y < self.__map.map_size[1]-self.__h

                if collide_y or not within_map_limits_y:
                    dy = step_y -1*dir_y
                    break
            
        return dx, dy

    def move(self, actions=None):
        
        if actions['K_A'] or actions['K_D'] or actions['K_W'] or actions['K_S']:
            dx, dy = 0, 0

            if actions['K_S']:
                dy = 1

            if actions['K_W']:
                dy = -1

            if actions['K_D']:
                dx = 1

            if actions['K_A']:
                dx = -1

            if actions['K_SPRINT']:
                dx *= self.__velocity
                dy *= self.__velocity

            dx, dy = self.analize_collision(dx, dy)

            self.__x += dx
            self.__y += dy

    def handle_actions(self, actions=None, window_size=None):

        self.move(actions=actions)
        self.update(window_size=window_size)


class Creature:
    def __init__(self, map_size) -> None:

        self.__id = uuid.uuid4()
        self.__name = 'Criatura'
        self.__w, self.__h = (25, 25)
        self.__x = random.randint(0, map_size[0] - self.__w)
        self.__y = random.randint(0, map_size[1] - self.__h)
        self.__type = 1

        self.__color = (125, 0, 125)
        self.__mouse_over_color = (125, 0, 255)
        self.__actual_color = self.__color
        
        self.__rect = (self.__x, self.__y, self.__w, self.__h, self.__color)
        self.__collision_box = None #pygame.Rect((self.__x, self.__y, self.__w, self.__h))

        self.atributes = {
            'ID': self.__id,
            'NAME': self.__name,
            'X': self.__x,
            'Y': self.__y,
            'TYPE': self.__type,
            'WIDTH': self.__w,
            'HEIGHT': self.__h,
            'COLOR': self.__color,
            'MOUSE_OVER_COLOR': self.__mouse_over_color,
            'ACTUAL_COLOR': self.__actual_color
        }

    def update(self) -> None:
        self.__rect = (self.__x, self.__y, self.__w, self.__h, self.__actual_color)
        self.__collision_box = pygame.Rect((self.__x, self.__y, self.__w, self.__h))

        self.atributes = {
            'ID': self.__id,
            'NAME': self.__name,
            'X': self.__x,
            'Y': self.__y,
            'TYPE': self.__type,
            'WIDTH': self.__w,
            'HEIGHT': self.__h,
            'COLOR': self.__color,
            'MOUSE_OVER_COLOR': self.__mouse_over_color,
            'ACTUAL_COLOR': self.__actual_color
        }

    def __set_coords(self, x, y):
        self.__x = x
        self.__y = y

    def get_coords(self):
        return self.__x, self.__y
    
    def get_id(self):
        return self.__id

    def get_size(self):
        return self.__w, self.__h
    
    def __set_mouse_over_color(self):
        self.__actual_color = self.__mouse_over_color

    def __reset_color(self):
        self.__actual_color = self.__color

    def get_rect(self):

        return self.__rect

    def get_collision_box(self):
        return self.__collision_box


class Map:

    def __init__(self) -> None:
        self.id = 0
        self.map_size = (500, 500)
        self.creatures = self.create_creatures()

    def create_creatures(self):

        creatures = []

        for _ in range(20):
            c = Creature(self.map_size)
            c.update()
            creatures.append(c)

        return creatures
    
    def get_size(self):
        return self.map_size
    
    def update(self):

        for c in self.creatures:
            c.update()

class Server:
    def __init__(self) -> None:
        self.players_online = {}

    def connect(self):
        player = Jugador()
        id = player.get_id()
        self.players_online[id] = player

        return id

    def recieve_player_data(self, player_data):
        
        id, actions, window_size = player_data

        #print(actions)
        #print(map.creatures)
        player_instance:Jugador = self.players_online[id]

        player_instance.handle_actions(actions=actions, window_size=window_size)

        return player_instance.atributes
            

map = Map()
server = Server()