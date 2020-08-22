import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return  self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE

    def is_end (self):
        return self.color == PURPLE

    def reset(self):
        self.color == WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self,other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Object that will be used to draw the most optimal path from node to node.
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

# A* Pathfinding Search
# This algorithm is mostly new to me, so I will be implementing it a step at a time.
# The first part of this is just me declaring functions to be used for later.
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	# Scores being used to represent the distances the nodes have to travel.
	# With a higher score indicating distance, and lower score indicating closeness.
	g_score = {Node: float("inf") for row in grid for Node in row}
	g_score[start] = 0
	f_score = {Node: float("inf") for row in grid for Node in row}
	f_score[start] = h(start.get_pos(), end.get_pos())
			
		
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for Node in row:
			Node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		# More logic for the tool state/controls
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]: # LEFT 
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				Node = grid[row][col]
				if not start and Node != end:
					start = Node
					start.make_start()

				elif not end and Node != start:
					end = Node
					end.make_end()

				elif Node != end and Node != start:
					Node.make_barrier() 
	
