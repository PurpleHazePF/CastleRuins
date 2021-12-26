from player import BLOCK_SIZE

text_map = [
    'W.......W',
    '..W.W.W..',
    '.........',
    'W.......W',
    '....W....',
    'W.......W'
]   # example map
map_cord = set()

for j, row in enumerate(text_map):
    for i, bloc in enumerate(row):
        if bloc == 'W':
            map_cord.add((i * BLOCK_SIZE, j * BLOCK_SIZE))
