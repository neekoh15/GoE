
class Entity:

    def __init__(self) -> None:
        self.x = None
        self.y = None
        self.coords = (self.x, self.y)
        self.width, self.height = (None, None)
        self.color = None

    def get_rect(self, screen, player_coords):
        w, h = screen.get_width(), screen.get_height()
        px, py = player_coords
        rel_x = w//2 + (self.x - px)
        rel_y = h//2 + (self.y - py)

        return (rel_x, rel_y, self.width, self.height)
    
    def update(self):
        self.coords = (self.x, self.y)


class Spider(Entity):
    def __init__(self) -> None:
        super().__init__()

        self.color = (255, 0, 255)
        self.width, self.height = (15, 15)
        self.update()

class Tree(Entity):
    def __init__(self) -> None:
        super().__init__()

        self.color = (0, 125, 0)
        self.width, self.height = (30, 30)
        self.update()