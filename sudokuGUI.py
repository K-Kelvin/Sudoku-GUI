import pygame, time, os, copy
from pygame.locals import *
pygame.init()

# setting up colors
BLACK = (0, 0, 0)
WHITE = (205, 205, 205)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)
MAGENTA = (200, 0 ,200)
SKYBLUE = (135, 206, 250)

# setting up the  screen
x, y = 0, 350
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (y,x)
screen = pygame.display.set_mode((800,600),RESIZABLE)
pygame.display.set_caption("Sudoku")
screen_rect = screen.get_rect()
background = WHITE

#icon = pygame.transform.scale(pygame.image.load('images/jet1.png'),(32,32))
#icon.set_colorkey(BLACK)
#pygame.display.set_icon(icon)

# setting up the clock
clock = pygame.time.Clock()

# setting up the boards
board1 = [
         [0,2,0,0],
         [1,3,0,0],
         [0,4,1,0],
         [3,0,2,4]
]
empty_board1 = [[0,0,0,0] for i in range(4)]
board2 = [
        [0, 0, 0, 0, 7, 0, 1, 9, 0],
        [9, 0, 7, 0, 0, 0, 3, 0, 0],
        [0, 6, 0, 0, 9, 0, 4, 5, 0],
        [2, 0, 4, 0, 5, 0, 0, 1, 0],
        [0, 1, 0, 3, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 6, 0, 0, 8, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 2, 0, 8, 0, 0, 0, 0, 1],
        [8, 0, 5, 0, 1, 0, 0, 3, 0]
]
empty_board2 = [[0,0,0,0,0,0,0,0,0] for i in range(9)]

def Print(text,size,pos,color,*args,my_font='quicksandmedium',surface=screen):
    try:
        if my_font in pygame.font.get_fonts() or my_font == None:
            font = pygame.font.SysFont(my_font, size)
        else:
            font = pygame.font.Font(my_font,size)
    except:
        font = pygame.font.Font(None,size)
    surf = font.render(text,True,color)
    rect = surf.get_rect(center=pos)
    for arg in args:
        if arg == 'center':
            rect.center = pos
        elif arg == 'midtop':
            rect.midtop = pos
        elif arg == 'midbottom':
            rect.midbottom = pos
        elif arg == 'midleft':
            rect.midleft = pos
        elif arg == 'midright':
            rect.midright = pos
        elif arg == 'topleft':
            rect.topleft = pos
        elif arg == 'topright':
            rect.topright = pos
        elif arg == 'bottomleft':
            rect.bottomleft = pos
        elif arg == 'bottomright':
            rect.bottomright = pos

    surface.blit(surf,rect)

def my_time(start_time,mode='run'):
	global the_time
	if mode == 'run':
		the_time = int( time.time() - start_time )
	else:
		the_time = the_time
	min = the_time // 60
	sec = the_time % 60
	if the_time < 60:
		if sec < 10 :
			return '0%s' % sec
		else:
			return sec
	else:
		if sec < 10:
			sec = '0%s' % sec
	return '%s:%s' %(min,sec)

