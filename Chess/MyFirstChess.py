import os, pygame
pygame.init()
square_size = 80
board_size = 8
win_size = square_size * board_size
win = pygame.display.set_mode((win_size,win_size+40))
pygame.display.set_caption('Chess by Mates')
counter_font = pygame.font.SysFont('arial', 20, True)

letters = ['A','B','C','D','E','F','G','H'] # not really in use - just for terminal view
board = []
cwd = os.path.dirname(__file__)
image_dir = os.path.join(cwd,'pieces')

pressed_key = False
run = True
score = [0,0]
move_counter = 1
sides = ['b','w']


class Piece(object):
    def __init__(self, x: int, y: int, side: str):
        self.x = x
        self.y = y
        self.side = side
        self.moved = False
    
    def possible_moves(self):
        result = poss_moves(self.x,self.y,self.side,self.one_step,self.name)
        return result

class Pawn(Piece):
    def __str__(self):
        return ' ' + str(letters[self.x])+str(8-self.y) + ' '
    
    name = 'pawn'
    worth = 1
    def draw(self, win: object):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir,'w_pawn_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir,'b_pawn_png_128px.png'))
        picture = pygame.transform.scale(picture, (53, 64))
        win.blit(picture,(square_size * self.x + 13 , square_size * self.y + 8))
    
    def possible_moves(self):
        side = -1 if self.side == 'w' else 1
        result = []
        # possible_steps [[0,1 * side]]
        # if not self.moved: possible_steps.append([0,2*side])

        take_moves = [[self.x + 1,self.y + 1 * side, 'take'],[self.x - 1,self.y + 1 * side, 'take']]
        if is_on_board(self.x,self.y + 1 * side):
            if not board[self.y + 1 * side][self.x]:
                result.append([self.x,self.y + 1 * side, 'free'])
        if not self.moved:    
            if not board [self.y + 2*side][self.x] and not board[self.y + 1 * side][self.x]:
                result.append([self.x, self.y + 2*side, 'free'])
        for move in take_moves:
            if is_on_board(move[0],move[1]):
                if board[move[1]][move[0]] and board[move[1]][move[0]].side != self.side:
                    result.append(move)

        return result
    
class Rook(Piece):
    name = 'rook'
    one_step = 0

    def __str__(self):
        return self.side + ' ' + 'R' + ' '
    
    worth = 5

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir,'w_rook_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir,'b_rook_png_128px.png'))
        picture = pygame.transform.scale(picture, (58, 64))
        win.blit(picture,(square_size * self.x + 11 , square_size * self.y + 8))

class Knight(Piece):
    name = 'knight'
    one_step = 1

    def __str__(self):
        return self.side + ' ' + 'N' + ' '

    worth = 3

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir,'w_knight_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir,'b_knight_png_128px.png'))
        picture = pygame.transform.scale(picture, (58, 64))
        win.blit(picture,(square_size * self.x + 11 , square_size * self.y + 8))

class Bishop(Piece):
    name = 'bishop'
    one_step = 0
    def __str__(self):
        return self.side + ' ' + 'B' + ' '

    worth = 3

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir,'w_bishop_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir,'b_bishop_png_128px.png'))
        picture = pygame.transform.scale(picture, (64, 64))
        win.blit(picture,(square_size * self.x + 8 , square_size * self.y + 8))

class Queen(Piece):
    name = 'queen'
    one_step = 0
    
    def __str__(self):
        return self.side + ' ' + 'Q' + ' '

    worth = 10

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir,'w_queen_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir,'b_queen_png_128px.png'))
        picture = pygame.transform.scale(picture, (70, 64))
        win.blit(picture,(square_size * self.x + 5 , square_size * self.y + 8))

class King(Piece):
    name = 'queen'
    one_step = 1

    def __str__(self):
        return self.side + ' ' + 'K' + ' '

    def draw(self, win):
        if self.side == 'w':
            picture = pygame.image.load(os.path.join(image_dir,'w_king_png_128px.png'))
        else:
            picture = pygame.image.load(os.path.join(image_dir,'b_king_png_128px.png'))
        picture = pygame.transform.scale(picture, (64, 64))
        win.blit(picture,(square_size * self.x + 8 , square_size * self.y + 8))

class My_cursor(object):
    def __init__(self,x,y,kind):
        self.x = x
        self.y = y
        self.selected = False
        self.kind = kind
    
    def draw(self, win):
        if self.kind == 'main':
            if self.selected:
                color = (0,255,0)
            else:
                color = (255,0,0)
        else:
            color = (255,255,0)
        position = (self.x * square_size + 2, self.y * square_size + 2, square_size - 6, square_size - 6)
        pygame.draw.rect(win, color, position ,2)

