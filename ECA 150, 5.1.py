#Max Notes:
#-Code taken from https://codereview.stackexchange.com/questions/15304/generating-a-1d-cellular-automata-in-python
#and adapted syntactically from python 2 to 3 by adapting the print syntax
#and changing all "xrange" functions to "range". I also included all of the
#suggested changes made in the comments of that article to make it more efficient.

#Next steps:
#-Try to follow the program through step-by-step to see why it's not producing
#the grid/image correctly. There's many different places this could be getting
#stuck.

#Version 5:
#-Create a wrap-around version that starts from a random row.


#!/usr/bin/env python
'''
Code that will generate a fractal or a pseudo-random fractal
based on an initial seed and any acceptable 1-d cellular automata
algorithm.
'''
import sys
import random
import time
import pygame

class Rules(object):
    '''Contains a variety of rules that determines if a cell should turn black 
    based on the cells in the row above. Each function is namespaced inside 
    the 'Rules' class for convenience.
    '''
    
    @staticmethod
    def rule30(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, False, False], [False, True, True], [False, True, False], [False, False, True]  )
        return above in black_set

    @staticmethod
    def rule90(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, True, False], [True, False, False], [False, True, True], [False, False, True] )
        return above in black_set

    @staticmethod
    def rule110(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, True, False], [True, False, True], [False, True, True], [False, True, False], [False, False, True]  )
        return above in black_set
    
    @staticmethod
    def rule150(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [False, False, True], [False, True, False], [True, False, False], [True, True, True] )
        return above in black_set

    @staticmethod
    def rule150randomized(above):
        '''Colors a cell black if there's an odd number of black cells above it 
        (although this rule will be ignored 0.05% of the time.'''
        black_set = ( [False, False, True], [False, True, False], [True, False, False], [True, True, True] )
        if above in black_set:
            return random.randint(0, 2000) != 0
        else:
            return False

    @staticmethod
    def rule184(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, True, True], [True, False, True], [True, False, False], [False, True, True] )
        return above in black_set

class Generator(object):
    '''An object which generates a single wedge based on an initial seed
    and a rule. If the seed is `None`, a random one will be generated.'''
    def __init__(self, seed=None, rule=Rules.rule150): #test
    #def __init__(self, seed=None, rule=Rules.rule150, grid_width=200):
        self.seed = seed
        self.rule = rule
#test ->
##        self.grid_width = grid_width #`n` isn't here, so I'm not sure if it's
                                        #correct to put `grid_width` here too.

    def _generate_seed(self, seed=None):
        '''Takes a seed and converts it into an integer.
        If the seed is `None`, a random seed based on system time
        will be generated.'''
        to_int = lambda item : int(''.join([str(ord(x)) for x in str(item)]))
        if seed is None:
            return to_int(time.time())
        elif type(seed) in (int, long):
            return seed
        else:
            return to_int(seed)

#Original code
##    def _calculate_row(self, previous_row): 
##        '''Generates the next row based on the previous row.'''
##        def _above(row):
##            previous_row = [False, False]
##            previous_row.extend(row)
##            previous_row.extend([False, False])
##            for i in range(len(previous_row) - 2):
##                yield previous_row[i: i+3]
##
##        return [self.rule(i) for i in _above(previous_row)]

    def random_first_row(self, grid_width): #test
        '''Creates a first row of random cell values.'''
        values = [False, True]
        first_row = []
        for i in range(grid_width):
            first_row.append(values[random.randint(0,1)])
        return first_row

##    def random_first_row(self):
##        '''Creates a first row of random cell values.'''
##        values = [False, True]
##        first_row = []
##        for i in range(self.grid_width):
##            first_row.append(values[random.randint(0,1)])
##        return first_row

    def _calculate_row(self, previous_row): 
        '''Generates the next row based on the previous row. Includes code
        for wrap-around effect.'''
        def _above(row):
            previous_row = [row[-1]]   #wrap-around
            previous_row.extend(row)
            previous_row.extend([row[0]])   #wrap-around
            for i in range(len(previous_row) - 1): #I'm not totally sure this is adapted correctly.
                yield previous_row[i: i+2] #Maybe this should be "i+1"?

        return [self.rule(i) for i in _above(previous_row)]

    def generate(self, n=None, grid_width=10): #test
##    def generate(self, n=None):
        '''Yields n rows.'''
        row = self.random_first_row(grid_width)
        yield row
        print (row) #testing
        if n == None:
            while True:
                row = self._calculate_row(row) 
                yield row
        else:
            for i in range(n - 1):
                row = self._calculate_row(row)
                yield row
                print (row) #testing

    def create_grid(self, n, grid_width=200):
        '''Returns a `Grid` object `n` rows long, yielding
        a rectangle of size `grid_width` by `n`.'''
        height = n  
        width = grid_width
        grid = Grid(width, height)
        # Takes raw coordinates and returns new ones 
        # based on the center of the grid.

        grid.seed = self._generate_seed(self.seed)
        random.seed(grid.seed)

        #START HERE: Understand how enumerate and generate work here.
