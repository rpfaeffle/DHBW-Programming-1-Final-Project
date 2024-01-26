import OpenGL.GL as gl
from core.component import Component
from core.context import WindowContext
from core.openGLUtils import OpenGLUtils

class Line(Component):
    def __init__(self, start_pos: tuple[int, int], end_pos: tuple[int, int], color: tuple[float, float, float, float] = (.75, .75, .75, 1.0)):
        super().__init__()
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.normalized_start_pos = None
        self.normalized_end_pos = None

    def render(self, cx: WindowContext):
        if self.normalized_start_pos is None or self.normalized_end_pos is None:
            self.normalized_start_pos = OpenGLUtils.convert_to_normalized_coordinates(self.start_pos[0], self.start_pos[1], cx.width, cx.height)
            self.normalized_end_pos = OpenGLUtils.convert_to_normalized_coordinates(self.end_pos[0], self.end_pos[1], cx.width, cx.height)

        x1, y1 = self.normalized_start_pos
        x2, y2 = self.normalized_end_pos

        gl.glPushMatrix()
        gl.glColor4f(*self.color)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex2f(x1, y1)
        gl.glVertex2f(x2, y2)
        gl.glEnd()
        gl.glPopMatrix()
