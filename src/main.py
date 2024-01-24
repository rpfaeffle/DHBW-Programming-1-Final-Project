from OpenGL.GL import *
from core.application import Application
from core.component import Component, Render
from core.openGLUtils import OpenGLUtils

# Constants
GAME_SPEED = 60 # Block moves down every 60 frames

class Tetris(Render):
    def __init__(self, cx):
        self.cx = None
        self.blocks = []
        self.initialize(cx)

    def initialize(self, cx):
        self.spawn_new_block(cx)

    def render(self, cx):
        print(cx.frame)
        if cx.frame % GAME_SPEED == 0:
          self.update()

        return self.blocks

    def spawn_new_block(self, cx):
        spawn_position = (0, cx.height)
        self.blocks.append(Block((1.0, 0.0, 0.0, 1.0), spawn_position[0], spawn_position[1]))
        pass

    def update(self):
        print(self.blocks)
        for block in self.blocks:
          if block.isFalling:
            block.move_down()

    @staticmethod
    def new(cx):
        return Tetris(cx)

class Block(Component):
  def __init__(self, color, x, y):
    super().__init__()
    self.color = color
    self.x = x
    self.y = y
    self.isFalling = True

  def render(self, cx):
    x, y = OpenGLUtils.convert_to_normalized_coordinates(self.x, self.y, cx.width, cx.height)
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
    print(self.y)
    self.y -= 20

if __name__ == '__main__':
  Application().run(lambda cx: Tetris.new(cx))
