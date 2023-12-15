import pygame

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
        self.actual_map_size = None
        self.nearby_objects = None
        self.nearby_creatures = None
        self.vision_radius = 200

    def update_rect(self, screen:pygame.surface.Surface):
        w, h = screen.get_width(), screen.get_height()
        #center the player on the screen
        self.rect = (w//2, h//2, self.width, self.height)

    def set_coords(self, coords):
        self.x, self.y = coords
        self.coords = coords 

    def get_actual_map_id(self):
        return self.actual_map_id
    
    def set_actual_map(self, actual_map_id, actual_map_size):
        self.actual_map_id = actual_map_id
        self.actual_map_size = actual_map_size
        

    def update(self):
        self.move()

        self.coords = (self.x, self.y)
        """ Update de timers y cooldowns (todavia no implementado)"""
        pass

    def draw(self, screen:pygame.surface.Surface):
        self.update_rect(screen)

        pygame.draw.rect(screen, self.color, self.rect)

    def try_to_move(self, dx=0, dy=0):
        #print('TRY TO MOVE!')
        new_pos_x = self.x + dx
        new_pos_y = self.y + dy

        if not 0 <= new_pos_x < self.actual_map_size[0] - self.width:
            new_pos_x = self.x
        
        if not 0 <= new_pos_y < self.actual_map_size[1] - self.height:
            new_pos_y = self.y

        #print(f'TRYNG TO MOVE {new_pos_x=},{new_pos_y=}')

        return (new_pos_x, new_pos_y)
    
    def move(self):
        dx,dy = 0,0

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP]:
            dy = -1

        if keys_pressed[pygame.K_DOWN]:
            dy = 1

        if keys_pressed[pygame.K_LEFT]:
            dx = -1

        if keys_pressed[pygame.K_RIGHT]:
            dx = 1

        self.x, self.y = self.try_to_move(dx, dy)


    def __repr__(self) -> str:
        return f'{self.default_player=}\n{self.coords=}\n{self.actual_map_id=}\n{self.name=}\n{self.x=}\n{self.y=}'
      
