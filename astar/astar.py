import pygame
import math
from queue import PriorityQueue

# RGB Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Node class, which contains the object initizalizers and methods that will be used throughout the project.
class Node:
	def __init__(self, row, col, window_size, total_rows):
		self.row = row
		self.col = col
		self.x = row * window_size
		self.y = col * window_size
		self.color = BLACK
		self.neighbors = []
		self.window_size = window_size
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == TURQUOISE
  
	def is_open(self):
		return self.color == RED

	def is_barrier(self):
		return self.color == WHITE

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == RED

	def reset(self):
		self.color = BLACK

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = TURQUOISE

	def make_open(self):
		self.color = RED

	def make_barrier(self):
		self.color = WHITE

	def make_end(self):
		self.color = RED

	def make_path(self):
		self.color = PURPLE

	def draw(self, client):
		pygame.draw.rect(client, self.color, (self.x, self.y, self.window_size, self.window_size))
  
	# Manhattan Heuristic Implementation
	# By using this Heuristic, we can only move along the grid in four directions and not "Diagonally" (up,down,left,right)
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

window_size = 600
client = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("[Thomas's Pathfinding Visualization Tool V1] Made by @Nyumat")

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# Creates path from node to node.
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

# A* Pathfinding Search
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	# G score is the cost "so far" to reach node n, which is why it starts at 0.
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	# F score will represent the total estimated cost of the path through the neighbors
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		current = open_set.get()[2]
		open_set_hash.remove(current)
		if current == end:
			# Draw the optimal path once the search reaches the second placed node.
			reconstruct_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True
		# Algo to simultaneously evaluate the neighbor and search for the ending node in the open set
		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			# SEE README.md to understand this algorithm.
			# To put it simply, it traces through each neighbor to find the end node.
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				# If the node isnt found within the open set, the search spreads.
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		draw()
		if current != start:
			current.make_closed()
	return False

# Function controls how our interface, or "grid" will be created.
def make_grid(rows, window_size):
	grid = []
	gap = window_size // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)
	return grid

# Function draws the border and lines for the tool
def draw_grid(client, rows, window_size):
	gap = window_size // rows
	for i in range(rows):
		pygame.draw.line(client, GREY, (0, i * gap), (window_size, i * gap))
		for j in range(rows):
			pygame.draw.line(client, GREY, (j * gap, 0), (j * gap, window_size))

# Function that will draw the plane for the tool to be used in
def draw(client, grid, rows, window_size):
	client.fill(BLACK)
	for row in grid:
		for node in row:
			node.draw(client)
      
	draw_grid(client, rows, window_size)
	pygame.display.update()

# Determines the part of the grid we're clicking so we can interact with it.
def get_clicked_pos(pos, rows, window_size):
	gap = window_size // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

# Main function to hold a lot of the logic and controls.
def main(client, window_size):
	ROWS = 40
	grid = make_grid(ROWS, window_size)

	start = None
	end = None

	run = True
	while run:
		draw(client, grid, ROWS, window_size)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			# Left click
			if pygame.mouse.get_pressed()[0]: 
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, window_size)
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.make_start()

				elif not end and node != start:
					end = node
					end.make_end()

				elif node != end and node != start:
					node.make_barrier()
			# Right Click
			elif pygame.mouse.get_pressed()[2]: 
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, window_size)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None
    
			if event.type == pygame.KEYDOWN:
				# Draw Path to the other node on run (space bar)
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
              
					# Call algorithm object for pathfinding. 
					algorithm(lambda: draw(client, grid, ROWS, window_size), grid, start, end)

				if event.key == pygame.K_r:
					start = None
					end = None
					grid = make_grid(ROWS, window_size)

	pygame.quit()
	
if __name__ == "__main__":
    main(client,window_size)
    