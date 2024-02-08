import argparse
import datetime
import logging
import operator
import os
import pygame
import random
import re

# Constants
MIN_WND_SIZE = 200 # Minimum for window height or width.
MIN_SNAKE_LEN = 2 # Minimum length of the snake.
MIN_TILE_SIZE = 10 # Minimum for tile size.
MIN_NB_ROWS = 12
MIN_NB_COLS = 20
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
HALT = (0, 0)
BLACK = '#000000'
WHITE = '#ffffff'
RED = '#ff0000'
GREEN = '#00ff00'
BLUE = '#0000ff'
FPS = 5
WIDTH = 640
HEIGHT = 480
MAX_HIGH_SCORES = 5
SNAKE_INIT_LENGTH = 3
TILE_SIZE = 20
SCORE_FILE = os.path.join(os.environ['HOME'], '.snake_scores.txt')

def read_args():
    """Read command line arguments."""

    # Define parser
    parser = argparse.ArgumentParser(
            description='An implementation of the Snake & Fruit game.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--bg-color-1', help='Background color 1.',
            default=WHITE)
    parser.add_argument('--bg-color-2', help='Background color 2.',
            default=BLACK)
    parser.add_argument('--height', help='Window height', type=int,
            default=HEIGHT)
    parser.add_argument('--width', help='Window width', type=int, default=WIDTH)
    parser.add_argument('--fps', help='Number of frames per second', type=int,
            default=FPS)
    parser.add_argument('--fruit-color', help='Fruit color.',
            default=RED)
    parser.add_argument('-G', '--gameover-on-exit',
            help='Terminate game when snake exit window.', action='store_true')
    parser.add_argument('-g', '--debug', help='Set debug mode.',
            action='store_true')
    parser.add_argument('--high-scores-file', default=SCORE_FILE,
            help="The path to the file in which to store high scores.")
    parser.add_argument('--max-high-scores', type=int, default=MAX_HIGH_SCORES,
            help='The maximum of high scores to store')
    parser.add_argument('--snake-color', help='Snake color.',
            default=GREEN)
    parser.add_argument('--snake-init-length', '--snake-length',
            help='The initial length of the snake', type=int,
            default=SNAKE_INIT_LENGTH)
    parser.add_argument('--tile-size', help='Tile size', type=int,
            default=TILE_SIZE)
    
    # Parse arguments
    args = parser.parse_args()

    # Enable debug messages
    if args.debug:
        logger.setLevel(logging.DEBUG)

    return args

def get_random_number(first, last):

    # Init random seed with system clock (default)
    random.seed()

    return random.randint(first, last)

# *** EXPLANATION ***
# SOME CLASSES NOW INHERIT FROM SUPER CLASSES.
# *******************
    
# Game over exception
class GameOver(Exception):
    pass

class Score:
    
    def __init__(self, score=0, name=None):
        self._score = score
        self._name = name

    def get(self):
        return self._score
        
    def toInt(self):
        return self.get()
    
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name

    def addPoints(self, points):
        self._score += points
    
    def __lt__(self, other):
        return (self._name < other._name if self._score == other._score else
                self._score < other._score)

    def __eq__(self, other):
        return self._score == other._score and self._name == other._name

    @classmethod
    def fromString(cls, s):
        (name, score) = s.split(',') # Split line in two
        score = int(score) # Convert from string to integer
        return cls(name=name, score=score)

    def toString(self):
        return "%s,%d" % ("Unknown" if self._name is None else self._name,
                self._score)

