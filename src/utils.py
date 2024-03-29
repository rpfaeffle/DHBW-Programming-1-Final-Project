from itertools import chain

def color(r, g, b):
  return (r / 255, g / 255, b / 255, 1.0)

def flatten(list_of_lists):
  return list(chain.from_iterable(list_of_lists))
