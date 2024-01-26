import OpenGL.GL as gl
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
        self.blocks = []
        self.lines = []
        self.falling_block = None
        self.score = 0
        self.game_over = False

        self.columns = cx.width // BLOCK_SIZE
        self.rows = TOTAL_ROWS

        self.initialize(cx)

    def initialize(self, cx):
        cx.input.register(Keys.LEFT_ARROW.value, 0, lambda: self.move_block(Direction.LEFT))
        cx.input.register(Keys.RIGHT_ARROW.value, 0, lambda: self.move_block(Direction.RIGHT))
        cx.input.register(Keys.DOWN_ARROW.value, 0, lambda: self.update())
        cx.input.register(b'z', 0, lambda: self.falling_block.rotate_shape(False))
        cx.input.register(b'c', 0, lambda: self.falling_block.rotate_shape(True))
        self.blocks = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.lines = [
          Line((0, i * BLOCK_SIZE), (cx.width, i * BLOCK_SIZE)) for i in range(self.rows)
        ] + [
          Line((i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, cx.height)) for i in range(self.columns)
        ]
        self.spawn_new_block()

    def render(self, cx):
        gl.glClearColor(0.9, 0.9, 0.9, 1.0)  # Set the background color to gray

        if cx.frame % GAME_SPEED == 0 and not self.game_over:
          self.update()

        blocks = list(flatten(self.blocks))
        falling_blocks = self.falling_block.blocks if self.falling_block else []

        return blocks + falling_blocks + self.lines

    def spawn_new_block(self):
        block_type = random.choice(KEYS)
        spawn_position = (self.columns // 2, VISIBLE_ROWS + 1)
        new_block = []

        self.falling_block = Shape(ShapeProps(
          color=COLORS[block_type],
          shape=POSITIONS[block_type],
          origin=ROTATION_ORIGINS[block_type],
        ), spawn_position, self.is_position_vacant)

    def move_block(self, direction: Direction):
      if direction == Direction.LEFT:
        for block in self.falling_block.blocks:
          if not self.is_position_vacant((block.x - 1, block.y)):
            return

        self.falling_block.move_horizontally(direction)
      elif direction == Direction.RIGHT:
        for block in self.falling_block.blocks:
          if not self.is_position_vacant((block.x + 1, block.y)):
            return

        self.falling_block.move_horizontally(direction)

    def update(self):
      if self.check_collision():
        self.register_blocks(self.falling_block.blocks)

        if self.check_game_over():
          self.game_over = True
          print("Game Over")
          return

        self.remove_full_rows()
        self.falling_block = None
        self.spawn_new_block()
      else:
        self.falling_block.fall()

    def remove_full_rows(self):
        rows_to_remove = []
        for i in range(self.columns):
            if all(self.blocks[i]):
                rows_to_remove.append(i)
        for row in reversed(rows_to_remove):
            self.move_all_blocks_down(row)
            self.blocks.pop(row)
            self.blocks.append([None for _ in range(self.columns)])
        self.update_score(len(rows_to_remove))

    def update_score(self, rows):
        if rows == 1:
            self.score += 40
        elif rows == 2:
            self.score += 100
        elif rows == 3:
            self.score += 300
        elif rows == 4:
            self.score += 1200
        print(f"Score: {self.score}")

    def check_game_over(self):
        return not all(block is None for block in self.blocks[VISIBLE_ROWS])

    def move_all_blocks_down(self, row):
      for i in range(row, self.rows):
        for j in range(self.columns):
          if self.blocks[i][j]:
            self.blocks[i][j].move_down()

    def register_blocks(self, blocks):
      for block in blocks:
        self.blocks[block.y][block.x] = block

    def check_collision(self):
      for block in self.falling_block.blocks:
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
      if position[1] >= 0 and position[0] >= 0 and position[0] < self.columns:
        if position[1] >= self.rows:
          return True
        return self.blocks[position[1]][position[0]] is None
      return False

    @staticmethod
    def new(cx):
        return Tetris(cx)

if __name__ == '__main__':
  Application(None, [200, 400]).run(lambda cx: Tetris.new(cx))
