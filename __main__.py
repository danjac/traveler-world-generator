import argparse


from .world import generate_worlds
from .map import draw_map


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose',
                        help='Print long world descriptions',
                        action='store_true')

    parser.add_argument('-n', '--names',
                        help='List of world names')

    parser.add_argument('-o', '--output',
                        help='Output starmap to file')

    args = parser.parse_args()

    worlds = generate_worlds(args.names)
    draw_map(worlds, 30, args.output)

    for i in range(1, 9):
        for j in range(1, 11):
            world = worlds.get((i, j))
            if world is None:
                continue
            if args.verbose:
                world.pprint()
                print("----------------------------")
            else:
                if args.names:
                    print(world.name, world.coords_desc, world.uwp)
                else:
                    print(world.coords_desc, world.uwp)


main()
