from core.component import Component
from core.openGLUtils import OpenGLUtils


class Text(Component):
    def __init__(self, text: str, x: int, y: int):
        super().__init__()
        self.text = text
        self.x, self.y = x, y

    def render(self, cx):
        x, y = OpenGLUtils.convert_to_normalized_coordinates(self.x, self.y, cx.width, cx.height)
        cx.font.draw(self.text, x, y)
        return self
