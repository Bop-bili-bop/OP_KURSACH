from settings import *

class BaseMino:
    def __init__(self, shape, shape_map, group, create_new_mino, field_data):
        self.shape = shape
        self.block_positions = shape_map[shape]['shape']
        self.color = shape_map[shape]['color']
        self.create_new_mino = create_new_mino
        self.field_data = field_data
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    def next_move_horizontal_collide(self, amount):
        return any(
            block.horizontal_collide(int(block.pos.x + amount), self.field_data)
            for block in self.blocks
        )

    def next_move_vertical_collide(self, amount):
        return any(
            block.vertical_collide(int(block.pos.y + amount), self.field_data)
            for block in self.blocks
        )

    def move_horizontal(self, amount):
        if not (self.next_move_horizontal_collide(amount) or
                self.next_move_vertical_collide(0)):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_mino()

    def rotate(self):
        if self.shape in NO_ROTATE_SHAPES:
            return

        pivot = self.blocks[0].pos
        new_positions = [block.rotate(pivot) for block in self.blocks]

        for pos in new_positions:
            if pos.x < 0 or pos.x >= COLUMNS or pos.y < 0 or pos.y >= ROWS:
                return
            if self.field_data[int(pos.y)][int(pos.x)]:
                return

        for block, new_pos in zip(self.blocks, new_positions):
            block.pos = new_pos


class Tetromino(BaseMino):
    def __init__(self, shape, group, create_new_tetromino, field_data):
        super().__init__(shape, SHAPE, group, create_new_tetromino, field_data)


class Pentomino(BaseMino):
    def __init__(self, shape, group, create_new_pentomino, field_data):
        super().__init__(shape, PENTOMINOS, group, create_new_pentomino, field_data)

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        #pos
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = (self.pos * CELL_SIZE))

    def rotate(self, pivot_position):
        return pivot_position + (self.pos - pivot_position).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not (0 <= x < COLUMNS):
            return True

        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE