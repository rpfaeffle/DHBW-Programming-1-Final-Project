from components.block import Block
import math

class ShapeProps:
    def __init__(self, color: tuple[float, float, float], shape: list[tuple[int, int]], origin: tuple[int, int]):
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

    def can_rotate(self):
        """
        Checks if the current tetromino can rotate without colliding with other blocks.

        Returns:
         - bool: True if the tetromino can rotate, False otherwise.
        """
        for block in self.blocks:
            position = self.get_position_after_rotation(block, True)
            if not self.is_position_vacant((position[0], position[1] - 1)):
                return False
        return True

    def get_position_after_rotation(self, block, is_clockwise: bool):
        shape_origin = self.shape.origin
        origin = (shape_origin[0] + self.current_pos[0], shape_origin[1] + self.current_pos[1])
        rotation_angle = math.radians(90) if is_clockwise else math.radians(-90)
        starting_pos = (block.x, block.y)
        relative_pos = (starting_pos[0] - origin[0], starting_pos[1] - origin[1])
        new_x = relative_pos[0] * math.cos(rotation_angle) - relative_pos[1] * math.sin(rotation_angle)
        new_y = relative_pos[0] * math.sin(rotation_angle) + relative_pos[1] * math.cos(rotation_angle)
        # Just casting the values to an int causes the block to move to the left
        # (because of the fact that the decimals get cut off instead of rounded)
        # so we need to add the origin to the new position to get the correct position
        # and round the final values.
        return (int(round(new_x + origin[0])), int(round(new_y + origin[1])))

    def rotate_shape(self, is_clockwise: bool):
        if not self.can_rotate():
            return

        for block in self.blocks:
            new_pos = self.get_position_after_rotation(block, is_clockwise)
            block.x = new_pos[0]
            block.y = new_pos[1]

    def move_horizontally(self, direction):
        self.current_pos = (self.current_pos[0] + (1 if direction == 'right' else -1), self.current_pos[1])
        if direction == 'left':
            for block in self.blocks:
                block.x -= 1
        elif direction == 'right':
            for block in self.blocks:
                block.x += 1

    def fall(self):
        self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)
        for block in self.blocks:
            block.move_down()

    def get_blocks(self):
        return self.blocks
