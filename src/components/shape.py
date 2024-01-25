from components.block import Block
import math

class Shape:
    def __init__(self, shape, starting_pos: (int, int)):
        self.shape = shape
        self.current_pos = starting_pos
        self.starting_pos = starting_pos
        self.blocks = []

        for position in shape['shape']:
            self.blocks.append(Block(shape['color'], position[0] + starting_pos[0], position[1] + starting_pos[1]))

    def get_position_after_rotation(self, block, is_clockwise: bool):
        shape_origin = self.shape['origin']
        origin = (shape_origin[0] + self.current_pos[0], shape_origin[1] + self.current_pos[1])
        rotation_angle = math.radians(90) if is_clockwise else math.radians(-90)
        starting_pos = (block.x, block.y)
        relative_pos = (starting_pos[0] - origin[0], starting_pos[1] - origin[1])
        new_x = relative_pos[0] * math.cos(rotation_angle) - relative_pos[1] * math.sin(rotation_angle)
        new_y = relative_pos[0] * math.sin(rotation_angle) + relative_pos[1] * math.cos(rotation_angle)
        return (int(new_x + origin[0]), int(new_y + origin[1]))

    def rotate_shape(self, is_clockwise: bool):
        for block in self.blocks:
            new_pos = self.get_position_after_rotation(block, is_clockwise)
            print(new_pos)
            block.x = new_pos[0]
            block.y = new_pos[1]

    def fall(self):
        self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)
        for block in self.blocks:
            block.move_down()

    def get_blocks(self):
        return self.blocks
