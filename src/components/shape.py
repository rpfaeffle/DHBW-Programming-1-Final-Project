from constants import Direction, RotationAngles
from components.block import Block
import math

class ShapeProps:
    def __init__(self, color: tuple[float, float, float, float], shape: list[tuple[int, int]], origin: tuple[int, int]):
        self.color = color
        self.shape = shape
        self.origin = origin

class Shape:
    def __init__(self, shape: ShapeProps, starting_pos: tuple[int, int], vacant_callback):
        self.shape = shape
        self.current_pos = starting_pos
        self.starting_pos = starting_pos
        self.blocks = []
        self.is_position_vacant = vacant_callback

        for position in shape.shape:
            self.blocks.append(Block(shape.color, position[0] + starting_pos[0], position[1] + starting_pos[1]))

    def can_rotate(self, cos_angle: float, sin_angle: float):
        """
        Checks if the current tetromino can rotate without colliding with other blocks.

        Returns:
         - bool: True if the tetromino can rotate, False otherwise.
        """
        for block in self.blocks:
            position = self.get_position_after_rotation(block, cos_angle, sin_angle)
            if not self.is_position_vacant((position[0], position[1] - 1)):
                return False
        return True

    def get_position_after_rotation(self, block, cos_angle: float, sin_angle: float):
        shape_origin = self.shape.origin
        origin = (shape_origin[0] + self.current_pos[0], shape_origin[1] + self.current_pos[1])
        starting_pos = (block.x, block.y)
        relative_pos = (starting_pos[0] - origin[0], starting_pos[1] - origin[1])
        new_x = relative_pos[0] * cos_angle - relative_pos[1] * sin_angle
        new_y = relative_pos[0] * sin_angle + relative_pos[1] * cos_angle
        # Just casting the values to an int causes the block to move to the left
        # (because the decimals get cut off instead of rounded)
        # so we need to add the origin to the new position to get the correct position
        # and round the final values.
        return (int(round(new_x + origin[0])), int(round(new_y + origin[1])))

    def rotate_shape(self, rotation_angle: RotationAngles):
        cos_angle = math.cos(rotation_angle.value)
        sin_angle = math.sin(rotation_angle.value)

        if not self.can_rotate(cos_angle, sin_angle):
            return

        for block in self.blocks:
            new_pos = self.get_position_after_rotation(block, cos_angle, sin_angle)
            block.x, block.y = new_pos

    def move_horizontally(self, direction: Direction):
        self.current_pos = (self.current_pos[0] + direction.value, self.current_pos[1])
        for block in self.blocks:
            block.x += direction.value

    def fall(self):
        self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)
        for block in self.blocks:
            block.move_down()