class Button:
    def __init__(self,size,radius,color,hover_color,txt_size,txt_color,surface):
        self.size = size
        self.radius = radius
        self.color = color
        self.color_ = copy.copy(color)
        self.hover_color = hover_color
        self.txt_size = txt_size
        self.txt_color = txt_color
        self.surface = surface
        self.rect = Rect((0,0),self.size)

    def my_button(self,pos,txt,*args):
        rect = Rect(pos,self.size)
        rad = self.radius
        if rad > 0.5*rect.height: rad = int(0.5*rect.height)
        elif rad > 0.5*rect.width: rad = int(0.5*rect.width)
        center = rect.width//2,rect.height//2
        rectangle = pygame.Surface(rect.size, SRCALPHA)
        rectangle.fill((0,0,0,0))

        rect2 = rect.inflate(0,-rad*2)
        rect3 = rect.inflate(-rad*2,0)
        rect2.center = center
        rect3.center = center
        rectangle2 = pygame.Surface(rect2.size, SRCALPHA)
        rectangle3 = pygame.Surface(rect3.size, SRCALPHA)

        rectangle2.fill(self.color)
        rectangle3.fill(self.color)
        rectangle.blit(rectangle2,rect2)
        rectangle.blit(rectangle3,rect3)

        pygame.draw.circle(rectangle, self.color, (rad,rad), rad)
        pygame.draw.circle(rectangle, self.color, (rect.width-rad,rad), rad)
        pygame.draw.circle(rectangle, self.color, (rad,rect.height-rad), rad)
        pygame.draw.circle(rectangle, self.color, (rect.width-rad,rect.height-rad), rad)

        Print(txt,self.txt_size,center,self.txt_color,'center',surface=rectangle)
        for arg in args:
            if arg == 'center': rect.center = rect.topleft
            if arg == 'midtop': rect.midtop = rect.topleft
            if arg == 'midbottom': rect.midbottom = rect.topleft
            if arg == 'midleft': rect.midleft = rect.topleft
            if arg == 'midright': rect.midright = rect.topleft
            if arg == 'topleft': rect.topleft = rect.topleft
            if arg == 'topright': rect.topright = rect.topleft
            if arg == 'bottomleft': rect.bottomleft = rect.topleft
            if arg == 'bottomright': rect.bottomright = rect.topleft
        self.surface.blit(rectangle, rect)
        self.rect = rect; self.txt = txt
        self.update()
        return self.rect

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color
            if click[0]:
                if self.txt == 'Solution':
                    print('Solution')
                elif self.txt == 'Reset':
                    print('Reset')
                elif self.txt == '4 x 4':
                    print('Current board: 9 x 9')
                elif self.txt == '9 x 9':
                    print('Current board: 4 x 4')
                elif self.txt == 'Custon':
                    print('Custom')
        else:
            self.color = self.color_