class Scores:
    
    def __init__(self, file, max_scores=None):
        if file is None:
            raise ValueError("You must provide a valid path for a file.")
        self._file = file
        self._scores = []
        self._max_scores = max_scores 
        self.load()

    def getSize(self):
        return len(self._scores)

    def get(self, index):
        if index < len(self._scores):
            return self._scores[index]
        return None

    def load(self):
        
        # Test if file exists
        if os.path.exists(self._file):

            # Open file for reading
            with open(self._file, 'r') as f:

                # Loop on all lines
                for line in f:
                    line = line.rstrip() # Get rid of new line character
                    logger.debug("Line in scores file: %s" % line)
                    self._scores.append(Score.fromString(line)) # Add to list

    def save(self):
        
        # Open file for writing
        with open(self._file, 'w') as f:

            # Loop on all scores
            for score in self._scores:
                print(score.toString(), file=f)

    def setMax(self, max_scores):
        self._max_scores = max_scores
        self._shorten_scores()

    def _shorten_scores(self):

        self._scores.sort()
        if self._max_scores is not None and len(self._scores) > self._max_scores:
            self._scores[0:len(self._scores) - self._max_scores] = []

    def addScore(self, new_score):

        # Add new score
        if new_score.get() > 0 and (self._max_scores is None
                or len(self._scores) < self._max_scores
                or len(self._scores) == 0 or
                new_score.get() > self._scores[0].get()):
            if new_score.getName() is None:
                new_score.setName(input("Write your name: "))
            self._scores.append(new_score)

        self._shorten_scores()

    def print(self):
        
        if len(self._scores) > 0:
            logger.info("\nHIGH SCORES:")
            for score in sorted(self._scores, reverse=True):
                logger.info("  %s: %d" % (score.getName(), score.get()))

