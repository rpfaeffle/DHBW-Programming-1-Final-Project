class FallingBlock(object):
  def __init__(self, blocks, type):
    self.blocks = blocks
    self.type = type

  def fall(self):
    for block in self.blocks:
      block.move_down()

  def can_fall(self):
    return True

  def get_blocks(self):
    return self.blocks
