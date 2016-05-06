import argparse
import csv
import sys


from .world import generate_worlds
from .map import draw_map

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose',
                    help='Print long world descriptions',
                    action='store_true')

parser.add_argument('-n', '--names',
                    help='List of world names')

parser.add_argument('-o', '--output',
                    help='Output starmap to file')


def yesno(value):
    return "Yes" if value else "No"


def main():

    args = parser.parse_args()

    worlds = generate_worlds(args.names)
    draw_map(worlds, 30, args.output)

    # if args.csv:
    w = csv.writer(sys.stdout)
    if args.verbose:
        headers = [
            "Coords",
            "UWP",
            "Starport",
            "Size",
            "Atmosphere",
            "Temperature",
            "Hydrographics",
            "Population",
            "Government",
            "Law level",
            "Tech level",
            "Notes",
            "Gas giant?",
            "Scout base?",
            "Naval base?",
            "Research base?",
            "Pirate base?",
            "Traveler's Aid Society?",
            "Imperial consulate?",
        ]
    else:
        headers = [
            "Coords",
            "UWP",
            "Bases",
            "Notes",
        ]

    if args.names:
        headers.insert(0, "Name")

    w.writerow(headers)

    for i in range(1, 9):
        for j in range(1, 11):
            world = worlds.get((i, j))
            if world is None:
                continue
            if args.verbose:
                values = [
                    world.coords_desc,
                    world.uwp,
                    world.starport,
                    world.size_desc,
                    world.atmosphere_desc,
                    world.temperature_desc,
                    world.hydrographics_desc,
                    world.population_desc,
                    world.government_desc,
                    world.law_level_desc,
                    world.tech_level,
                    world.long_trade_classifications,
                    yesno(world.is_gas_giant),
                    yesno(world.is_scout_base),
                    yesno(world.is_naval_base),
                    yesno(world.is_research_base),
                    yesno(world.is_pirate_base),
                    yesno(world.is_tas),
                    yesno(world.is_consulate),
                ]

            else:
                values = [
                    world.coords_desc,
                    world.uwp,
                    world.base_codes,
                    world.short_trade_classifications,
                ]

            if args.names:
                values.insert(0, world.name)

            w.writerow(values)

main()
