import pygame
import pickle


pygame.init()

# constants
SCREEN_WIDTH = 980
SCREEN_HEIGHT = 630
SIDE_MARGIN = 200
MAX_COL = 28
TILE_TYPES = 3
level = 0
ROW = 18
current_tile = 0
wall_size = SCREEN_HEIGHT // ROW
world_data = []

for row in range(ROW):
    r = [-1] * MAX_COL
    world_data.append(r)

for tile in range(0, MAX_COL):
    world_data[ROW - 1][tile] = 0


# stabalizing FPS
clock = pygame.time.Clock()
FPS = 60

# setting up screen
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))

# caption
pygame.display.set_caption("Level Editor")

# icon
icon = pygame.image.load("levelicon.png")
pygame.display.set_icon(icon)

# loading tiles 
img_list = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f"tile{i}.png")
    img = pygame.transform.scale(img, (wall_size, wall_size))
    img_list.append(img)

# save image
save_img = pygame.image.load("save.png")
s_img = pygame.transform.scale(save_img, (wall_size, wall_size))

# load image
load_img = pygame.image.load("load.png")
l_img = pygame.transform.scale(load_img, (wall_size, wall_size))

# to diplay text
def show_text(level, x, y):
    font = pygame.font.Font("freesansbold.ttf",30)
    levels = font.render(f"Level :- {level}", True, (0,255,0))
    screen.blit(levels, (x, y))

#handling buttons
class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # trigger to check if mouse is clicked
        self.is_clicked = False
    
    def draw(self):
        # getting the position of mouse
        pos = pygame.mouse.get_pos()
        # trigger to perform an action
        action = False
        # checking if the mouse is clicked on the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.is_clicked == False:
                action = True
                self.is_clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.is_clicked = False

        screen.blit(self.image, self.rect)
        return action

# displays the tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * wall_size, y * wall_size))


#buttons
button_list = []
btn_col = 0
btn_row = 0
for i in range(len(img_list)):
    tile_button = Button(SCREEN_WIDTH + 100, SCREEN_HEIGHT // 2 - (btn_col*50), img_list[i])
    button_list.append(tile_button)
    btn_col += 1
    if btn_col > 2:
        btn_row += 1
        btn_col = 0

# diplay grids
def drawgrid():
    for line in range(0, 53):
        pygame.draw.line(screen,(0,0,0),(0, line * wall_size), (SCREEN_WIDTH, line * wall_size))
        pygame.draw.line(screen,(0,0,0), (line * wall_size, 0), (line * wall_size, SCREEN_HEIGHT))

run = True

# creating save and download buttons
save_btn = Button(SCREEN_WIDTH + 50, SCREEN_HEIGHT // 2 + 250, s_img)
load_btn = Button(SCREEN_WIDTH + 120, SCREEN_HEIGHT // 2 + 250, l_img)

#game loop
while run:
    clock.tick(FPS)
    #background
    screen.fill((255,255,255))

    #calling functions
    drawgrid()
    draw_world()
    show_text(level,800, 5)

    #draw panel
    pygame.draw.rect(screen,(10,0,10), (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    #displaying buttons
    btn_count = 0
    for btn_count , btn in enumerate(button_list):
        if btn.draw():
            current_tile = btn_count

    #highlight
    pygame.draw.rect(screen, (0,255,0), button_list[current_tile].rect, 3)

    # save button config
    if save_btn.draw():
        pickle_out = open(f"level{level}_data", "wb")
        pickle.dump(world_data, pickle_out)
        pickle_out.close()

    # load button config
    if load_btn.draw():
        world_data = []
        pickle_in = open(f"level{level}_data", "rb")
        world_data = pickle.load(pickle_in)

    pos = pygame.mouse.get_pos()
    x = pos[0] // wall_size
    y = pos[1] // wall_size
    
    # for dropping new tiles
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        # increase / decrease levels
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1

            if event.key == pygame.K_DOWN and level > 0:
                level -= 1

    pygame.display.update()
pygame.quit()