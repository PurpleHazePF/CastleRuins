from player import BLOCK_SIZE

text_map = [
    'W.......W',
    '..W.W.W..',
    '.........',
    'W.......W',
    '....W....',
    'W.......W',
    'W.......W'
]   # example map
map_cord = set()
width, height = 900, 650
BLOCK_SIZE_X = (width / len(text_map[0])) // 1 + 1
BLOCK_SIZE_Y = (height / len(text_map)) // 1 + 1
for j, row in enumerate(text_map):
    for i, bloc in enumerate(row):
        if bloc == 'W':
            map_cord.add((i * BLOCK_SIZE_X, j * BLOCK_SIZE_Y))
