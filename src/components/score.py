import OpenGL.GL as gl
from core.component import Component
from components.text import Text


class Score(Component):
    def __init__(self, level: int = 1, score: int = 0):
        super().__init__()
        self.level = level
        self.score = score

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
        return Text(f"Score: {self.score}\nLevel: {self.level}", 10, 450)