class Board():
    def __init__(self,board):
        self.width = 432
        self.height = 432
        the_board = copy.deepcopy(board)
        self.board = copy.deepcopy(the_board)
        self.grid_color = RED
        self.cube_color = GRAY
        self.line_color = BLUE
        self.original_board = [] # holds the positions of original numbers of the board
        self.num_type = 'original' # distinguish original numbers from input numbers
        self.mode = 'solving'
        self.reinitialize()

    def reinitialize(self):
        # function to reinitialize the positions if the screen size changes
        self.positions = []  # holds the center positions of the cubes
        self.count = True  # variable to enable single appending of cube center positions to the self.positions list
        self.rect = Rect((screen_rect.width - self.width) / 2, (screen_rect.height - self.height) / 2, self.width,self.height)
        self.x, self.y = self.rect.left, self.rect.top

    def custom(self):
        self.mode = 'editing'
        self.num_type = None
        self.original_board = []
        if len(self.board) == 9:
            self.board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        else:
            self.board = [[0,0,0,0] for i in range(4)]

    def grid(self):
        # prints the cubes,lines and grid and records the cube positions
        y = self.rect.top
        # print the cubes
        for row in range(len(self.board)):
            lst = []
            x = self.rect.left
            for column in range(len(self.board[0])):
                self.cube = Rect(x,y,self.width//len(self.board),self.height//len(self.board))
                pygame.draw.rect(screen,self.cube_color,self.cube,1)
                x += self.cube.width
                lst.append(self.cube.center)
            if self.count: # record the center positions of the cubes once
                self.positions.append(lst)
            y += self.cube.height
        self.count = False
        # print the lines
        if len(self.board) == 4:
            pygame.draw.line(screen, self.line_color, ( self.rect.left,self.rect.centery), (self.rect.right,self.rect.centery), 2)
            pygame.draw.line(screen, self.line_color, (self.rect.centerx, self.rect.top), (self.rect.centerx, self.rect.bottom), 2)
        else:
            s = 3 # thickness of the lines
            cube_length = (1/3)*self.rect.height
            # horizontal lines
            pygame.draw.line(screen,self.line_color, (self.rect.left, self.rect.top+cube_length), (self.rect.right, self.rect.top+cube_length), s)
            pygame.draw.line(screen,self.line_color, (self.rect.left,self.rect.top +2*cube_length),(self.rect.right,self.rect.top+2*cube_length), s)
            # vertical lines
            pygame.draw.line(screen,self.line_color, (self.rect.left+cube_length,self.rect.top), (self.rect.left+cube_length, self.rect.bottom), s)
            pygame.draw.line(screen,self.line_color,(self.rect.left+2*cube_length,self.rect.top),(self.rect.left+2*cube_length,self.rect.bottom),s)
        # finally print the grid then call the update then the print_numbers function
        pygame.draw.rect(screen, self.grid_color, self.rect, 4)
        #self.update()
        self.print_numbers()

    def update(self):
        #self.num_type = 'editable'
        global previous_key
        cell_size = self.cube.width - 8
        cell = Rect(self.x + 4, self.y + 4, cell_size, cell_size)

        # control movement of the selector cell
        key = pygame.key.get_pressed()
        if key[K_LCTRL] and key[K_z]:
            self.solve()
        if key[K_UP] and not previous_key[K_UP] and cell.top > self.rect.top+4:
            self.y -= self.cube.width
        if key[K_DOWN] and not previous_key[K_DOWN] and cell.bottom < self.rect.bottom-4:
            self.y += self.cube.width
        if key[K_LEFT] and not previous_key[K_LEFT] and cell.left > self.rect.left+4:
            self.x -= self.cube.width
        if key[K_RIGHT] and not previous_key[K_RIGHT] and cell.right < self.rect.right-4:
            self.x += self.cube.width

        # check the position of the selector(cell) and fill in values
        for cube_row in range(len(self.positions)):
            for cube_column in range(len(self.positions[0])):
                if cell.collidepoint(self.positions[cube_row][cube_column]): # if selector is in that cube
                    if key[K_RETURN] and not previous_key[K_RETURN]:
                        print('selected: ',self.board[cube_row][cube_column])
                    for value,keypress in enumerate(key_list1 if len(self.board) == 4 else key_list2):
                        # if the position is in the original list, dont change it
                        if (cube_row,cube_column) not in self.original_board:
                            if key[K_BACKSPACE]:
                                self.board[cube_row][cube_column] = 0
                            if key[keypress] and not previous_key[keypress]:
                                self.board[cube_row][cube_column] = value + 1
                        else: # if the player wants to input a custom board
                            if self.mode == 'editing':
                                if key[K_BACKSPACE]:
                                    self.board[cube_row][cube_column] = 0
                                if key[keypress] and not previous_key[keypress]:
                                    self.board[cube_row][cube_column] = value + 1
        previous_key = key
        pygame.draw.rect(screen, MAGENTA, cell, 4)

    def print_numbers(self):
        pos_dict = self.positions
        board = self.board
        for n in range(len(pos_dict)):
            for m in range(len(pos_dict[0])):
                if board[n][m] == 0:
                    Print(' ', 30, pos_dict[n][m], BLACK,'center')
                else:
                    if self.num_type == 'original' or self.mode == 'editing':
                        self.original_board.append((n, m))
                    if (n,m) in self.original_board or self.mode == 'editing':
                        Print('%s' % (board[n][m]), 35, pos_dict[n][m], BLACK, 'center')
                    else:
                        Print('%s' % (board[n][m]), 30, pos_dict[n][m], GRAY, 'center')
        self.num_type = 'editable'

    def solve(self):
        # finds an empty position in the board and overwrites a valid number on that position
        self.mode = 'solving'
        self.num_type = 'editable'  # distinguishes the numbers of the original board from the numbers in the solution
        find = self.find_empty()
        if find:
            row, col = find
        else:
            return True
        for i in range(1,len(self.board[0])+1):
            if self.valid((row, col), i):
                self.board[row][col] = i
                if len(self.board) == 4:
                	screen.fill(background)
                	Print('Time: {}'.format(my_time(start_time)) , 30, (10, 10), Color('black'), 'topleft')
                	Print('Solving...', 50,(screen_rect.width/2, 100), Color('green4'),'center')
                	self.grid()
                	pygame.display.update()
                	pygame.time.delay(150)
                
                elif len(self.board) == 9:
                	pass ;'''
                	screen.fill(background)
                	Print('Solving...',50,(screen_rect.width/2,100),Color('green4'),'center')
                	self.grid()
                	pygame.display.update()'''

                if self.solve():
                    return True

                self.board[row][col] = 0
        return False

    def valid(self, pos, num):
        # checks if num, an integer, is valid at position pos, (row,column)
        # check row
        for i in range(0, len(self.board)):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False
        # check column
        for i in range(0, len(self.board)):
            if self.board[i][pos[1]] == num and pos[1] != i:
                return False
        # check box
        if len(self.board[0]) == 4:
            box_x = pos[1] // 2
            box_y = pos[0] // 2
            for i in range(box_y*2, box_y*2 + 2):
                for j in range(box_x*2, box_x*2 + 2):
                    if self.board[i][j] == num and (i,j) != pos:
                        return False
            return True
        else:
            box_x = pos[1] // 3
            box_y = pos[0] // 3
            for i in range(box_y*3, box_y*3 + 3):
                for j in range(box_x*3, box_x*3 + 3):
                    if self.board[i][j] == num and (i, j) != pos:
                        return False
            return True

    def find_empty(self):
        #  finds an empty space in the board :returns (row, column)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0 or type(self.board[i][j]) != int:
                    return (i, j)
        return None

bd1 = Board(board1)
bd2 = Board(board2)
key_list1 = [K_1, K_2, K_3, K_4]
key_list2 = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]

