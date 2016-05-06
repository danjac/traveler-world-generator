import math


from PIL import Image, ImageDraw


def draw_map(worlds, edge_length, filename=None):
    image_size = edge_length * 20
    image = Image.new('RGB', (image_size, image_size), 'white')

    draw = ImageDraw.Draw(image)
    hex_generator = HexGenerator(edge_length)

    for row in range(20):
        for col in range(1, 5):
            hex = list(hex_generator(row, col))
            draw.polygon(hex, outline='black', fill='white')

    hex_width = round(math.sqrt(3) * edge_length)

    for row in range(1, 11):
        # this needs to be fixed a bit to the right
        # doesn't work with larger map sizes
        x = ((edge_length * 1.5) * 2) + 1
        for col in range(1, 9):
            # height one cell higher for odd columns
            y = hex_width * row
            if col % 2 == 1:
                y -= (hex_width / 2)
            text = "%02.d%02.d" % (col, row)
            # text/world positions should be proportional to hex size
            draw.text((x, y-20), text, 8)
            world = worlds.get((col, row))
            if world is not None:
                draw.text((x+10, y-10), world.starport, 12)
                r = 5
                draw.ellipse((x+12-r, y+10-r, x+12+r, y+10+r), fill='black')
            x += (edge_length * 1.5)
    if filename:
        image.save(filename)
    else:
        image.show()


class HexGenerator(object):

    def __init__(self, edge_length):
        self.edge_length = edge_length
        self.col_width = self.edge_length * 3
        self.row_height = math.sin(math.pi / 3) * self.edge_length

    def __call__(self, row, col):
        x = (col + 0.5 * (row % 2)) * self.col_width
        y = row * self.row_height
        for angle in range(0, 360, 60):
            r_angle = math.radians(angle)
            x += math.cos(r_angle) * self.edge_length
            y += math.sin(r_angle) * self.edge_length
            yield x, y
