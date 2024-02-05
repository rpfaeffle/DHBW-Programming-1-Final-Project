import OpenGL.GL as gl
from core.component import Component
from components.text import Text
from components.block import Block


class Score(Component):

    def __init__(self, level: int, score: int):
        super().__init__()
        self.level = level
        self.score = score
        self.background = Block((0, 0, 0), 0, 0, 240, 100)

    def render(self, cx):
        gl.glPushMatrix()
        gl.glTranslatef(-1, 1, 0)  # Position the rectangle
        gl.glColor4f(0, 0, 0, 1)  # Set the rectangle color
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(0, 0)
        gl.glVertex2f(0, -.4)
        gl.glVertex2f(2, -.4)
        gl.glVertex2f(2, 0)
        gl.glEnd()
        gl.glPopMatrix()

        gl.glColor4f(1, 1, 1, 1)
        return [Text(f"Score: {self.score}\nLevel: {self.level}", 10, 450)]
