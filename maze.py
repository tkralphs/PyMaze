'''
Maze module
Brief description:
Defines a maze class, has solve method that finds the path from the upper left 
cell to down right cell.
 
Detailed description:
Classes contained:
Maze
    attributes:
        density:    density of the obstacles in the maze
                    type: float
        dim1:       x-dimension of the maze
                    type: int
        dim2:       y-dimension of the maze
                    type: int
        mode:       graphics mode for the solve method
                    SILENT:            no graphics
                    GRAPHICAL_FULL:    display algorithm progess with full view
                    GRAPHICAL_LIMITED: display algorithm progess with limited view
        path:       path found by the robot
                    type: list of tuples (x,y)
        maze:       maze
                    type: list of lists
        xCurrent:   current x coordinate of the robot
                    type: int
        yCurrent:   current y coordinate of the robot
                    type: int
    methods:
        __init__(self):            constructor of the class
        generate_maze(self):       generates self.maze randomly such that it 
                                   contains at least one path from upper left 
                                   cell to the down right cell
        solve(self):               generates path and produce graphical output
                                   according to self.mode value. To change
                                   display mode use self.set_mode() method.
                                   if mode='silent': generates path with no
                                   display
                                   if mode='graphical_full': generates path and
                                   shows algorithm progress with view of whole
                                   maze
                                   if mode='graphical_limited': generates path
                                   and shows algorithm progress with limited
                                   view of maze
        game(self):                displays partial maze, waits for user input 
                                   (arrow keys) to move the robot, pressing key
                                   'a' uncovers the whole maze
        get_new_coordinates(self):
                                   generates the new coordinates by evaluating 
                                   the user input (used in game mode)
        step(self):
                                   returns to next coordinates of the robot by 
                                   evaluating the current coordinate and
                                   the maze.
        display_init(self):        initialize display (pygame) related 
                                   parameters and functions
        draw_maze(self):           draws the whole self.maze to display
        update_maze(self):
                                   updates the status of the neighbors of cell 
                                   (self.xCurrent,self.yCurrent)
        set_mode(self, mode):      Sets mode attribute (see above)

Maze ASCII representation
 ' ' represents an empty cell
 'X' represents an obstacle
 '*' represents the path

Maze graphical representation
 Grey  represents an empty cell (not visited)
 Green represents an empty cell (already visited)
 Red   represents an obstacle
 Blue  represents the path
 White represents the current location of the robot

Meaning of entries in self.maze
 0 represents empty (unexplored) cell
 1 represents an obstacle
 2 represents the path
 3 represents a cell that has been explored, but is not on the path
 4 represents the cell the robot is in

Created on Dec 25, 2011
Modified Feb 6, 2012
'''

__version__    = '1.0.0'
__author__     = 'Aykut Bulut, Ted Ralphs (ayb211@lehigh.edu,ted@lehigh.edu)'
__license__    = 'BSD'
__maintainer__ = 'Aykut Bulut'
__email__      = 'ayb211@lehigh.edu'
__url__        = None
__title__      = 'Maze class'

import pygame
from pygame.locals import *
from random import seed, random
from coinor.blimpy import Stack

# empty (unexplored) cell
EMPTY = 0
# cell with an obstacle
OBSTACLE = 1
# cell that is on the path
ON_PATH = 2
# cell that has been explored, but is not on the path
EXPLORED = 3
# cell the robot is in
ROBOT = 4

# graphical modes
SILENT = "silent"
GRAPHICAL_FULL = "graphical_full"
GRAPHICAL_LIMITED = "graphical_limited"

# Search directions
UP = {'x': -1, 'y': 0}
DOWN = {'x': 1, 'y': 0}
RIGHT = {'x': 0, 'y': 1}
LEFT = {'x': 0, 'y': -1}

# Order in which to try directions
SEARCH_ORDER = [DOWN, RIGHT, UP, LEFT]

KEY_PRESS_DIRECTION = {K_UP : UP,
                       K_DOWN : DOWN,
                       K_RIGHT : RIGHT,
                       K_LEFT : LEFT}