def draw_board(board_size: int, win: object):
    count = 1
    for y in range (board_size):
        for x in range (board_size):
            if count % 2:
                color = (200,200,200)
            else:
                color = (55,55,55)
            pygame.draw.rect(win, color, (x * square_size, y * square_size, square_size, square_size))
            count += 1
        count += 1

# Create an empty list in proper size
def create_board(board_size: int):
    global board
    for _i in range (board_size):
        line = []
        for _j in range (board_size):
            line.append('')
        board.append(line)

# Fill the board with pieces according to normal chess rules
def fill_with_pieces(board: list):
    side = 'b'
    global white_pieces, black_pieces
    piece_list = black_pieces
    for i in [0,1,6,7]:
        if i == 6: 
            side = 'w'
            piece_list = white_pieces
        if i in [1,6]:
            for j in range (8):
                board [i][j] = Pawn(j,i,side)
        if i in [0,7]:
            board[i][0], board[i][7] = Rook(0,i,side), Rook(7,i,side)
            board[i][1], board[i][6] = Knight(1,i,side), Knight(6,i,side)
            board[i][2], board[i][5] = Bishop(2,i,side), Bishop(5,i,side)
            board[i][3] = Queen(3,i,side)
            board[i][4] = King(4,i,side)
        for cell in board[i]:
            piece_list.append(cell)

# Checking if the move is possible and what type of move it is (not very good name for it though)
def line_move(x: int, y: int, side: str):
    if not is_on_board(x,y): 
        return False, False
    
    if board[y][x]:
        if board[y][x].side == side:
            return False, False
        else:
            return [x,y,'take'], False
    else:
        return [x,y,'free'], True

def is_on_board(x: int, y: int) -> bool:
    if x >=8 or y >=8: return False
    if x < 0 or y < 0: return False
    return True 

def poss_moves(initial_x: int, initial_y: int, side: str, one_step: int, piece: str):
    result = []
    if piece == 'bishop':
        possible_steps = [[1,1],[1,-1],[-1,-1],[-1,1]]
    elif piece == 'rook':
        possible_steps = [[1,0],[-1,0],[0,1],[0,-1]]
    elif piece == 'queen':
        possible_steps = [[1,1],[1,-1],[-1,-1],[-1,1],[1,0],[-1,0],[0,1],[0,-1]]
    elif piece == 'knight':
        possible_steps = [[1,2],[1,-2],[2,1],[2,-1],[-1,2],[-1,-2],[-2,1],[-2,-1]]
    step = 1
    while possible_steps:
        remove = []
        for option in possible_steps :
            x, y = initial_x + step * option[0], initial_y + step * option[1]
            if not line_move(x,y,side)[0]: 
                remove.append(option)
                continue
            result.append(line_move(x,y,side)[0])
            if not line_move(x,y,side)[1]: remove.append(option)
        for option in remove:
            possible_steps.pop(possible_steps.index(option))
        step += 1
        if one_step:
            break
        
    return result

def is_check():
    global white_king, black_king, move_counter, white_pieces, black_pieces
    king = white_king if sides[move_counter % 2] == 'w' else black_king
    piece_list = white_pieces if sides[(move_counter+1) % 2] == 'w' else black_pieces
    # print(king)
    # print(piece_list[0].side)

    for piece in piece_list:
        all_moves = piece.possible_moves()
        for move in all_moves:
            if move[2] == 'take':
                if move[0] == king.x and move[1] == king.y:
                    return True
    return False

# print board in terminal (not in use anymore)
def print_board(board):
    template_lst = ['']
    for _cell in board:
        template_lst.append('{}')
    template_lst.append('')
    template = '|'.join(template_lst)
    print('-' * len(board) * 5)
    for line in board:
        print(template.format(*line))
        print('-' * len(board) * 5)

def piece_move():
    global move_counter
    if cursor.x != pos_cursor.x or cursor.y != pos_cursor.y:
        piece = board[cursor.y][cursor.x]
        if board[pos_cursor.y][pos_cursor.x]:
            taken_piece = board[pos_cursor.y][pos_cursor.x]
            score[move_counter % 2] += taken_piece.worth
            board[pos_cursor.y][pos_cursor.x] = ''
            del taken_piece
        piece.moved = True
        board[pos_cursor.y][pos_cursor.x] = piece
        piece.x = pos_cursor.x
        piece.y = pos_cursor.y
        board[cursor.y][cursor.x] = ''
        move_counter += 1

        if piece.name == 'pawn':    # Possible promotion
            if piece.side == 'w' and piece.y == 0 or piece.side == 'b' and piece.y == 7:
                x, y, side = piece.x, piece.y, piece.side
                del piece
                board[y][x] = Queen(x,y,side)

        if is_check():              # Check
            print ('this is a check')

