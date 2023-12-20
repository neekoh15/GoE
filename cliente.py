import pygame
from network import Network

class Player:

    def __init__(self, data) -> None:
        self.x, self.y = data['COORDS']
        self.actual_map = data['MAP']

        self.width, self.height = (30, 30)
        self.rect = (self.x, self.y, self.width, self.height)
        self.color = (255, 255, 255)

    def update(self, server_response:tuple[int]):
        """ Update the player status 
        - server_response = (player_x, player_y)"""
        self.x, self.y = server_response['COORDS']
        self.actual_map = server_response['MAP']
        self.rect = (self.x, self.y, self.width, self.height)

class Creature:
    def __init__(self,x ,y) -> None:
        self.x = x
        self.y = y
        self.width, self.height = (30, 30)
        self.rect = (x, y, self.width, self.height)
        self.color = (255, 0, 255)
        self.sprite = ''

    def update(self, server_response:tuple[int]):
        self.x, self.y = server_response['COORDS']
        self.sprite = server_response['SPRITE']
        self.rect = (self.x, self.y, self.width, self.height)


class Client:

    def __init__(self) -> None:
        self.win_size = (600, 600)
        self.width, self.height = self.win_size
        self.init_pygame = pygame.init()
        self.window = pygame.display.set_mode((self.win_size))
        self.clock = pygame.time.Clock()
        self.network = Network()
        self.connected_to_server = False
        self.run = True

        self.visual_data = []
        self.player:Player = None
        self.creatures:dict = None

        self.events = {
            'MOUSE': {
                'LCLICK': False,
                'RCLICK': False,
                'MCLICK': False
            },
            'KEYBOARD': {
                'Q': False,
                'W': False,
                'E': False,
                'R': False
            }
        }

    def connect_to_server(self) -> int:
        """ Connects to the server and retrieve player data """
        try:
            server_response:tuple = self.network.connect()
            self.player = Player(*server_response)
            self.connected_to_server = True
            return 1
        
        except Exception as e:
            print('Failed to connect to the server: ', e)
            return 0


    def catch_keyboard_events(self):
        k_events = pygame.key.get_pressed()
        self.events['KEYBOARD']['Q'] = k_events[pygame.K_q]
        self.events['KEYBOARD']['W'] = k_events[pygame.K_w]
        self.events['KEYBOARD']['E'] = k_events[pygame.K_e]
        self.events['KEYBOARD']['R'] = k_events[pygame.K_r]

    def catch_mouse_events(self):
        m_events = pygame.mouse.get_pressed()
        self.events['MOUSE']['LCLICK'] = m_events[0]
        self.events['MOUSE']['RCLICK'] = m_events[1]
        self.events['MOUSE']['MCLICK'] = m_events[2]

    def update_game(self, server_response:dict):
        player_data:Player = server_response('PLAYER_DATA')
        if player_data:
            self.player.update(player_data)

        creature_data:Creature = server_response.get('CREATURE_DATA')
        if creature_data:
            for cd in creature_data:
                self.creatures[cd.get_id()] = cd

    def draw_game(self):
        """ Draw the game on the screen 
        - Draw map background
        - Draw player
        - Draw Creatures
        """
        # draw map background
        pygame.draw.rect(self.window, (0, 125, 0), (-self.player.x +self.width//2, -self.player.y + self.height//2, 600, 600))
        
        # draw creatures
        for creature in self.creatures.values():
            rel_x = self.width//2 + (creature.x - self.player.x)
            rel_y = self.height//2 + (creature.y - self.player.y)
            pygame.draw.rect(self.window, creature.color, (rel_x, rel_y, creature.width, creature.height))
        
        # draw player
        pygame.draw.rect(self.window, self.player.color, (self.width//2, self.height//2, self.player.width, self.player.height))

    def main(self):

        self.connect_to_server()

        if self.connected_to_server:
            while self.run:
                server_response = self.network.send_data(self.events)
                self.update_game(server_response=server_response)
                self.draw_game()

    

        