btn = Button((140, 80), 10, Color('gold3'), Color('red2'), 30, Color('black'), screen)
btn2 = copy.copy(btn)
btn3 = copy.copy(btn)
btn4 = copy.copy(btn)

previous_key = pygame.key.get_pressed()
def main():
    global screen_rect, screen, bd1, bd2
    the_board = bd1
    global start_time
    mode = 'run'
    start_time = time.time()
    while True:
        screen.fill(background)
        button1 = btn.my_button((12, 80), 'Solution')
        button2 = btn2.my_button((12, 200), 'Reset')
        button3 = btn3.my_button((12, 320), '{}'.format('>>' if the_board == bd1 else '<<'))
        button4 = btn4.my_button((12, 440), 'Custom')
        for event in pygame.event.get():
            if event.type == QUIT: quit()
            elif event.type == VIDEORESIZE:
                if event.w < 500: event.w = 500
                elif event.h < 600: event.h = 500
                screen = pygame.display.set_mode((event.w,event.h),RESIZABLE)
                screen_rect = screen.get_rect()
                bd1.reinitialize(); bd2.reinitialize()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button1.collidepoint(event.pos): the_board.solve()
                    if button2.collidepoint(event.pos):
                        the_board.__init__(board1) if the_board == bd1 else the_board.__init__(board2)
                        start_time = time.time()
                        mode = 'run'
                    if button3.collidepoint(event.pos):
                        if the_board == bd1: the_board = bd2
                        else: the_board = bd1
                    if button4.collidepoint(event.pos): the_board.custom()
            elif event.type == KEYDOWN:
                if event.key == K_LSHIFT: the_board = bd1
                elif event.key == K_RSHIFT: the_board = bd2
                elif event.key == K_ESCAPE: quit()
        ############################# code goes here #############################
        the_board.grid()
        the_board.update()

        Print(f'Time: {my_time(start_time,mode)}', 30, (10, 10), Color('black'), 'topleft')
        if not the_board.find_empty():
        	mode = 'stop'
        	Print('Solved',50,(screen_rect.width/2,100),Color('maroon'),'center')

        #############################   end of code  #############################
        pygame.display.update()
        clock.tick(20)
        #pygame.time.delay(2000)

main()