class Maze(object):
    '''
    Defines a maze class, has solve method that finds the path from the upper
    left cell to down right cell.
    '''
    def __init__ (self, dimx=50, dimy=50, seedInput=0, density=0.5):
        ''' Constructor for Maze class
        posts: self.destiny, self.dim1, self.dim2, self.mode, self.maze,
        self.path, self.xCurrent, self.yCurrent
        '''
        seed(seedInput)
        self.density = density
        self.dimension = {'x' : dimx, 'y' : dimy}
        self.mode = GRAPHICAL_LIMITED
        self.generate_maze()
        self.path = Stack()
        self.location = (0, 0)

    def generate_maze(self):
        '''
        Generates self.maze randomly such that it contains at least one path
        from upper left cell to the down right cell
        Post: updates self.maze
        '''
        x,y = 0,0
        path = set()
        path.add((x,y))
        while (x, y) != (self.dimension['x']-1, self.dimension['y']-1):
            if random() < 0.5:
                if x<self.dimension['x']-1:
                    x+=1
                    path.add((x,y))
            else:
                if y<self.dimension['y']-1:
                    y+=1
                    path.add((x,y))
        self.maze = []
        for x in range(self.dimension['x']):
            self.maze.append([])
            for y in range(self.dimension['y']):
                if random() < self.density:
                    self.maze[x].append(OBSTACLE)
                else:
                    self.maze[x].append(EMPTY)
        for x,y in path:
            self.maze[x][y] = EMPTY

    def __str__(self):
        '''
        Returns string representation of Maze object.
        Return: string a that represents current status of Maze object.
        '''
        a = ''
        for x in range(self.dimension['x']):
            for y in range(self.dimension['y']):
                if self.maze[x][y] == ON_PATH or self.maze[x][y] == ROBOT:
                    a += '*'
                elif self.maze[x][y] == OBSTACLE:
                    a += 'X'
                else:
                    a += ' '
            a += '\n'
        a += '\n'
        return a
        
    def solve(self):
        '''
        If mode=SILENT: generates path with no display, if mode=GRAPHICAL_FULL: generates path and
        shows algorithm progress with view of whole maze if mode=GRAPHICAL_LIMITED: generates
        path and shows algorithm progress with limited view of maze.
        Post: updates self.maze, self.path, self.xCurrent, self.yCurrent
        Return: returns self.path
        '''
        eventType, done = None, False
        self.location = (0, 0)
        self.maze[self.location[0]][self.location[1]] = ROBOT
        if self.mode == GRAPHICAL_FULL:
            self.display_init()
            self.draw_maze()
        elif self.mode == GRAPHICAL_LIMITED:
            self.display_init()
            self.update_maze()
        while eventType != QUIT and not done:
            if self.mode == GRAPHICAL_FULL or self.mode == GRAPHICAL_LIMITED:
                for event in pygame.event.get():
                    eventType = event.type
            new_location = self.find_next_step()
            if new_location is None:
                # Mark the current location as a dead end
                self.maze[self.location[0]][self.location[1]] = EXPLORED
                # pop the next cell off the path stack (go back one space)
                self.location = self.path.pop()
                self.maze[self.location[0]][self.location[1]] = ROBOT
            else:
                self.maze[self.location[0]][self.location[1]] = ON_PATH
                self.path.push(self.location)
                self.location = new_location
            if self.mode == GRAPHICAL_FULL or self.mode == GRAPHICAL_LIMITED:
                self.clock.tick(self.framerate)
                self.update_maze()
                self.screen.blit(self.background, (0,0))
                pygame.display.flip()
            if (self.maze[0][0] == EXPLORED or
                self.location == (self.dimension['x']-1, self.dimension['y']-1)):
                self.path.push(self.location)
                done = True
        return self.path

    def game(self):
        '''
        displays partial maze, waits for user input (arrow keys) to move the
        robot, pressing key 'a' uncovers the whole maze.
        Post: Updates self.xCurrent, self.yCurrent
        '''
        # pygame related
        self.display_init()
        # end of pygame related
        eventType, done = None, False
        self.maze[self.location[0]][self.location[1]] = ROBOT
        self.path.push(self.location)
        self.update_maze()
        while eventType != QUIT and done == False: 
            for event in pygame.event.get():
                eventType = event.type
            keystate = pygame.key.get_pressed()
            new_location = self.get_new_coordinates(keystate)
            if new_location is not None:
                self.location = new_location
                self.path.push(self.location)
            self.clock.tick(self.framerate)
            self.update_maze()
            self.screen.blit(self.background, (0,0))
            pygame.display.flip()
            if self.location == (self.dimension['x']-1, self.dimension['y']-1):
                done = True

    def get_new_coordinates(self,keystate):
        '''
        Generates the new coordinates by evaluating the user input (used
        in game mode)
        Post: Updates self.maze
        Return: Returns (x,y) that represents new coordinates.
        '''
        for key_press in KEY_PRESS_DIRECTION:
            if keystate[key_press] is 0:
                continue
            new_location = (self.location[0] + KEY_PRESS_DIRECTION[key_press]['x'],
                            self.location[1] + KEY_PRESS_DIRECTION[key_press]['y'])
            if (0 <= new_location[0] < self.dimension['x'] and
                0 <= new_location[1] < self.dimension['y'] and
                self.maze[new_location[0]][new_location[1]] != OBSTACLE):
                self.maze[self.location[0]][self.location[1]] = ON_PATH
                self.maze[new_location[0]][new_location[1]] = ROBOT
                return new_location
        return None
    
    def find_next_step(self):
        # Search for a place to go
        for direction in SEARCH_ORDER:
            new_location = (self.location[0] + direction['x'],
                            self.location[1] + direction['y'])
            if (0 <= new_location[0] < self.dimension['x'] and
                0 <= new_location[1] < self.dimension['y'] and
                self.maze[new_location[0]][new_location[1]] == EMPTY):
                self.maze[new_location[0]][new_location[1]] = ROBOT
                return new_location
        return None
    
    def display_init(self):
        '''
        Initialize display (pygame) related parameters and functions
        '''
        pygame.init()
        # pygame display parameters
        self.cellDimension = {0:10,1:10}
        self.framerate = 10
        self.colors = {EMPTY:(200,200,200),
                       OBSTACLE:(200,0,0),
                       ON_PATH:(0,0,200), 
                       EXPLORED:(0,200,0), 
                       ROBOT:(255,255,255,255)}
        # end of pygame display parameters
        self.screenDimension = (self.dimension['y']*self.cellDimension[0],
                                self.dimension['x']*self.cellDimension[1]) 
        self.screen = pygame.display.set_mode(self.screenDimension)
        pygame.display.set_caption(__title__)
        self.background = self.screen.convert()
        self.clock = pygame.time.Clock()

    def draw_maze(self):
        '''
        Draws the whole self.maze to display
        '''
        for x in range(self.dimension['y']):
            for y in range(self.dimension['x']):
                rectangle = (x*self.cellDimension[0],y*self.cellDimension[1],
                             self.cellDimension[0], self.cellDimension[1])
                pygame.draw.rect(self.background,self.colors[self.maze[y][x]],
                                 rectangle) 

    def update_maze(self):
        '''
        Updates the status of the neighbors of cell (self.xCurrent,
        self.yCurrent)
        '''
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if (0 <= self.location[1] + i < self.dimension['x'] and 
                    0 <= self.location[0] + j < self.dimension['y']):
                    rectangle = ((self.location[1] + i) * self.cellDimension[0], 
                                 (self.location[0] + j) * self.cellDimension[1],
                                  self.cellDimension[0], 
                                  self.cellDimension[1])
                    pygame.draw.rect(self.background, 
                                     self.colors[self.maze[self.location[0]+j]
                                                          [self.location[1]+i]], 
                                     rectangle) 

    def set_mode(self, mode):
        '''
        Sets mode attribute (see solve() method for details).
        '''
        self.mode = mode

if __name__ == '__main__':
    maze = Maze(50, 50, 2, 0.5)
    maze.set_mode(GRAPHICAL_FULL)
    path = maze.solve()
    print maze
    print path
