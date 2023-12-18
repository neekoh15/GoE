import uuid
import random

class Jugador:
    def __init__(self) -> None:
        print('CREATING NEW PLAYER INSTANCE')

        self.id = uuid.uuid4()
        self.x = 0
        self.y = 0
        self.map_id = 0

        self.name = None
        self.hp = None
        self.mp = None
        self.lvl = None
        self.str = None
        self.dex = None
        self.vit = None
        self.luk = None
        self.mag = None
        self.int = None
        self.gold = None

        self.map = Map()

        self.atributes = {
            'ID': self.id,
            'STATS': {
                'NAME': self.name,
                'HP': self.hp,
                'MP': self.mp,
                'LVL': self.lvl,
                'STR': self.str,
                'DEX': self.dex,
                'VIT': self.vit,
                'LUK': self.luk,
                'MAG': self.mag,
                'INT': self.int,
                'GOLD': self.gold
            },

            'COORDS': {
                'x': self.x,
                'y': self.y,
                'map_id': self.map_id,
            },
            
            'RECT': {
                'color': (255, 255, 255),
                'w': 32,
                'h': 32
            },

            'CREATURES': []
        }

    def update(self, window_size):

        self.atributes = {
            'ID': self.id,
            'STATS': {
                'NAME': self.name,
                'HP': self.hp,
                'MP': self.mp,
                'LVL': self.lvl,
                'STR': self.str,
                'DEX': self.dex,
                'VIT': self.vit,
                'LUK': self.luk,
                'MAG': self.mag,
                'INT': self.int,
                'GOLD': self.gold
            },

            'COORDS': {
                'x': self.x,
                'y': self.y,
                'map_id': self.map_id,
            },
            
            'RECT': {
                'color': (255, 255, 255),
                'w': 32,
                'h': 32
            },

            'CREATURES': self.get_near_creatures(window_size)
        }

    def get_near_creatures(self, client_size):

        w,h = client_size
        near_creatures = []
        if self.map:
            if self.map.creatures:
                for creature in map.creatures:
                    if (self.x - w//2 < creature.x < self.x +w//2) and (self.y - h//2 < creature.y < self.y +h//2):
                        near_creatures.append(creature)

        return near_creatures
    
    def move(self, actions=None):
        
        if actions['K_DOWN'] or actions['K_UP'] or actions['K_LEFT'] or actions['K_RIGHT']:
            if actions['K_DOWN']:
                self.y += 1

            if actions['K_UP']:
                self.y -= 1

            if actions['K_RIGHT']:
                self.x += 1

            if actions['K_LEFT']:
                self.x -= 1

    def handle_actions(self, actions=None, window_size=None):

        self.move(actions=actions)
        self.update(window_size=window_size)


class Creature:
    def __init__(self) -> None:
        
        self.x = None
        self.y = None
        self.color = (125, 0, 125)
        self.w, self.h = (25, 25)



class Map:

    def __init__(self) -> None:
        self.id = 0
        self.map_size = (500, 500)
        self.creatures = self.create_creatures()

    def create_creatures(self):

        creatures = []

        for _ in range(20):
            c = Creature()

            c.x = random.randint(0, self.map_size[0] - c.w)
            c.y = random.randint(0, self.map_size[1] - c.h)
            creatures.append(c)

        return creatures

class Server:
    def __init__(self) -> None:
        self.players_online = {}

    def connect(self):
        player = Jugador()
        self.players_online[player.id] = player

        return player.id

    def recieve_player_data(self, player_data):
        
        id, actions, window_size = player_data

        print(actions)
        #print(map.creatures)
        player_instance:Jugador = self.players_online[id]

        player_instance.handle_actions(actions=actions, window_size=window_size)

        return player_instance.atributes
            

map = Map()
server = Server()