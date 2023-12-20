import random

class Server:
    def __init__(self) -> None:
        self.online_players = []
        self.dummy_player = None
        self.maps = {
            'map1': [Dummy_Creature(map_size=(600,600)).get_data()]
        }

    def connect(self):
        """ Stablish conection with the server
        - Returns player data
        """
        self.dummy_player = Dummy_Player()
        self.online_players.append(self.dummy_player)

        return self.dummy_player.data
    
    def recieve(self, events):
        self.dummy_player.update_status(events=events)
        player_data = self.dummy_player.data
        creatures = self.maps[self.dummy_player.get_actual_map()]

        return {
            'PLAYER_DATA': player_data,
            'CREATURE_DATA': creatures,
        }
    
class Dummy_Player:
    def __init__(self) -> None:
        self.__x = 0
        self.__y = 0
        self.__actual_map = 'map1'

        self.data = {
            'COORDS': (self.__x, self.__y),
            'MAP': self.__actual_map
        }

    def get_coords(self):
        return (self.__x, self.__y)
    
    def get_actual_map(self):
        return self.__actual_map

    def update_status(self, events):
        mouse_events = events.get['MOUSE']
        keyboards_events = events.get['KEYBOARD']
        return self.data

class Dummy_Creature:
    def __init__(self, map_size) -> None:
        self.__id = 'CREATURE_ID_123'
        self.__x = random.randint(0, map_size[0])
        self.__y = random.randint(0, map_size[1])
        self.__sprite = 'dummy_sprite.png'

        self.__data = {
            'SPRITE': self.__sprite,
            'COORDS': (self.__x, self.__y),
            'ID': self.__id
        }

    def get_data(self):
        return self.__data

    def get_coords(self):
        return (self.__x, self.__y)

    def get_id(self):
        return self.__id

server = Server()
