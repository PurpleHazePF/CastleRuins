import math
from map import width, BLOCK_SIZE_X

x, y = 500, 300
vector = 0
speed = 10
fps = 30
nach_y = 300
dlina_vzglyada = (40, 40)

OBZOR = math.pi / 3
NUM_RAYS = 300
DELTA_ANGLE = OBZOR / NUM_RAYS
PROJ_COEFF = 2 * NUM_RAYS / (2 * math.tan(OBZOR / 2)) * BLOCK_SIZE_X
SCALE = math.ceil(width / NUM_RAYS)

# hero width, height
SIZE = 10
