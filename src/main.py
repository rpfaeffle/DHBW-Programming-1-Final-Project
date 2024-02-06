from typing import Optional

import OpenGL.GL as gl
from components.text import Text
from core.application import Application
from core.component import Render
import random
import math

from components.block import Block
from components.line import Line
from components.score import Score
from components.shape import Shape, ShapeProps
import constants as const
from utils import color, flatten

class Tetris(Render):
    def __init__(self, cx):
        self.blocks: list[list[Optional[Block]]] = []
        self.lines: list[Line] = []
        self.score = Score()
        self.falling_block: Optional[Shape] = None
        self.falling_speed = const.GAME_SPEED
        self.tetrises = 0
        self.game_over = False
        self.paused = False

        self.columns = cx.width // const.BLOCK_SIZE
        self.rows = const.TOTAL_ROWS

        self.update_game_speed()
        self.initialize(cx)

    def update_game_speed(self):
        # Formula based on https://harddrop.com/wiki/Tetris_Worlds
        self.falling_speed = int(const.GAME_SPEED * math.pow(0.8 - ((self.score.level - 1) * 0.007), self.score.level - 1))

    def setup_event_listeners(self, cx):
        """
        Setup event listeners for the game.
        """
        cx.input.register(const.Keys.LEFT_ARROW.value, 0, lambda: self.move_block(const.Direction.LEFT))
        cx.input.register(const.Keys.RIGHT_ARROW.value, 0, lambda: self.move_block(const.Direction.RIGHT))
        cx.input.register(const.Keys.DOWN_ARROW.value, 0, lambda: self.update())
        cx.input.register(const.Keys.SPACEBAR.value, 0, lambda: self.hard_drop())
        cx.input.register(b'z', 0, lambda: self.falling_block.rotate_shape(const.RotationAngles.CLOCKWISE))
        cx.input.register(b'c', 0, lambda: self.falling_block.rotate_shape(const.RotationAngles.COUNTER_CLOCKWISE))
        cx.input.register(b'r', 0, lambda: self.reset_game() if not self.paused else self.resume_game())
        cx.input.register(const.Keys.ESC.value, 0, lambda: self.pause_game())

    def initialize(self, cx):
        self.setup_event_listeners(cx)
        self.blocks = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.lines = [
          Line((0, i * const.BLOCK_SIZE), (cx.width, i * const.BLOCK_SIZE)) for i in range(self.rows)
        ] + [
          Line((i * const.BLOCK_SIZE, 0), (i * const.BLOCK_SIZE, cx.height)) for i in range(self.columns)
        ]
        self.spawn_new_block()


    def render(self, cx):
        if self.game_over:
          gl.glClearColor(*color(0, 0, 0))
          return Text("Game Over", cx.width // 2, cx.height // 2, center=True)

        if self.paused:
          gl.glClearColor(*color(0, 0, 0))
          return Text("Pause\n\nCmd + Q\nto close\n\nr to continue", cx.width // 2, cx.height // 2, center=True)

        gl.glClearColor(*color(230, 230, 230))

        if cx.frame % self.falling_speed == 0 and not self.game_over:
          self.update()

        blocks = flatten(self.blocks)
        falling_blocks = self.falling_block.blocks if self.falling_block else []

        return blocks + falling_blocks + self.lines + [self.score]

    def spawn_new_block(self):
        block_type = random.choice(const.SHAPE_IDS)
        spawn_position = (self.columns // 2, const.VISIBLE_ROWS + 1)

        self.falling_block = Shape(ShapeProps(
          color=const.COLORS[block_type],
          shape=const.POSITIONS[block_type],
          origin=const.ROTATION_ORIGINS[block_type],
        ), spawn_position, self.is_position_vacant)

    def move_block(self, direction: const.Direction):
      """
      Move the falling block in the given direction if the position is vacant.
      """
      for block in self.falling_block.blocks:
        if not self.is_position_vacant((block.x + direction.value, block.y)):
          return

      self.falling_block.move_horizontally(direction)

    def hard_drop(self):
      """
      Move the falling block to the lowest possible position.
      """
      while not self.check_collision():
        self.falling_block.fall()
      self.update()

    def update(self):
      if self.check_collision():
        self.register_blocks(self.falling_block.blocks)

        if self.check_game_over():
          self.game_over = True
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
        self.tetrises += rows
        if rows == 1:
            self.score.score += 40
        elif rows == 2:
            self.score.score += 100
        elif rows == 3:
            self.score.score += 300
        elif rows == 4:
            self.score.score += 1200

        # Advance level if tetrises is greater than or equal to the current level * 10 + 10
        if self.tetrises >= self.score.level * 10 + 10:
            self.tetrises = 0
            self.score.level += 1
            self.update_game_speed()

    def check_game_over(self):
        return not all(block is None for block in self.blocks[const.VISIBLE_ROWS])

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

    def reset_game(self):
        if self.game_over:
          self.blocks = [[None for _ in range(self.columns)] for _ in range(self.rows)]
          self.score = Score()
          self.tetrises = 0
          self.game_over = False
          self.spawn_new_block()

    def pause_game(self):
        self.paused = True

    def resume_game(self):
        self.paused = False

    @staticmethod
    def new(cx):
        return Tetris(cx)

if __name__ == '__main__':
  Application(None, [200, 500]).run(lambda cx: Tetris.new(cx))
