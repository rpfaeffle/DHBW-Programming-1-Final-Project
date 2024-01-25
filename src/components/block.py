from OpenGL.GL import *
from core.component import Component
from core.openGLUtils import OpenGLUtils

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
    glColor4f(*self.color)  # Set the rectangle color
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(0, height)
    glVertex2f(width, height)
    glVertex2f(width, 0)
    glEnd()
    glPopMatrix()

  def move_down(self):
    self.y -= 1
