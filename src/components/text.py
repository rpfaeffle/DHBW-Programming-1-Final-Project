import functools
from core.component import Component
from core.openGLUtils import OpenGLUtils


class Text(Component):
    def __init__(self, text: str, x: int, y: int):
        super().__init__()
        self.text = text
        self.x, self.y = x, y

    def render(self, cx):
        lines = self.text.split('\n')
        x, y = OpenGLUtils.convert_to_normalized_coordinates(self.x, self.y, cx.width, cx.height)

        for i in range(len(lines)):
          line = lines[i]
          cx.font.draw(line, x, y - i * cx.font.dimension.height)
