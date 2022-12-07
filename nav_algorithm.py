"""
A* Pathfinding visualization simulation for Walmart shopping path generation.
Algorithm: F(n) = G(n) + H(n)

NAVIGATION DETAILS (NOTE):
Line 36 >> node class details
Line 106 >> heuristic function
Line 120 >> algorithm
Line 165 >> make grid
Line 195 >> draw
Line 206 >> main function
Line 207 >> grid dimensions 
Line 261 >> start
"""

import pygame
import math
from queue import PriorityQueue

WIDTH = 800 # dimensions of display
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Walmart Path Generation")

# colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQOUISE = (64, 224, 208)

# red = checked
# white = not checked
# black = barrier (avoid, can't be used as node to visit)
# orange = start node
# purple = path

# visualize node
class Node:
    # keep track of position (x, y), width, color, neighbours, etc.
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # keep track of position 
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE 
    
    def is_end(self):
        return self.color == TURQOUISE
    
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED # changes color
    
    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQOUISE
    
    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other): # compares 2 nodes (n1 < n2 or n1 > n2)
        return False

def H(p1, p2): # heuristic function
    # use manhattan/taxi cab distance
    # formula to computes the quickest distance shaped like an L to get from point p1 to p2
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from: # table that stores node connections
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {} # keeps track of path
    g_score = {node: float("inf") for row in grid for node in row} # stores all the g-scores; key for every node inside g-score
    # starts at float infinity
    g_score[start] = 0 # starts and ends at 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = H(start.get_pos(), end.get_pos()) # uses heuristic function; estimate
    # estimate how far away end node is from start node
    # don't automatically assume best path
    open_set_hash = {start} # check for stuff in priority queue; stores stuff from priority queue; diff data structure

    while not open_set.empty(): # runs until open set is empty; considered every possible node
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # allow to quit and exit

        current = open_set.get()[2] # current node we're working at
        open_set_hash.remove(current) # synchronize with open set hash

        if current == end: # found shortest path
            reconstruct_path(came_from, end, draw)
            end.make_end() # don't draw on end node
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1 # 1 more node over
            if temp_g_score < g_score[neighbour]: # if we found better path, update
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + H(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open() # just inserted in open set

        draw()

        if current != start: # if the node that was just considered is not the start node, it will be turned closed (red)
            current.make_closed()

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([]) # creates row
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node) # append node to row
    # 2D list [[], [], []]
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        # goes from left to right
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
            # goes from up to down

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def draw(win, grid, rows, width): # main draw function
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()
    # runs on update

def main(win, width): # main loop/update func
    ROWS = 10 # change
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    # started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # if started:
            #     continue
            if pygame.mouse.get_pressed()[0]: # left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and start and end: # check for end and start node
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)   
            
                if event.key == pygame.K_r: # reset
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                
    pygame.quit()

main(WIN, WIDTH)