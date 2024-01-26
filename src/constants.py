from utils import color

# Constants
GAME_SPEED = 5 # Block moves down every 60 frames
BLOCK_SIZE = 20

COLORS = {
  'O': color(255, 239, 43),
  'L': color(247, 167, 0),
  'J': color(0, 100, 200),
  'I': color(0, 201, 223),
  'T': color(155, 0, 190),
  'Z': color(220, 0, 0),
  'S': color(0, 230, 50),
}

POSITIONS = {
  'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
  'L': [(0, 0), (0, 1), (0, 2), (1, 2)],
  'J': [(1, 0), (1, 1), (1, 2), (0, 2)],
  'I': [(0, 0), (0, 1), (0, 2), (0, 3)],
  'T': [(1, 0), (0, 1), (1, 1), (1, 2)],
  'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
  'S': [(0, 1), (1, 1), (1, 0), (2, 0)],
}

KEYS = list(set(COLORS.keys()))

ROTATION_ORIGINS = {
  'O': (0.5, 0.5),
  'L': (0, 1),
  'J': (1, 1),
  'I': (0.5, 1.5),
  'T': (1, 1),
  'Z': (1, 1),
  'S': (1, 1),
}