def redraw_window(board_size, board, win):
    win.fill((0,0,0))
    draw_board(board_size, win)
    cursor.draw(win)
    for line in board:
        for square in line:
            try:
                square.draw(win)
            except:
                pass
    # possible moves
    if cursor.selected:
        poss_mov = board[cursor.y][cursor.x].possible_moves()    
        for move in poss_mov:
            color = (0,255,255) if move[2] == 'free' else (255,0,0)
            position = (move[0] * square_size + 2, move[1] * square_size + 2,  square_size - 6, square_size - 6)
            pygame.draw.rect(win, color, position ,2)
        try:
            pos_cursor.draw(win)
        except:
            pass
    
    move_text = counter_font.render('Move: ' + str(move_counter), 1, (255,255,255))
    score_text = counter_font.render('Score: ' + str(score[1]) + ' | ' + str(score[0]), 1, (255,255,255))
    win.blit(move_text, (10,win_size + 10))
    win.blit(score_text, (win_size//2,win_size + 10))
    pygame.display.update()
    
create_board(8)
white_pieces, black_pieces = [],[]
fill_with_pieces(board)
#fill_with_pieces(board)
cursor = My_cursor(5,3,'main')

# board[2][2] = rook(2,2,'w')
# board[3][5] = bishop(5,3,'w')
# board[1][3] = ''

redraw_window(board_size, board, win)
white_king = board[7][4]
black_king = board[0][4]
key_loop = 0
print(type(board[1][1]))
while run:
   
    keys = pygame.key.get_pressed()
    pygame.time.delay(50)

    if key_loop > 0:
        key_loop += 1
    if key_loop > 3:
        key_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Cursor movement
    if not cursor.selected:
        if keys[pygame.K_RIGHT] and not key_loop:
            pressed_key, key_loop = True, 1
            if cursor.x < board_size - 1:
                cursor.x += 1
        if keys[pygame.K_LEFT] and not key_loop:
            pressed_key, key_loop = True, 1
            if cursor.x > 0:
                cursor.x -= 1
        if keys[pygame.K_UP] and not key_loop:
            pressed_key, key_loop = True, 1
            if cursor.y > 0:
                cursor.y -= 1
        if keys[pygame.K_DOWN] and not key_loop:
            pressed_key, key_loop = True, 1
            if cursor.y < board_size - 1:
                cursor.y += 1
    else:   # movement when selected
        if keys[pygame.K_RIGHT] and not key_loop:
            pressed_key, key_loop = True, 1
            if pos_cursor.x < board_size - 1:
                pos_cursor.x += 1
        if keys[pygame.K_LEFT] and not key_loop:
            pressed_key, key_loop = True, 1
            if pos_cursor.x > 0:
                pos_cursor.x -= 1
        if keys[pygame.K_UP] and not key_loop:
            pressed_key, key_loop = True, 1
            if pos_cursor.y > 0:
                pos_cursor.y -= 1
        if keys[pygame.K_DOWN] and not key_loop:
            pressed_key, key_loop = True, 1
            if pos_cursor.y < board_size - 1:
                pos_cursor.y += 1

    if board[cursor.y][cursor.x]:
        if board[cursor.y][cursor.x].side == sides[move_counter % 2]:
            if keys[pygame.K_KP_ENTER] and not key_loop or keys[pygame.K_SPACE] and not key_loop or keys[pygame.K_RETURN] and not key_loop:
                pressed_key, key_loop = True, 1
                if cursor.selected:
                    for move in poss_mov:
                        if pos_cursor.x == move[0] and pos_cursor.y == move[1]:
                            piece_move()
                            cursor.selected = False
                            pos_counter = 0
                            del pos_cursor
                            break
                else: 
                    cursor.selected = True
                    poss_mov = board[cursor.y][cursor.x].possible_moves()
                    poss_mov.insert(0,[cursor.x,cursor.y,'possition'])
                    pos_cursor = My_cursor(cursor.x, cursor.y,'possition')
    if pressed_key:
        redraw_window(board_size, board, win)
        pressed_key = False

pygame.quit()