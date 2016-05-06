#! /usr/bin/python

import random
import math

from PIL import Image, ImageDraw

HEADERS = (
    ("Coordinates", "coords_desc", False),
    ("Starport", "starport", False),
    ("Size", "size_desc", False),
    ("Atmosphere", "atmosphere_desc", False),
    ("Temperature", "temperature_desc", False),
    ("Hydrographics", "hydrographics_desc", False),
    ("Population", "population_desc", False),
    ("Government", "government_desc", False),
    ("Law level", "law_level_desc", False),
    ("Tech level", "tech_level", False),
    ("Trade classifications", "trade_classifications", False),
    ("Gas giant", "is_gas_giant", True),
    ("Scout base", "is_scout_base", True),
    ("Naval base", "is_naval_base", True),
    ("Research base", "is_research_base", True),
    ("Pirate base", "is_pirate_base", True),
    ("Traveler's Aid Society", "is_tas", True),
    ("Imperial consulate", "is_consulate", True),
    ("UWP", "uwp", False),
)

# longest header?

MAX_HEADER_SIZE = max(len(row[0]) for row in HEADERS)


TEMP_MODIFIERS = (
    ((2, 3), 2),
    ((4, 5, 14), -1),
    ((8, 9), 1),
    ((10, 13, 15), 2),
    ((11, 12), 6),
)

STARPORTS = ("X", "E", "E", "D", "D", "C", "C", "B", "B", "A", "A")

ATMOSPHERES = (
    "None", "Trace", "Very thin, Tainted", "Very thin", "Thin, Tainted",
    "Thin", "Standard", "Standard, Tainted", "Dense", "Dense, Tainted",
    "Exotic", "Corrosive", "Insidious", "Dense, High", "Thin, Low", "Unusual",
)

GOVERNMENTS = (
    "None", "Company/Corporation", "Participating Democracy",
    "Self-Perpetuating Oligarchy", "Representative Democracy",
    "Feudal Technocracy", "Captive Government", "Balkanization",
    "Civil Service Bureaucracy", "Impersonal Bureaucracy",
    "Charismatic Dictatorship", "Non-Charismatic Leader",
    "Charismatic Oligarchy", "Religious Dictatorship",
)

LAW_LEVELS = (
    "No prohibitions",
    "Body pistols, explosives, and poison gas prohibited",
    "Portable energy weapons prohibited",
    "Machineguns, automatic rifles prohibited",
    "Light assault weapons prohibited",
    "Personal concealable weapons prohibited",
    "All firearms except shotguns prohibited",
    "Shotguns prohibited",
    "Long bladed weapons controlled; open possession prohibited",
    "Possession of weapons outside the home prohibited",
    "Weapon possession prohibited",
    "Rigid control of civilian movement",
)

BERTHING_COST_MODIFIERS = {
    "A": 1000,
    "B": 500,
    "C": 100,
    "D": 10,
}

TAS_MODIFIERS = {
    "A": 4,
    "B": 2,
    "C": -2,
}

CONSULATE_MODIFIERS = {
    "A": 2,
    "C": -2,
}


STARPORT_TECH_MODIFIERS = {
    "A": 6,
    "B": 4,
    "C": 2,
    "X": -4,
}

SIZE_TECH_MODIFIERS = {
    0: 2,
    1: 2,
    2: 1,
    3: 1,
    4: 1,
}

HYDRO_TECH_MODIFIERS = {
    0: 1,
    9: 1,
    10: 2,
}

POP_TECH_MODIFIERS = {
    9: 1,
    10: 2,
    11: 3,
    12: 4,
}

GOV_TECH_MODIFIERS = {
    0: 1,
    5: 2,
    13: -4,
    15: -2,
}


def die_roll(dice, modifier=0, min=None, max=None):
    result = sum(random.randint(1, 6) for die in range(dice)) + modifier
    if min is not None and result < min:
        result = min
    if max is not None and result > max:
        result = max
    return result


