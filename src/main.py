from OpenGL.GLUT import *
from OpenGL.GL import *
from core.application import Application
from core.component import Component, Render
from core.openGLUtils import OpenGLUtils
from itertools import chain
import random

# Constants
GAME_SPPED = 5 # Block moves down every 60 frames

COLORS = {
  'I': (0.0, 1.0, 1.0, 1.0),
  'J': (0.0, 0.0, 1.0, 1.0),
  'L': (1.0, 0.64, 0.0, 1.0),
  'O': (1.0, 1.0, 0.0, 1.0),
  'S': (0.0, 1.0, 0.0, 1.0),
  'T': (0.5, 0.0, 0.5, 1.0),
  'Z': (1.0, 0.0, 0.0, 1.0),
}

SHAPES = {
  'I': [[True, True, True, True]],
  'J': [[True, False, False], [True, True, True]],
  'L': [[False, False, True], [True, True, True]],
  'O': [[True, True], [True, True]],
  'S': [[False, True, True], [True, True, False]],
  'T': [[False, True, False], [True, True, True]],
  'Z': [[True, True, False], [False, True, True]],
}

KEYS = list(SHAPES.keys())

def flatten(list):
  return chain.from_iterable(list)

class Tetris(Render):
    def __init__(self, cx):
        self.cx = None
        self.blocks = []
        self.falling_block = None

        self.rows = cx.width // 20
        self.columns = cx.height // 20

        self.initialize(cx)

    def initialize(self, cx):
        self.blocks = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.spawn_new_block(cx)

    def render(self, cx):
        if cx.frame % GAME_SPPED == 0:
          self.update()

        return list(
          flatten(
            [
              flatten(self.blocks),
              self.falling_block.blocks if self.falling_block else []
            ]
          )
        )

    def spawn_new_block(self, cx):
        block_type = random.choice(KEYS)
        spawn_position = (self.rows // 2, self.columns - 1)
        new_block = []

        block_shape = SHAPES[block_type]
        block_color = COLORS[block_type]

        for row in range(len(block_shape)):
          for column in range(len(block_shape[row])):
            if block_shape[row][column]:
              new_block.append(Block(block_color, spawn_position[0] + column, spawn_position[1] - row))

        self.falling_block = FallingBlock(new_block)

    def update(self):
      if self.check_collision():
        self.register_blocks(self.falling_block.blocks)
        self.falling_block = None
        self.spawn_new_block(self.cx)
      else:
        self.falling_block.fall()

    def register_blocks(self, blocks):
      for block in blocks:
        self.blocks[block.y][block.x] = block

    def check_collision(self):
      for block in self.falling_block.get_blocks():
        if block.y <= 0:
          return True

        if self.blocks[block.y - 1][block.x] is not None:
          return True

    @staticmethod
    def new(cx):
        return Tetris(cx)

class Block(Component):
  def __init__(self, color, x, y):
    super().__init__()
    self.color = color
    self.x = x
    self.y = y

  def render(self, cx):
    x, y = OpenGLUtils.convert_to_normalized_coordinates(self.x * 20, self.y * 20, cx.width, cx.height)
    width, height = OpenGLUtils.convert_to_normalized_size(20, 20, cx.width, cx.height)

    glPushMatrix()
    glTranslatef(x, y, 0)  # Position the rectangle
    glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])  # Set the rectangle color
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(0, height)
    glVertex2f(width, height)
    glVertex2f(width, 0)
    glEnd()
    glPopMatrix()

  def move_down(self):
    self.y -= 1

class FallingBlock(object):
  def __init__(self, blocks):
    self.blocks = blocks

  def fall(self):
    for block in self.blocks:
      block.move_down()

  def can_fall(self):
    return True

  def get_blocks(self):
    return self.blocks

if __name__ == '__main__':
  Application().run(lambda cx: Tetris.new(cx))
