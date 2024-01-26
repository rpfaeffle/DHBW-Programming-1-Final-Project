from OpenGL.GLUT import *
from OpenGL.GL import *
from core.application import Application
from core.component import Component, Render
from core.openGLUtils import OpenGLUtils
from itertools import chain
import random

from components.block import Block
from components.line import Line
from components.shape import Shape, ShapeProps
from constants import *
from utils import flatten

class Tetris(Render):
    def __init__(self, cx):
        self.cx = None
        self.blocks = []
        self.lines = []
        self.falling_block = None

        self.rows = cx.width // BLOCK_SIZE
        self.columns = cx.height // BLOCK_SIZE

        self.initialize(cx)

    def initialize(self, cx):
        cx.input.register(b'a', 0, lambda: self.move_block('left'))
        cx.input.register(b'd', 0, lambda: self.move_block('right'))
        self.blocks = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.lines = [
          Line((0, i * BLOCK_SIZE), (cx.width, i * BLOCK_SIZE)) for i in range(self.columns)
        ] + [
          Line((i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, cx.height)) for i in range(self.rows)
        ]
        self.spawn_new_block(cx)

    def render(self, cx):
        glClearColor(0.9, 0.9, 0.9, 1.0)  # Set the background color to gray

        if cx.frame % GAME_SPEED == 0:
          self.update()

        blocks = list(flatten(self.blocks))
        falling_blocks = self.falling_block.blocks if self.falling_block else []

        return blocks + falling_blocks + self.lines

    def spawn_new_block(self, cx):
        block_type = random.choice(KEYS)
        spawn_position = (self.rows // 2, self.columns - 1)
        new_block = []

        self.falling_block = Shape(ShapeProps(
          color=COLORS[block_type],
          shape=POSITIONS[block_type],
          origin=ROTATION_ORIGINS[block_type],
        ), spawn_position, self.is_position_vacant)

    def move_block(self, direction):
      if direction == 'left':
        for block in self.falling_block.get_blocks():
          if not self.is_position_vacant((block.x - 1, block.y)):
            return

        self.falling_block.move_horizontally('left')
      elif direction == 'right':
        for block in self.falling_block.get_blocks():
          if not self.is_position_vacant((block.x + 1, block.y)):
            return

        self.falling_block.move_horizontally('right')

    def update(self):
      if self.check_collision():
        self.register_blocks(self.falling_block.blocks)
        self.falling_block = None
        self.spawn_new_block(self.cx)
      else:
        self.falling_block.rotate_shape(True)
        self.falling_block.fall()

    def register_blocks(self, blocks):
      for block in blocks:
        self.blocks[block.y][block.x] = block

    def check_collision(self):
      for block in self.falling_block.get_blocks():
        if not self.is_position_vacant((block.x, block.y - 1)):
          return True
      return False

    def is_position_vacant(self, position):
      """
      Check if a given position is vacant in the grid.

      Parameters:
        - position (tuple): The position to check in the format (row, column).

      Returns:
        - bool: True if the position is vacant, False otherwise.
      """
      if position[1] >= 0 and position[0] >= 0 and position[0] < self.rows:
        if position[1] >= self.columns:
          return True
        return self.blocks[position[1]][position[0]] is None
      return False

    @staticmethod
    def new(cx):
        return Tetris(cx)

if __name__ == '__main__':
  Application().run(lambda cx: Tetris.new(cx))
