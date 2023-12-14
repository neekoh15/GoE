import pygame
from maps import map1

class Player:
    def __init__(self, coords:tuple, actual_map_id:int, name:str, default=False) -> None:
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.actual_map_id = actual_map_id
        self.name = name
        self.default_player= default
        self.rect = None
        self.color = (255, 255, 255)
        self.width = 20
        self.height = 20

    def update_rect(self, screen:pygame.surface.Surface):
        w, h = screen.get_width(), screen.get_height()
        #center the player on the screen
        self.rect = (w//2, h//2, self.width, self.height)

    def get_actual_map_id(self):
        return self.actual_map_id
    
    def set_actual_map(self, actual_map_id):
        self.actual_map_id = actual_map_id

    def update(self):
        pass

    def draw(self, screen:pygame.display):
        self.update_rect(screen)

        pygame.draw.rect(screen, self.color, self.rect)


    def __repr__(self) -> str:
        return f'{self.default_player=}\n{self.coords=}\n{self.actual_map_id=}\n{self.name=}\n{self.x=}\n{self.y=}'
        
class Map_Manager:
    def __init__(self) -> None:
        self.maps = [map1]
        self.maps_dict = {m.id:m for m in self.maps}
        self.actual_map = None

        self.actual_map_event = None


    def get_map(self, id):
        return self.maps_dict.get(id)
    
    def set_player_actual_map(self, destination_map_id:int):
        self.actual_map = self.maps_dict.get(destination_map_id)
    
    def update(self) -> None:
        for maps in self.maps:
            maps.update()

        
        if self.actual_map.get_event() == 1:
            print('evento cambio de mapa!')
            new_destination_map_id = self.actual_map.new_destination_map_id

            self.actual_map = self.get_map(new_destination_map_id)


    def assign_player_to_map(self, map_to_assign, player):

        map_to_assign.set_player(player)

    def return_player_current_map(self, player:Player):

        player_current_map = self.get_map(player.actual_map_id)

        return player_current_map
    


class Game:
    def __init__(self, WIN_SIZE, FPS) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(WIN_SIZE)

        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.map_manager = None
        self.player = None
        self.current_map = None

        self.exit_game = False
        self.reset = False

    def init_map_manager(self):
        """ Inicializa el manejador de mapas """
        print('INICIALIZANDO MANEJADOR DE MAPAS')
        self.map_manager = Map_Manager()
        self.current_map = self.map_manager.return_player_current_map(self.player)

        self.map_manager.set_player_actual_map(self.player.actual_map_id)
        self.map_manager.assign_player_to_map(self.current_map, self.player)

        print(f'Manejador de mapas iniciado correctamente: {self.map_manager.actual_map}\n{self.current_map=}\n{self.current_map.player=}')

    def init_player(self):
        """ Carga la inforamacion previa de un jugador, o crea un nuevo jugador por default """

        print('INICIALIZANDO JUGADOR')
        import json
        import os

        player_data_path = 'player_stats.json'

        player_data_exist = os.path.exists(player_data_path)

        if player_data_exist:
            try:
                #raise Exception('Testing error: player_data_exist and could not load')

                with open('player_stats.json', 'r') as json_file:
                    player_data = json.load(json_file)

                    print('\n -> Player data loaded successfully\n')

                    self.player = Player(
                        coords=tuple(player_data['coords'].values()),
                        actual_map_id=player_data['actual_map_id'],
                        name= player_data['name']
                    )


            except Exception as e:
                with open('logs.txt', 'a') as log_file:
                    log_file.writelines(str(e) + '\n')

                print('Error parsing player stats: ', e)
                print('Creating new default player')
            
        else:
            print('No data found for player')
            print('Creating new default player')

        self.player = Player(
                    coords=(0,0),
                    actual_map_id=0,
                    name= 'Default Name',
                    default=True
                )
    
    def set_fps(self, fps):
        self.fps = fps

    def update_game(self):

        self.player.update()
        self.map_manager.update()

        if self.current_map is not self.map_manager.actual_map:
            # flag - el usuario cambio de mapa
            print(' El jugador cambio de mapa')
            self.current_map = self.map_manager.actual_map

    def draw_game(self):
        self.current_map.draw(self.screen, self.player.coords)
        self.player.draw(self.screen)

    def reset_game(self):
        self.run_game()

    def run_game(self):

        # Incializar al jugador
        self.init_player()

        # Inicializar al manejador de mapas
        self.init_map_manager()

        while not self.exit_game:

            self.screen.fill((0,0,0))

            events = pygame.event.get()
            if pygame.QUIT in [e.type for e in events]:
                pygame.quit()
                exit(0)

            self.update_game()

            self.draw_game()

            self.clock.tick(self.fps)

            pygame.display.update()
       


if __name__ == "__main__":

    WIN_SIZE = 700, 700
    FPS = 20
    game = Game(WIN_SIZE=WIN_SIZE, FPS=FPS)
    game.run_game()
