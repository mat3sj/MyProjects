import pygame, random
pygame.init()

# window init
win_size = 500
cell_size = 5
win = pygame.display.set_mode((win_size,win_size))
pygame.display.set_caption('Game of Life by Mates')

# Probability of initial life
initial_odds = [True]
for i in range (10):
    initial_odds.append(False)

class cell(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.life = random.choice(initial_odds) 

    def draw(self,win: object):
        if self.life:
            pygame.draw.rect(win, (0,0,0), (self.x * 5,self.y * 5,5,5))
        else:
            pygame.draw.rect(win, (255,255,255), (self.x * 5,self.y * 5,5,5))

# Board creation
board = []
for y in range(win_size//cell_size):
    line = []
    for x in range(win_size//cell_size):
        line.append(cell(x,y))
    board.append(line)

# Counting number of cells alive including the middle one
def neighbours_alive(x: int, y: int) -> int:
    result = 0
    min_x, min_y, max_x, max_y = x-1, y-1, x+1, y+1
    if x==0: min_x += 1
    if y == 0: min_y += 1 
    if x == win_size // cell_size: max_x -= 1
    if y == win_size // cell_size: max_y -= 1 
    for this_y, line in enumerate(current_board[min_y:max_y + 1]):
        for this_x, this_cell in enumerate(line[min_x:max_x + 1]):
            if this_cell.life == True:
                result += 1

    return result

counter_font = pygame.font.SysFont('arial', 20, True)
def redraw_game_window():
    win.fill((255,255,0))
    for line in current_board:
        for this_cell in line:
            this_cell.draw(win)
    text = counter_font.render('Generation: ' + str(counter), 1, (255,0,0))
    text2 = counter_font.render('Alive: ' + str(alive) + ' %', 1, (255,0,0))
    win.blit(text, (10,10))
    win.blit(text2, (10,30))
    pygame.display.update()

counter = 0
state_A, state_B = board, []
both_states = [state_A, state_B]

run = True
while run:
    pygame.time.delay(1000)
    current_board = both_states[counter % 2]
    next_board = []
    alive = 0
    for line in current_board:
        new_line = []
        for this_cell in line:
            # Actual rules of Game of Life
            if this_cell.life == True:
                if not (neighbours_alive(this_cell.x, this_cell.y) -1) in [2,3]:
                    this_cell.life = False
                else:
                    alive +=1
            else:
                if neighbours_alive(this_cell.x, this_cell.y) == 3:
                    this_cell.life = True
                    alive += 1
            new_line.append(this_cell)
        next_board.append(new_line)

    both_states[counter % 2] = []
    both_states[(counter + 1) % 2] = next_board

    redraw_game_window()
    counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()