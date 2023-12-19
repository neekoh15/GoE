""" Client side of application"""
import pygame
from server import server

class Client_Player:
    def __init__(self):
        self.id = None

        self.name = None
        
        self.hp = None
        self.mp = None
        self.stamina = None

        self.lvl = None
        
        self.str = None
        self.dex = None
        self.int = None
        self.mag = None
        self.vit = None

        self.gold = None
        
        self.velocity = None

        self.rect = None
        self.color = None
        self.width = None
        self.height = None

        self.x = None
        self.y = None
        self.map_id = None
        self.map_background = None
        self.map_size = None

        self.creatures = {}
        self.entities = {}

        self.atributes = {
            'ID': None,
            'STATS': {
                'NAME': None,
                'HP': None,
                'MP': None,
                'LVL': None,
                'STR': None,
                'DEX': None,
                'VIT': None,
                'LUK': None,
                'MAG': None,
                'INT': None,
                'GOLD': None,
                'VELOCITY': None
            },

            'RECT': {
                'COLOR': None,
                'WIDTH': None,
                'HEIGHT': None,
            },

            'COORDS': {
                'X': None,
                'Y': None,
                'MAP_ID': None,
                'BACKGROUND_COLOR': None
            },

            'CREATURES': None,
        }

    def update(self, atributes:dict[dict]):
        self.id = atributes.get('ID')

        self.name = atributes.get('STATS').get('NAME')
        
        self.hp = atributes.get('STATS').get('HP')
        self.mp = atributes.get('STATS').get('MP')
        self.stamina = atributes.get('STATS').get('STAMINA')

        self.lvl = atributes.get('STATS').get('LVL')
        
        self.str = atributes.get('STATS').get('STR')
        self.dex = atributes.get('STATS').get('DEX')
        self.int = atributes.get('STATS').get('INT')
        self.mag = atributes.get('STATS').get('MAG')
        self.vit = atributes.get('STATS').get('VIT')

        self.gold = atributes.get('STATS').get('GOLD')
        
        self.velocity = atributes.get('STATS').get('VELOCITY')

        #self.creatures = atributes.get('CREATURES') #pendiente de chequeo
        creatures = atributes.get('CREATURES')

        for c in creatures:
            self.creatures[c.get_id()] = c

        for c in self.creatures:
            if c.get_id() not in creatures:
                self.creatures.pop(c.get_id(), None)
                
        """for atribute in creatures_atributes:
            if not self.creatures.get(atribute['ID']):
                c = Client_Creature(atribute)
                self.creatures[atribute['ID']] = c
            if atribute not in [c.atribute for c in self.creatures.values()]:
                pass"""

        self.entities = self.creatures

        self.color = atributes.get('RECT').get('COLOR')
        self.width = atributes.get('RECT').get('WIDTH')
        self.height = atributes.get('RECT').get('HEIGHT')
        self.rect = (self.color, self.width, self.height)

        self.x = atributes.get('COORDS').get('X')
        self.y = atributes.get('COORDS').get('Y')
        self.map_id = atributes.get('COORDS').get('MAP_ID')
        self.map_background = atributes.get('COORDS').get('BACKGROUND_COLOR')
        self.map_size = atributes.get('COORDS').get('MAP_SIZE')

        self.rect = (self.color, self.width, self.height)

        #print(self.__dir__())

"""class Client_Creature:
    
    def __init__(self, atributes:dict):
        #print('- CREATING NEW CREATURE -')
        self.id = None
        self.x = None
        self.y = None
        self.color = (125, 0, 125)
        self.mouse_over_color = (0, 0, 125)
        self.actual_color = self.color
        self.width = None
        self.height = None
        self.rect = None
        self.type = None

        self.update(atributes)

    def update(self, atributes):

        self.id = atributes.get('ID')
        self.x = atributes.get('X')
        self.y = atributes.get('Y')

        self.width = atributes.get('WIDTH')
        self.height = atributes.get('HEIGHT')
        self.type = atributes.get('TYPE')

        self.rect = (self.x, self.y, self.width, self.height, self.actual_color)

        self.collison_box = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_rect(self):
        return self.rect
    
    def get_collision_box(self):
        return self.collison_box

    def reset_color(self):
        self.actual_color = self.color

    def set_mouse_over_color(self):
        self.actual_color = self.mouse_over_color"""


