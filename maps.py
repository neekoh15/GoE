import pygame
import random

class Map:
    def __init__(self, id) -> None:

        self.id = id
        self.event = 0
        self.maps_connected = []
        self.portals = []
        self.new_destination_map_id = None
        self.new_destination_coords = None
        self.spawn_coords = None

        self.player = []
        self.creatures = []
        self.objects = []
        self.resources = []

        self.fixed_map_size = (500, 500)
        self.background_color = None
        self.corner_color = None
        self.corner_size = (20, 20)

        self.all_entities = self.player + self.creatures + self.objects + self.resources

    def reset_stats(self):
        self.set_event(0)
        self.new_destination_map_id = None
        self.new_destination_coords = None
        self.spawn_coords = None

    def add_new_portal(self, id:int, portal_coords:tuple, destination_id:int, destination_coords:tuple, available=True):
        """ 
        Crea un nuevo portal hacia un nuevo destino

        - portal_coords: list[tuple, tuple] -> rect coords (x1, y1, x2, y2)\n
            Define una seccion rectangular donde se producira el evento de cambio de mapa o destino

        - destination_id: int -> id del destino a donde se quiere redirigir el jugador
        """

        self.portals.append({
            'id': id,
            'destination_id': destination_id,
            'destination_coords': destination_coords,
            'rect': portal_coords,
            'available': available
        })

        print('NUEVO PORTAL ANIADIDO')

    def enable_portal(self, available_state, portal_id):
        """ 
        Actualiza el estado del portal
        - available_state -> bool
            Setea la disponibilidad del portal (si el player puede cambiar de destino o no)
        - portal_destination_id -> int
            
        """
        for portal in self.portals:
            if portal['id'] == portal_id:
                portal['available'] = available_state

    def create_creatures(self, creature, ammount):
        for _ in range(ammount):
            c = creature
            c.x, c.y = random.randint(0, self.fixed_map_size[0] - c.width), random.randint(0, self.fixed_map_size - c.height)
            self.creatures.append(creature)

    def create_resources(self, resource, ammount):
        for _ in range(ammount):
            self.resources.append(resource)

    def get_player_nearest_creatures(self):

        nearest_creatures = []

        for other_creature in self.creatures:

            distance_x = (self.player.x - other_creature.x)**2
            distance_y = (self.player.y - other_creature.y)**2
            mod_distance = (distance_x + distance_y)**0.5

            if mod_distance <= self.player.vision_radius:
                nearest_creatures.append(other_creature)

        return nearest_creatures

    def get_nearest_entities(self):
        pass

    def set_player(self, player):
        self.player = player

    def set_event(self, event):
        """ 
        Cambia el estado de evento del mapa
        
        - Ningun evento -> 0
        - Cambio de mapa -> 1
        """

        self.event = event

    def get_event(self):
        """ Devuelve los eventos ocurridos en el mapa:
            - 1 -> Cambio de mapa
            - 0 -> Ningun evento
        """
        return self.event    

    def update_events(self):
        """ 
        Actualiza el valor de evento de mapa en base a la posicion del jugador
        Eventos del mapa:
        - 1 -> Cambio de mapa
        - 0 -> Ningun cambio
        """

        if not self.player:
            # si no esta el player en este mapa, se resetan los eventos y el buffer de nuevo destino
            self.reset_stats()

        if self.player:

            for portal in self.portals:

                if portal['available']:
                    portal_coords = portal['rect']
                    x1, y1, x2, y2 = portal_coords

                    if x1 < self.player.x < x2 and y1 < self.player.y < y2:
                        """ el jugador se encuentra dentro de la zona del portal """
                        self.new_destination_map_id = portal['destination_id']
                        self.new_destination_coords = portal['destination_coords']
                        self.set_event(1)
                        self.player = []
                        print('PLAYER ON PORTAL ZONE! DESTINATION_ID: ', portal['destination_id'])

            
    def update_creatures(self):
        """ Actualiza a cada criatura """
        if self.creatures:
            self.creatures = [creature for creature in self.creatures if creature.alive]

            for creature in self.creatures:
                creature.nearest_creatures = self.get_nearest_creatures(creature)
                creature.update()
        else:
            self.creatures = []

    def update_resources(self):
        if self.resources:
            self.resources = [resource for resource in self.resources if resource.available]
        else:
            self.resources = []

    def update_all_entities(self):
        self.update_creatures()
        self.update_resources()

    def update(self):
        self.update_all_entities()
        self.update_events()
    
    def draw(self, screen, player_coords):
        self.draw_background(screen, player_coords)
        self.draw_portals(screen, player_coords)

        for c in self.get_player_nearest_creatures():

            pygame.draw.rect(screen, c.color, c.get_rect(screen, player_coords))
            

        for r in self.resources:
            pygame.draw.rect(screen, r.color, r.get_rect(screen, player_coords))

    def draw_background(self, screen:pygame.surface.Surface, player_coords:tuple):
        #print(f'MAP DRAW BACKGROUND {player_coords=}')

        w, h = screen.get_width(), screen.get_height()
        px, py = player_coords
        
        b_rel_x, b_rel_y = w//2 - px, h//2 - py

        c_w, c_h = self.corner_size
        
        c1_x, c1_y = (0,0)
        c1_relx, c1_rely = w//2 + (c1_x - px), h//2 + (c1_y - py)
        
        c2_x, c2_y = (0, self.fixed_map_size[1]-c_h)
        c2_relx, c2_rely = w//2 + (c2_x - px), h//2 + (c2_y - py)

        c3_x, c3_y = (self.fixed_map_size[0]-c_w, self.fixed_map_size[1]-c_h)
        c3_relx, c3_rely = w//2 + (c3_x - px), h//2 + (c3_y - py)

        c4_x, c4_y = (self.fixed_map_size[0]-c_w, 0)
        c4_relx, c4_rely = w//2 + (c4_x - px), h//2 + (c4_y - py)

        #draw background terrain:
        pygame.draw.rect(screen, self.background_color, (b_rel_x, b_rel_y, *self.fixed_map_size))

        #draw corners
        pygame.draw.rect(screen, (50, 50, 50), (c1_relx, c1_rely, c_w, c_h))
        pygame.draw.rect(screen, (50, 50, 50), (c2_relx, c2_rely, c_w, c_h))
        pygame.draw.rect(screen, (50, 50, 50), (c3_relx, c3_rely, c_w, c_h))
        pygame.draw.rect(screen, (50, 50, 50), (c4_relx, c4_rely, c_w, c_h))        

    def draw_portals(self, screen:pygame.surface.Surface, player_coords:tuple):
        w, h = screen.get_width(), screen.get_height()
        for portal in self.portals:
            #print('DIBUJAND PORTAL: ', portal)

            px, py = player_coords
            port_x1, port_y1, port_x2, port_y2 = portal['rect']

            rel_x = w//2 + (port_x1 - px)
            rel_y = h//2 + (port_y1 - py)
            #print(f'REL X: {rel_x}, REL Y: {rel_y}')
            pygame.draw.rect(screen, (0, 255, 0), (rel_x, rel_y, abs(port_x2 - port_x1), abs(port_y2-port_y1)))
    
    def __repr__(self) -> str:
        return f'Map id: {self.id}'
    

class Aldea(Map):

    def __init__(self, id=0) -> None:
        print('mapa aldea inicializando ..')     
        super().__init__(id)

        self.background_color = (125, 200, 200)
        self.corner_color = (50, 50, 50)

        self.add_new_portal(id='p1', 
                            portal_coords=(470,0, 500, 500), 
                            destination_id=1,
                            destination_coords=(50, 250),
                            available=True
                            )
        
        self.create_creatures()
        
class Bosque(Map):
    def __init__(self, id=1) -> None:
        super().__init__(id)

        self.background_color = (200, 200, 200)
        self.corner_color = (30, 30, 30)

        self.add_new_portal(id='p1', 
                            portal_coords=(0,0, 30, 500), 
                            destination_id=0,
                            destination_coords=(430, 250),
                            available=True
                            )


aldea = Aldea(id=0)
bosque = Bosque(id=1)
