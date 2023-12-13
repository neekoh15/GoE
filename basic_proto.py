import pygame

class Map_Manager:
    def __init__(self) -> None:
        self.maps = [map1, map2]
        self.maps_dict = {m.id:m for m in self.maps}

    def get_map(self, id):
        return self.maps_dict.get(id)
    

class Map:
    def __init__(self, id) -> None:
        self.id = id

    def __repr__(self) -> str:
        return f'Map id: {self.id}'
    
class Game:
    def __init__(self, W, H) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((W,H))
        self.clock = pygame.time.Clock()

        self.map_manager = Map_Manager()



if __name__ == "__main__":
    map1 = Map(id=1)
    map2 = Map(id=2)

    m = Map_Manager()

    print(m.get_map(2))