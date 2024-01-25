from OpenGL.GLUT import *
from OpenGL.GL import *
from core.application import Application
from core.component import Component, Render
from core.openGLUtils import OpenGLUtils
from itertools import chain
import random

from components.block import Block
from components.shape import Shape
from constants import GAME_SPEED, COLORS, POSITIONS, KEYS, ROTATION_ORIGINS
from utils import flatten

class Tetris(Render):
    def __init__(self, cx):
        self.cx = None
        self.blocks = []
        self.falling_block = None

        self.rows = cx.width // 20
        self.columns = cx.height // 20

        self.initialize(cx)

    def initialize(self, cx):
        cx.input.register(b'a', 0, lambda: self.move_block('left'))
        cx.input.register(b'd', 0, lambda: self.move_block('right'))
        self.blocks = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.spawn_new_block(cx)

    def render(self, cx):
        glClearColor(0.9, 0.9, 0.9, 1.0)  # Set the background color to gray

        if cx.frame % GAME_SPEED == 0:
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

        self.falling_block = Shape({
          'color': COLORS[block_type],
          'shape': POSITIONS[block_type],
          'origin': ROTATION_ORIGINS[block_type],
        }, spawn_position)

    def move_block(self, direction):
      if direction == 'left':
        for block in self.falling_block.get_blocks():
          if block.x <= 0:
            return

          if self.blocks[block.y][block.x - 1] is not None:
            return

        for block in self.falling_block.get_blocks():
          block.x -= 1
      elif direction == 'right':
        for block in self.falling_block.get_blocks():
          if block.x >= self.rows - 1:
            return

          if self.blocks[block.y][block.x + 1] is not None:
            return

        for block in self.falling_block.get_blocks():
          block.x += 1

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
        if block.y >= len(self.blocks) - 1:
          return False

        if block.y <= 0:
          return True

        if self.blocks[block.y - 1][block.x] is not None:
          return True

    @staticmethod
    def new(cx):
        return Tetris(cx)

if __name__ == '__main__':
  Application().run(lambda cx: Tetris.new(cx))
