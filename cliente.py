""" Client side of application"""
import pygame
from server import server

class Client_Player:
    def __init__(self):
        self.id = None
        self.atributes = None

            
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
            'K_UP': False,
            'K_DOWN': False,
            'K_LEFT': False,
            'K_RIGHT': False
        }

    def reset(self):
        self.client_actions= {
            'K_UP': False,
            'K_DOWN': False,
            'K_LEFT': False,
            'K_RIGHT': False
        }

    def connect_to_server(self):
        #try:
        self.player.id = self.network.connect_to_server()
        self.connection = True
        #except Exception as e:
        #    print(e)

    def get_movement_events(self):
        
        key_presseds = pygame.key.get_pressed()

        if key_presseds[pygame.K_UP]:
            self.client_actions['K_UP'] = True

        if key_presseds[pygame.K_DOWN]:
            self.client_actions['K_DOWN'] = True

        if key_presseds[pygame.K_LEFT]:
            self.client_actions['K_LEFT'] = True

        if key_presseds[pygame.K_RIGHT]:
            self.client_actions['K_RIGHT'] = True

    def draw_game(self):
        player = self.player

        if player.atributes['CREATURES']:
            for c in player.atributes['CREATURES']:
                rel_x = self.w//2 + (c.x - self.player.atributes['COORDS']['x'])
                rel_y = self.h//2 + (c.y - self.player.atributes['COORDS']['y'])
                pygame.draw.rect(self.window, c.color, (rel_x, rel_y, c.w, c.h))

        p_color = self.player.atributes['RECT']['color']
        p_w = self.player.atributes['RECT']['w']
        p_h = self.player.atributes['RECT']['h']

        pygame.draw.rect(self.window, p_color, (self.w//2 , self.h//2, p_w, p_h))

    def handle_pygame_events(self):
        events = pygame.event.get()

        if pygame.QUIT in [e.type for e in events]:
            pygame.quit()
            exit(0)


    def main_loop(self):
        self.connect_to_server()

        if self.connection:
            while True:
                self.handle_pygame_events()
                self.get_movement_events()

                self.window.fill((0,0,0))

                server_response = self.network.request((self.player.id, self.client_actions, self.client_size))
                self.player.atributes = server_response
                
                print(self.player.atributes['COORDS'])
                #print(self.player.atributes['CREATURES'])
                
                self.draw_game()
                self.reset()
                self.clock.tick(30)

                pygame.display.update()
                
            
if __name__ == "__main__":
    cliente = Client()
    cliente.main_loop()


    