class Board:

    def __init__(self, width, height, tile_size):
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._objects = []
        self._removed_objects = []

        # Check arguments
        if self._height < MIN_WND_SIZE or self._width < MIN_WND_SIZE:
            raise ValueError(("Window height and width must be greater or " +
                "equal to %d.") % MIN_WND_SIZE)
        if self._tile_size < MIN_TILE_SIZE:
            raise ValueError("Tile size must be greater or equal to %d."
                    % MIN_TILE_SIZE)
        if (self._height % self._tile_size != 0 or
                self._width % self._tile_size != 0):
            raise ValueError(("Window width (%d) and window height (%d) must" +
                " be dividable by the tile size (%d).") % (self._width,
                    self._height, self._tile_size))
        if self._width // self._tile_size < MIN_NB_COLS:
            raise ValueError(("Number of columns must be greater or equal to" + 
                " %d, but width / tile_size = %d / %d = %d.") % (MIN_NB_COLS,
                    self._width, self._tile_size,
                    self._width // self._tile_size))
        if self._height // self._tile_size < MIN_NB_ROWS:
            raise ValueError(("Number of rows must be greater or equal to" + 
                " %d, but height / tile_size = %d / %d = %d.") % (MIN_NB_ROWS,
                    self._height, self._tile_size,
                    self._height // self._tile_size))

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def getNbCols(self):
        return self._width // self._tile_size

    def getNbRows(self):
        return self._height // self._tile_size

    def getRandomTile(self, color=BLUE):
        return Tile(col=get_random_number(0, self.getNbCols() - 1),
                row=get_random_number(0, self.getNbRows() - 1), color=color)

    def drawTiles(self, screen, tiles):
        
        # Loop on all tiles
        for tile in tiles:

            # Is tile inside board?
            if (tile.getCol() >= 0 and tile.getCol() < self.getNbCols()
                    and tile.getRow() >= 0
                    and tile.getRow() < self.getNbRows()):

                # Compute rectangle
                tile_rect = pygame.Rect(tile.getCol() * self._tile_size,
                        tile.getRow() * self._tile_size,
                        self._tile_size, self._tile_size)
                
                # Draw tile
                pygame.draw.rect(screen, tile.getColor(), tile_rect)

    def drawObjects(self, screen):
        for obj in self._objects:
            obj.draw(screen)

    def addObject(self, obj):
        self._objects.append(obj)

    def removeObject(self, obj):
        self._objects.remove(obj)
        self._removed_objects.append(obj)
        
    def notifyMovement(self, obj):

        intersected = self.getIntersectedObjects(obj)
        
        for other in intersected:
            obj.notifyCollision(other)
            other.notifyCollision(obj)

    def getIntersectedObjects(self, obj):

        intersected = []
        for other in self._objects:
            if other != obj and obj.intersectsWith(other):
                intersected.append(other)
                
        return intersected
        
    def intersectsWithObjects(self, obj):

        logger.debug("Check if object %s intersects with others." % str(obj))
        for other in self._objects:
            logger.debug("other object: %s" % str(other))
            if other != obj and obj.intersectsWith(other):
                logger.debug("Object %s intersects with %s." % (str(obj),
                    str(other)))
                return True
            
        logger.debug("No intersection found for object %s." % str(obj))
        return False

    def countObjectType(self, cls):

        n = 0
        
        for obj in self._objects:
            if isinstance(obj, cls):
                n += 1
                
        return n

class Tile:
    
    def __init__(self, col, row, color=None):
        self._row = row
        self._col = col
        self._color = None if color is None else pygame.Color(color)

    def getCol(self):
        return self._col

    def getRow(self):
        return self._row

    def setCol(self, col):
        self._col = col

    def setRow(self, row):
        self._row = row

    def getColor(self):
        return self._color

    def translate(self, direction):
        return Tile(col=self._col + direction[0],
                row=self._row + direction[1],
                color=self._color)

    def __repr__(self):
        return "[%d, %d]" % (self._col, self._row)
    
    def __eq__(self, other):
        return self._col == other._col and self._row == other._row
    
    def __lt__(self, other):

        if self._col == other._col:
            return self._row < other._row

        return self._col < other._col

class Factory:
    def __init__(self, board):
        self._board = board
        self._fruits = {}

    def declareFruit(self, name, color, points):
        self._fruits[name] = {'color': color, 'points': points}

    def createFruit(self, name):
        
        for name2 in self._fruits:
            bool = False
            if name == name2:
                bool = True

        if bool == False:
            raise ValueError("Unknown fruit \"%s\"." % name)

        color = self._fruits[name]['color']
        points = self._fruits[name]['points']

        fruit = None
        while fruit is None or self._board.intersectsWithObjects(fruit):
            fruit = Fruit(board=self._board,
                    tile=self._board.getRandomTile(color=color),
                    points=points)

        self._board.addObject(fruit)

        return fruit
    
    def createSnake(self, length, color=GREEN, **args):


class GameObject:

    def __init__(self, board, tiles=None):
        self._board = board
        self._tiles = None if tiles is None else tiles.copy()

    def getTiles(self):
        return self._tiles.copy()

    def intersectsWith(self, other):
        
        logger.debug("Generic intersection test between 2 objects.")
        if not isinstance(other, GameObject):
            raise ValueError("`other` must be a GameObject.")

        if (self._tiles is None or other._tiles is None
                or isinstance(self, BackgroundObject)
                or isinstance(other, BackgroundObject)):
            return False

        intersect = [tile for tile in self._tiles if tile in other._tiles]
        
        return len(intersect) > 0

    def isEatable(self):
        return False

    def notifyCollision(self, other):
        pass

    def draw(self, screen):
        if self._tiles is not None:
            self._board.drawTiles(screen, self._tiles)

class MovingObject(GameObject):

    def __init__(self, board, tiles, direction):
        super().__init__(board, tiles)
        self._direction = direction

    def move(self):
        raise Exception("move() method not implemented.")

class BackgroundObject(GameObject):
    pass

class CheckerBackground(BackgroundObject):

    def __init__(self, board, color_1=WHITE, color_2=BLACK):
    
        # Create tiles
        tiles = []
        # Loop on all rows and columns
        for i in range(board.getNbCols()):
            for j in range(board.getNbRows()):
                
                # Alternate color
                tile_color = color_1 if (i + j) % 2 == 0 else color_2
                
                # New tile
                tiles.append(Tile(col=i, row=j, color=tile_color))

        # Call super class
        super().__init__(board, tiles)

class Fruit(GameObject):

    def __init__(self, board, tile, points=1):
        super().__init__(board, [tile])
        self._points = points
        self._eaten = False

    @classmethod
    def createRandom(cls, board, color=RED, **args):
        
        fruit = None

        # We search for a random place of the fruit that does no collide with
        # the snake.
        while fruit is None or board.intersectsWithObjects(fruit):
            fruit = cls(board, tile=board.getRandomTile(color=color), **args)
        
        return fruit

    def isEatable(self):
        return True

    def getPoints(self):
        return self._points

    def notifyEaten(self):
        self._board.removeObject(self)

class Snake(MovingObject):

    def __init__(self, board, tiles, direction, gameover_on_exit=True):
        super().__init__(board, tiles=tiles, direction=direction)
        self._score = Score()
        self._gameover_on_exit = gameover_on_exit
        self._length = len(tiles)

    @classmethod
    def createRandom(cls, board, length, color=GREEN, **args):

        # Check arguments
        if length < MIN_SNAKE_LEN:
            raise ValueError("Snake length must be greater or equal to %d." %
                    MIN_SNAKE_LEN)

        # Set first cell randomly
        init_pos = board.getRandomTile(color=color)
        tiles = [init_pos]
        
        # Get random direction
        snake_dir = [LEFT, RIGHT, UP, DOWN][get_random_number(0, 3)]
        
        # Make other cells
        for i in range(length - 1):
            x = tiles[-1].getCol() + snake_dir[0]
            y = tiles[-1].getRow() + snake_dir[1]
            if x < 0:
                x = 0
            if x >= board.getNbCols():
                x = board.getNbCols() - 1
            if y < 0:
                y = 0
            if y >= board.getNbRows():
                y = board.getNbRows() - 1
            tiles.append(Tile(col=x, row=y, color=color))

        return cls(board, tiles=tiles, direction=snake_dir, **args)

    def getScore(self):
        return self._score

    def getHeadTile(self):
        return self._tiles[-1]
    
    def setDirection(self, direction):
        self._direction = direction

    def hasTile(self, tile):
        return tile in self._tiles

    def notifyCollision(self, other):
        
        if other.isEatable():
            self._length += 1
            self._score.addPoints(other.getPoints())
            other.notifyEaten()

    def move(self):

        # Make snake grow (i.e.: compute new head)
        new_head = self._tiles[-1].translate(self._direction)

        # Game over if exit window
        if self._gameover_on_exit:
            if (new_head.getCol() < 0 or
                    new_head.getCol() >= self._board.getNbCols() or
                    new_head.getRow() < 0 or
                    new_head.getRow() >= self._board.getNbRows()):
                raise GameOver()

        # Snake continues on opposite side of the window  
        else: 
            if new_head.getCol() < 0: # Exit left
                new_head.setCol(self._board.getNbCols() - 1)
            elif new_head.getCol() >= self._board.getNbCols(): # Exit right
                new_head.setCol(0)
            elif new_head.getRow() < 0: # Exit top
                new_head.setRow(self._board.getNbRows() - 1)
            elif new_head.getRow() >= self._board.getNbRows(): # Exit bottom
                new_head.setRow(0)
                
        # Detect collision on itself
        if new_head in self._tiles:
            raise GameOver()
            
        # Append new head
        self._tiles.append(new_head)

        # Notify board that this snake has moved
        self._board.notifyMovement(self)

        # Shorten snake
        while len(self._tiles) > self._length:
            del(self._tiles[0])

class Game:

    def __init__(self, width=WIDTH, height=HEIGHT, tile_size=TILE_SIZE,
            max_high_scores=MAX_HIGH_SCORES,
            snake_init_length=SNAKE_INIT_LENGTH, high_score_file=SCORE_FILE,
            bg_color_1=WHITE, bg_color_2=BLACK, fruit_color=RED,
            snake_color=GREEN, fps=FPS, gameover_on_exit=False,
            **_): # **_ ignore remaining arguments

        self._max_high_scores = max_high_scores
        self._high_score_file = high_score_file
        self._fps = fps

        # Check color arguments using regular expressions.
        color_re = re.compile(r'^#[0-9a-f]{6}$')
        if not re.match(color_re, fruit_color):
            raise ValueError("Bad format for fruit color %s."
                    % fruit_color)
        if not re.match(color_re, snake_color):
            raise ValueError("Bad format for snake color %s."
                    % snake_color)
        if not re.match(color_re, bg_color_1):
            raise ValueError("Bad format for background color 1 %s." %
                    bg_color_1)
        if not re.match(color_re, bg_color_2):
            raise ValueError("Bad format for background color 2 %s." %
                    bg_color_2)

        # Initialize the Pygame library.
        # This is a special step needed by Pygame. Most (99%) libraries do not
        # need an initialization step.
        logger.debug("Initialize Pygame.")
        pygame.init()
        
        # Create a screen for display, choosing its size (width x height).
        logger.debug("Create Pygame screen.")
        self._screen = pygame.display.set_mode((width, height))

        # Create a clock object that we will use to control the speed of our
        # game.
        logger.debug("Create Pygame clock.")
        self._clock = pygame.time.Clock()

        # Create the game space
        logger.debug("Create Board instance.")
        self._board = Board(width=width, height=height, tile_size=tile_size)

        # Create the checkerboard background
        logger.debug("Create background instance.")
        self._board.addObject(CheckerBackground(self._board, color_1=bg_color_1,
                color_2=bg_color_2))

        # Create snake
        logger.debug("Create Snake instance.")
        self._snake = Snake.createRandom(self._board,
                length=snake_init_length,
                color=snake_color, gameover_on_exit=gameover_on_exit)
        self._board.addObject(self._snake)
        
        # Create first fruit
        logger.debug("Create first Fruit instance.")
        self._board.addObject(Fruit.createRandom(self._board,
            color=fruit_color))

    def _process_events(self):
        """Process new events (keyboard, mouse)."""

        for event in pygame.event.get():
            
            # Catch selection of exit icon (Window "cross" icon)
            if event.type == pygame.QUIT:
                raise GameOver()

            # Catch a key press
            elif event.type == pygame.KEYDOWN:
                
                # "Q" key has been pressed
                if event.key == pygame.K_q:
                    raise GameOver()
        
                # Arrow keys
                elif event.key == pygame.K_UP:
                    self._snake.setDirection(UP)
                elif event.key == pygame.K_DOWN:
                    self._snake.setDirection(DOWN)
                elif event.key == pygame.K_RIGHT:
                    self._snake.setDirection(RIGHT)
                elif event.key == pygame.K_LEFT:
                    self._snake.setDirection(LEFT)

    def _update_objects(self):
        
        # Update snake
        self._snake.move()

        # Create new fruit if needed
        if self._board.countObjectType(Fruit) == 0:
            self._board.addObject(Fruit.createRandom(board=self._board,
                color=RED))
        
    def _update_display(self):
        
        # Draw all objects
        self._board.drawObjects(self._screen)

        # Update title with score.
        pygame.display.set_caption("Snake - score: %d"
                % self._snake.getScore().get())

        # Display the display
        pygame.display.update()

    def _process_score(self):

        logger.info("\nScore: %d." % self._snake.getScore().get())
        
        # Read table from file
        scores = Scores(file=self._high_score_file,
                max_scores=self._max_high_scores) 

        # Update table
        scores.addScore(self._snake.getScore())
        
        # Print table
        scores.print()
        
        # Save table to file
        scores.save()

    def start(self):

        # Loop forever
        logger.debug("Start main loop.")
        try:
            while True:
                
                # Wait 1/FPS of a second, starting from last display or now
                self._clock.tick(self._fps)
                
                self._process_events()
                self._update_objects()
                self._update_display()

        except GameOver:
            pass

        logger.info("\nGame over.")

        # Terminate Pygame
        pygame.quit()
        self._process_score()

def main():

    logger.debug("Start main function.")
    # Read command line arguments
    args = read_args()

    # Create the game instance
    logger.debug("Create Game instance.")
    game = Game(**vars(args)) # vars() transforms mapping (args) into
                              # a dictionary

    # Run the game instance
    logger.debug("Start Game instance.")
    game.start()

# Create a logger for this module
logger = logging.getLogger(__name__)
        
if __name__ == "__main__":

    import sys

    # Setup the logger
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Call main function
    main()

    # Quit program properly
    quit(0)