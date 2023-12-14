class Map:
    def __init__(self, id) -> None:

        self.id = id
        self.event = 0
        self.maps_connected = []
        self.portals = []
        self.new_destination_map_id = None

        self.player = []
        self.creatures = []
        self.objects = []
        self.resources = []

        self.fixed_map_size = (1000, 1000)

        self.all_entities = self.player + self.creatures + self.objects + self.resources

    def add_new_portal(self, id:int, portal_coords:tuple, destination_id:int, available=True):
        """ 
        Crea un nuevo portal hacia un nuevo destino

        - portal_coords: list[tuple, tuple] -> rect coords (x1, y1, x2, y2)\n
            Define una seccion rectangular donde se producira el evento de cambio de mapa o destino

        - destination_id: int -> id del destino a donde se quiere redirigir el jugador
        """
        self.portals.append({
            'id': id,
            'destination_id': destination_id,
            'rect': portal_coords,
            'available': available
        })

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


    def get_nearest_creatures(self, creature):

        nearest_creatures = []
        
        for other_creature in self.creatures:
            if other_creature != creature:

                distance_x = (creature.x - other_creature.x)**2
                distance_y = (creature.y - other_creature.y)**2
                mod_distance = (distance_x - distance_y)**0.5

                if mod_distance <= creature.vision_radius:
                    nearest_creatures.append(creature)

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
            self.set_event(0)
            self.new_destination_map_id = None

        if self.player:

            for portal in self.portals:

                if portal['available']:
                    portal_coords = portal['rect']
                    x1, y1, x2, y2 = portal_coords

                    if x1 < self.player.x < x2 and y1 < self.player.y < y2:
                        """ el jugador se encuentra dentro de la zona del portal """
                        self.new_destination_map_id = portal['destination_id']
                        self.set_event(1)
                        self.player = []

            
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
        pass
    
    def __repr__(self) -> str:
        return f'Map id: {self.id}'
    


map1 = Map(id=0)