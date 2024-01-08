import pygame
from network import Network
from utils import make_tuple, parse_tuple, load_dict, dump_dict

width = 500
height = 500
pygame.init()
window = pygame.display.set_mode((width, height))

pygame.display.set_caption("client")

class Player:
    def __init__(self, x, y, width, height, color, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.id = id
        self.rect = (x, y, width, height)
        self.vel = 3
    
#    def draw(self, window):
#        pygame.draw.rect(window, self.color, self.rect)
    
    # check for key press
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.x -= self.vel
        
        if keys[pygame.K_d]:
            self.x += self.vel
        
        if keys[pygame.K_w]:
            self.y -= self.vel
        
        if keys[pygame.K_s]:
            self.y += self.vel
        
        self.update()
    
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def as_dict(self):
        # TODO: find a way to write this better
        # (rewrite this if ever re-fmt data)
        return {"pos": (self.x, self.y)}

def redraw(window, my_player, my_player_data):
    window.fill((255, 255, 255))

    # TODO: definitely update this later lmao
    # keep a list of player objects, then update the objects from the server response?
    for id, player in my_player_data.items():
        pos = player["pos"]
        pos_x = pos[0]
        pos_y = pos[1]

        if id == my_player.id:
            pygame.draw.rect(window, (0, 255, 0), (pos_x, pos_y, 50, 50))
        else:
            pygame.draw.rect(window, (255, 0, 0), (pos_x, pos_y, 50, 50))

    pygame.display.update()

def main():
    n = Network()
    start_pos = n.pos
    start_pos_x = start_pos[0]
    start_pos_y = start_pos[1]

    running = True
    clock = pygame.time.Clock()
    player = Player(start_pos_x, start_pos_y, 50, 50, (0, 255, 0), id=n.id)
    all_players_data = {}
    
    while running:
        clock.tick(60)

        # send my player data to server (pos/states)
        my_player_data = dump_dict(player.as_dict())
        server_response = n.send(my_player_data)
        all_players_data = load_dict(server_response) # server response w all player data

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        player.move()
        redraw(window, player, all_players_data)

if __name__ == "__main__":
    main()
