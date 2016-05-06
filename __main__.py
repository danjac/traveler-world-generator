import argparse


from .world import generate_worlds
from .map import draw_map


def main():

    worlds = generate_worlds()
    draw_map(worlds, 30)

    for i in range(1, 9):
        for j in range(1, 11):
            world = worlds.get((i, j))
            if world:
                # print(world.coords_desc, world.uwp)
                world.pprint()
                print("----------------------------")


main()