def yesno(value):
    return "Yes" if value else "No"


def draw_map(worlds):
    image = Image.new('RGB', (600, 600), 'white')
    draw = ImageDraw.Draw(image)
    hex_generator = HexGenerator(30)
    for row in range(20):
        for col in range(1, 5):
            hex = list(hex_generator(row, col))
            draw.polygon(hex, outline='black', fill='white')

    for row in range(1, 11):
        x = 93  # edge / 2 + hex total width (sqrt of 3 * edge)
        for col in range(1, 9):
            # height one cell higher for odd columns
            y = 52 * row
            if col % 2 == 1:
                y -= 26
            text = "%02.d%02.d" % (col, row)
            draw.text((x, y-20), text, 8)
            world = worlds.get((col, row))
            if world is not None:
                draw.text((x+10, y-10), world.starport, 12)
                r = 5
                draw.ellipse((x+12-r, y+10-r, x+12+r, y+10+r), fill='black')
            x += 45  # 1 + 1/2 edges
    # image.save('hexmap.png')
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


class World(object):

    def __init__(self, coordinates):

        self.coordinates = coordinates

        self.is_gas_giant = die_roll(2) >= 10

        self.size = die_roll(2, -2)

        # atmosphere

        self.atmosphere = die_roll(2, (-7 + self.size), 0, 15)

        # temperature

        temp_modifier = 0

        for (atmospheres, modifier) in TEMP_MODIFIERS:
            if self.atmosphere in atmospheres:
                temp_modifier += modifier

        self.temperature = die_roll(2, temp_modifier, 0, 15)

        # hydrographics

        hydro_modifier = self.size - 7
        if self.atmosphere in (0, 1, 10, 11, 12):
            hydro_modifier -= 4
        if self.atmosphere != 13:
            if self.temperature in (10, 11):
                hydro_modifier -= 2
            elif self.temperature >= 12:
                hydro_modifier -= 6

        self.hydrographics = die_roll(2, hydro_modifier, 0, 10)

        # population

        self.population = die_roll(2)
        low_pop_bound = math.pow(10, self.population)
        high_pop_bound = math.pow(10, self.population + 1)
        self.exact_population = int(
            random.randint(low_pop_bound, high_pop_bound)
        )

        # starport

        starport_modifier = self.population - 7
        starport_roll = die_roll(2, starport_modifier, 2, 12)
        self.starport = STARPORTS[starport_roll - 2]

        berthing_cost_modifier = \
            BERTHING_COST_MODIFIERS.setdefault(self.starport, 0)

        self.berthing_cost = die_roll(1) * berthing_cost_modifier

        # bases & facilities

        self.is_naval_base = False

        if self.starport in ("A", "B"):
            self.is_naval_base = die_roll(2) > 7

        self.is_scout_base = False

        if self.starport not in ("E", "X"):
            scout_base_modifier = 1 if self.starport == "D" else 0
            self.is_scout_base = die_roll(2, scout_base_modifier) > 7

        self.is_research_base = False

        if self.starport in ("A", "B", "C"):
            research_base_modifier = 0 if self.starport == "A" else -2
            self.is_research_base = die_roll(2, research_base_modifier) > 7

        self.is_tas = False

        if self.starport in ("A", "B", "C"):
            tas_modifier = TAS_MODIFIERS.setdefault(self.starport, 0)
            self.is_tas = die_roll(2, tas_modifier) > 7

        self.is_consulate = False

        if self.starport in ("A", "B", "C"):
            consulate_modifier = \
                CONSULATE_MODIFIERS.setdefault(self.starport, 0)

            self.is_consulate = die_roll(2, consulate_modifier) > 7

        self.is_pirate_base = False

        if self.starport not in ("A", "X"):
            pirate_base_modifier = 0
            if self.starport in ("B", "D", "E"):
                pirate_base_modifier = -4
            elif self.starport == "C":
                pirate_base_modifier = -2
            self.is_pirate_base = die_roll(2, pirate_base_modifier) > 7

        # government

        gov_modifier = self.population - 7
        self.government = die_roll(2, gov_modifier, 0, 13)

        # law level

        law_modifier = self.government - 7
        self.law_level = die_roll(2, law_modifier, 0, 10)

        # tech level

        tech_modifier = 0

        tech_modifier += STARPORT_TECH_MODIFIERS.setdefault(self.starport, 0)
        tech_modifier += SIZE_TECH_MODIFIERS.setdefault(self.size, 0)
        tech_modifier += HYDRO_TECH_MODIFIERS.setdefault(self.hydrographics, 0)
        tech_modifier += POP_TECH_MODIFIERS.setdefault(self.population, 0)
        tech_modifier += GOV_TECH_MODIFIERS.setdefault(self.government, 0)

        if self.atmosphere < 4 or self.atmosphere > 9:
            tech_modifier += 1

        if self.population > 0 or self.population < 6:
            tech_modifier += 1

        self.tech_level = die_roll(1, tech_modifier, 0, 16)

    def pprint(self):
        for header, attr, is_bool in HEADERS:
            spacing = " " * (MAX_HEADER_SIZE - len(header))
            value = getattr(self, attr)
            if is_bool:
                value = yesno(value)
                header += "?"
            else:
                header += ":"
            print(header, spacing, value)

    @property
    def uwp(self):
        rv = [self.starport]
        rv += ["%.X" % value for value in (
            self.size,
            self.atmosphere,
            self.hydrographics,
            self.population,
            self.government,
            self.law_level,
        )]

        rv.append("-%.X" % self.tech_level)

        bases = []

        if self.is_naval_base:
            bases.append("N")
        if self.is_scout_base:
            bases.append("S")
        if self.is_research_base:
            bases.append("R")
        if self.is_tas:
            bases.append("T")
        if self.is_consulate:
            bases.append("I")
        if self.is_pirate_base:
            bases.append("P")

        if bases:
            rv.append(" ")
            rv.append(" ".join(bases))

        trade_cls = []

        if self.is_agricultural:
            trade_cls.append("Ag")
        if self.is_non_agricultural:
            trade_cls.append("Na")
        if self.is_asteroid_belt:
            trade_cls.append("As")
        if self.is_barren:
            trade_cls.append("Ba")
        if self.is_desert:
            trade_cls.append("De")
        if self.is_fluid:
            trade_cls.append("Fl")
        if self.is_garden_world:
            trade_cls.append("Ga")
        if self.is_high_population:
            trade_cls.append("Hi")
        if self.is_ice_capped:
            trade_cls.append("IC")
        if self.is_industrial:
            trade_cls.append("In")
        if self.is_low_population:
            trade_cls.append("Lo")
        if self.is_non_industrial:
            trade_cls.append("Ni")
        if self.is_poor:
            trade_cls.append("Po")
        if self.is_rich:
            trade_cls.append("Ri")
        if self.is_water_world:
            trade_cls.append("Wa")
        if self.is_vaccuum_world:
            trade_cls.append("Va")

        if trade_cls:
            rv.append(" ")
            rv.append(" ".join(trade_cls))

        return "".join(rv)

    @property
    def is_agricultural(self):
        return all((
            self.atmosphere > 3,
            self.atmosphere < 10,
            self.hydrographics > 3,
            self.hydrographics < 9,
            self.population > 4,
            self.population < 8,
        ))

    @property
    def is_non_agricultural(self):
        return all((
            self.atmosphere < 4,
            self.hydrographics < 4,
            self.population > 5,
        ))

    @property
    def is_asteroid_belt(self):
        return self.atmosphere == self.size == self.hydrographics == 0

    @property
    def is_barren(self):
        return self.population == 0

    @property
    def is_desert(self):
        return self.atmosphere > 1 and self.hydrographics == 0

    @property
    def is_fluid(self):
        return self.atmosphere > 9 and self.hydrographics > 0

    @property
    def is_garden_world(self):
        return all((
            self.size > 4,
            self.atmosphere > 3,
            self.atmosphere < 10,
            self.hydrographics > 3,
            self.hydrographics < 9,
        ))

    @property
    def is_high_population(self):
        return self.population > 8

    @property
    def is_low_population(self):
        return self.population < 4

    @property
    def is_ice_capped(self):
        return self.atmosphere < 2 and self.hydrographics > 0

    @property
    def is_industrial(self):
        return all((
            (self.atmosphere < 3 or self.atmosphere in (4, 7, 9)),
            self.population > 8,
        ))

    @property
    def is_non_industrial(self):
        return self.population < 7

    @property
    def is_rich(self):
        return all((
            self.atmosphere in (6, 8),
            self.population > 5,
            self.population < 9,
            self.government > 3,
            self.government < 10,
        ))

    @property
    def is_poor(self):
        return all((
            self.atmosphere > 1,
            self.atmosphere < 6,
            self.hydrographics < 4,
        ))

    @property
    def is_water_world(self):
        return self.hydrographics > 9

    @property
    def is_vaccuum_world(self):
        return self.atmosphere == 0 and self.size > 0

    @property
    def coords_desc(self):
        return "%02.d%02.d" % self.coordinates

    @property
    def size_desc(self):
        if self.size == 0:
            return "N/A"
        return "{:,} miles".format(self.size * 1000)

    @property
    def atmosphere_desc(self):
        return ATMOSPHERES[self.atmosphere]

    @property
    def temperature_desc(self):
        if self.temperature < 3:
            return "Frozen"
        if self.temperature in (3, 4):
            return "Cold"
        if self.temperature in (10, 11):
            return "Hot"
        if self.temperature > 11:
            return "Roasting"
        return "Temperate"

    @property
    def hydrographics_desc(self):
        return "{}%".format(self.hydrographics * 10)

    @property
    def population_desc(self):
        return "{:,}".format(self.exact_population)

    @property
    def government_desc(self):
        return GOVERNMENTS[self.government]

    @property
    def law_level_desc(self):
        return LAW_LEVELS[self.law_level]

    @property
    def trade_classifications(self):
        rv = []
        if self.is_agricultural:
            rv.append("Agricultural")
        if self.is_non_agricultural:
            rv.append("Non-agricultural")
        if self.is_asteroid_belt:
            rv.append("Asteroid belt")
        if self.is_barren:
            rv.append("Barren")
        if self.is_desert:
            rv.append("Desert")
        if self.is_fluid:
            rv.append("Fluid")
        if self.is_garden_world:
            rv.append("Garden world")
        if self.is_high_population:
            rv.append("High population")
        if self.is_ice_capped:
            rv.append("Ice-capped")
        if self.is_industrial:
            rv.append("Industrial")
        if self.is_low_population:
            rv.append("Low population")
        if self.is_non_industrial:
            rv.append("Non-industrial")
        if self.is_poor:
            rv.append("Poor")
        if self.is_rich:
            rv.append("Rich")
        if self.is_water_world:
            rv.append("Water world")
        if self.is_vaccuum_world:
            rv.append("Vaccuum world")

        if not rv:
            return "None"
        return ", ".join(rv)


def main():

    worlds = {}
    for i in range(1, 11):
        for j in range(1, 9):
            if die_roll(2) > 7:
                world = World((j, i))
                # hex.world.pprint()
                # print("----------------------------")
                worlds[(j, i)] = world
    draw_map(worlds)
    for i in range(1, 9):
        for j in range(1, 11):
            world = worlds.get((i, j))
            if world:
                print(world.coords_desc, world.uwp)


main()