class Network:
    def __init__(self):
        self.server = server
        self.connection = False

    def connect_to_server(self):
        self.connection = True
        new_player_id_instance = self.server.connect()
        return new_player_id_instance

    def request(self, data):
        if self.connection:
            response = server.recieve_player_data(data)
            return response
        else:
            return None
        

class Client:
    def __init__(self):
        pygame.init()
        self.network = Network()
        self.client_size = (600, 600)
        self.w, self.h = self.client_size
        self.window = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.player = Client_Player()
        self.connection = False

        self.client_actions= {
            'K_W': False,
            'K_S': False,
            'K_A': False,
            'K_D': False,
            'K_SPRINT': False,
            'MOUSE_OVER': None,
            'MOUSE_CLICK': None,
            'ATTACK_MODE': False,
            'TARGET': None,
            'SKILL_TARGET': None,
            'USE_ATTACK': False,    # TRIGGER ATTACK ANIMATION
            'USE_SKILL': None,      # TRIGGER SKILL ANIMATION
        }

    def reset(self):
        self.client_actions= {
            'K_W': False,
            'K_S': False,
            'K_A': False,
            'K_D': False,
            'SKILL': False,
            'K_SPRINT': False,
        }

    def connect_to_server(self):
        #try:
        self.player.id = self.network.connect_to_server()
        self.connection = True
        #except Exception as e:
        #    print(e)

    def get_keyboard_events(self):
        
        keyboard_event = pygame.key.get_pressed()

        if keyboard_event[pygame.K_w]:
            self.client_actions['K_W'] = True

        if keyboard_event[pygame.K_s]:
            self.client_actions['K_S'] = True

        if keyboard_event[pygame.K_a]:
            self.client_actions['K_A'] = True

        if keyboard_event[pygame.K_d]:
            self.client_actions['K_D'] = True

        if keyboard_event[pygame.K_LSHIFT]:
            self.client_actions['K_SPRINT'] = True

    def get_mouse_events(self):
        mouse_click_events = pygame.mouse.get_pressed()
        x,y = pygame.mouse.get_pos()

        # fix mouse relative position to player and not to the screen
        rel_x = x - (self.w//2 - self.player.x)
        rel_y = y - (self.h//2 - self.player.y)
        cursor = pygame.Rect(rel_x, rel_y, 1, 1)
        pre_target = None

        for ent in self.player.entities:
        
            collision = cursor.colliderect(ent.get_collision_box())

            if collision:
                print('mouse over creature: ', ent.get_id())

        if mouse_click_events[0]:

            if rel_x >= 0 and rel_y >= 0:
                print(f'valid mouse click at ({rel_x, rel_y})')

        

    def draw_game(self):
        player = self.player

        rel_bg_x = None
        rel_bg_y = None
        pygame.draw.rect(self.window, player.map_background, (-player.x + self.w//2, -player.y + self.h//2, *player.map_size))

        if player.creatures:
            for c in player.creatures:
                c_x, c_y, c_w, c_h, c_color = c.get_rect()
                rel_x = self.w//2 + (c_x - self.player.x)
                rel_y = self.h//2 + (c_y - self.player.y)
                pygame.draw.rect(self.window, c_color, (rel_x, rel_y, c_w, c_h))

        p_color, p_w, p_h = player.rect

        pygame.draw.rect(self.window, p_color, (self.w//2 , self.h//2, p_w, p_h))

    def handle_pygame_events(self):
        events = pygame.event.get()

        if pygame.QUIT in [e.type for e in events]:
            pygame.quit()
            exit(0)

    def update(self, server_response):
        self.player.update(server_response)

    def main_loop(self):
        self.connect_to_server()

        server_response = self.network.request((self.player.id, self.client_actions, self.client_size))
        self.player.update(server_response)

        if self.connection:
            while True:
                self.handle_pygame_events()
                self.get_keyboard_events()
                self.get_mouse_events()

                self.window.fill((0,0,0))

                server_response = self.network.request((self.player.id, self.client_actions, self.client_size))
                
                self.update(server_response)

                
                #print(self.player.atributes['COORDS'])
                #print(self.player.atributes['CREATURES'])
                
                self.draw_game()
                self.reset()
                self.clock.tick(30)

                pygame.display.update()
                
            
if __name__ == "__main__":
    cliente = Client()
    cliente.main_loop()


    