##        xc,yc = grid.center #original code, I don't think I need "center" stuff any more.
##        for index, row in enumerate(self.generate(n)):
##            raw_x = index
##            for i, cell in enumerate(row):
##                if cell:  
##                    raw_y = i - index
##                    grid.set( xc - raw_y, raw_x ) 

        xc,yc = grid.center
        for index, row in enumerate(self.generate(n)):
            raw_x = index
            for i, cell in enumerate(row):
                if cell:  
                    raw_y = i - index
                    grid.set( xc - raw_y, raw_x ) 

        return grid

    def __call__(self, *args, **kwargs):
        '''A convenience function to create a grid.'''
        return self.create_grid(*args, **kwargs)

class Grid(object):
    '''An object which holds an arbitrary grid of pixels.'''
    def __init__(self, x, y, seed=None):
        self.width = x
        self.height = y
        self.array = []
        self.center = (int(x / 2), int(1))
        # The seed used to generate the grid.
        self.seed = seed
        for i in range(self.height):
            self.array.append([False for i in range(self.width)])

    def get(self, x, y):
        return self.array[y][x]

    def set(self, x, y, value=True):
        self.array[y][x] = value

class PygameRenderer(object):
    '''Renders a grid object using Pygame, and also contains code to
    save the current grid.'''
    def __init__(self, n, grid_width, pixel_size, 
                    background=(255, 255, 255), foreground=(0, 0, 0)):
        self.pixel_size = pixel_size
        width = grid_width
        height = n - 1
        self.size = (width * self.pixel_size, 
                     height * self.pixel_size)
        self.background = background
        self.foreground = foreground

        self._configure_pygame()
        self._configure_graphics()

        self.grid = None

    def _configure_pygame(self):
        pygame.init()
        pygame.display.set_mode(self.size)
        self.surface = pygame.display.get_surface()

    def _configure_graphics(self):
        self.tile = pygame.Surface((self.pixel_size, self.pixel_size))
        self.tile.fill(self.foreground)

    def render(self, grid):
        '''Renders the grid, and prints the current seed to stdout.'''
        self.grid = grid
        self.surface.fill(self.background)
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid.get(x, y):
                    self.surface.blit(
                        self.tile,
                        (x * self.pixel_size, y * self.pixel_size)
                    )
        pygame.display.flip()
        print (self.grid.seed)

    def wait(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def refresh(self):
        '''Waits until Pygame is closed. Clicking any keyboard
        button will save the current image to the current directory,
        and clicking the mouse will break from the mainloop so that
        the containing function can create a new grid.'''
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return # Returns so that a new grid can be generated.
            elif event.type == pygame.KEYDOWN:
                filename = str(self.grid.seed) + '.png'
                pygame.image.save(self.surface, filename)
                

class AsciiRenderer(object):
    '''Creates an ASCII version of the grid.'''
    def to_string(self, grid):
        out = []
        for x in range(grid.width):
            row = ['[']
            for y in range(grid.height):
                if grid.get(x, y):
                    row.append('#')
                else:
                    row.append(' ')
            row.append(']')
            out.append(''.join(row))
        return '\n'.join(out)

    def render(self):
        print (self.to_string())


def test_rows(n=5):
    '''Tests generating a series of rows.'''
    g = Generator()
    for index, row in enumerate(g.generate(n)):
        padding = " " * (n - index - 1)
        out = "[{0}{1}{0}]"
        print (out.format(padding, "".join("#" if n else " " for n in row)))

def test_grid(n = 5, grid_width = 200, pixel_size = 16, rule=Rules.rule150):
    '''Creates a normal grid.'''
    grid = Generator(rule=rule)(n)(grid_width) #test
##    grid = Generator(rule=rule)(n) #Not sure why this works (was there before) but the below one doesn't.
    #grid = Generator(seed=None, rule=Rules.rule150, grid_width=200)
    r = PygameRenderer(n, grid_width, pixel_size)
    r.render(grid)
##    print (grid)   #I couldn't get this to work.
##    a = AsciiRenderer(grid)
##    #a.to_string(grid)
##    a.render(grid)
    while True:
        r.refresh()

def test_grid_randomized(n=256, pixel_size=1, rule=Rules.rule150randomized):
    '''Creates a randomized grid, and will repeatedly create a new one.'''
    g = Generator(rule=rule)
    r = PygameRenderer(n, pixel_size)

    while True:
        grid = g(n)
        r.render(grid)
        r.refresh()

def generate_single_random_grid(n=256, pixel_size=1, 
            rule=Rules.rule150randomized, seed=None):
    '''Creates a randomized grid.'''
    grid = Generator(rule=rule, seed=seed)(n)
    r = PygameRenderer(n, pixel_size)
    r.render(grid)
    r.refresh()

def profiling_test(n):
    Generator(rule=rule)(n)


if __name__ == '__main__':
    #test_rows()
    #test_grid(16, 4, Rules.rule150)
    #test_grid(256, 1, Rules.rule150)
    #test_grid(800, 1, Rules.rule150)
    test_grid(10, 10, 1, Rules.rule30)
    #test_grid_randomized(256, 1, Rules.rule150randomized)
    #profiling_test(256, 1, Rules.rule150)
