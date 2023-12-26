"""--- Day 5: If You Give A Seed A Fertilizer ---
    You take the boat and find the gardener right where you were told he would be:
    managing a giant "garden" that looks more to you like a farm.

    "A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

    "Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water.
    Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no."
    His face sinks into a look of horrified realization.

    "I've been so busy making sure everyone here has food that I completely forgot to
    check why we stopped getting more sand!
    There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat.
    Could you please go check it out?"

    You barely have time to agree to this request when he brings up another.
    "While you wait for the ferry, maybe you can help us with our food production problem.
    The latest Island Island Almanac just arrived and we're having trouble making sense of it."

"""
import re
import time
from ..day import DayBase

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

# example2 = """seeds: 0 4 0 14 0 22 8 6 18 4 8 14
example2 = """seeds: 0 4 8 6 18 4

seed-to-soil map:
105 5 12
52 50 48

soil-to-fertilizer map:
1000 0 1000"""


class Almanac:
    """The almanac (your puzzle input) lists all of the seeds that need to be planted.
    It also lists what type of soil to use with each kind of seed, what type of fertilizer
    to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on.
    Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused
    by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.



    The rest of the almanac contains a list of maps which describe how to convert numbers from a source category
    into numbers in a destination category.
    That is, the section that starts with seed-to-soil map:
    describes how to convert a seed number (the source) to a soil number (the destination).
    This lets the gardener and his team know which soil to use with which seeds,
    which water to use with which fertilizer, and so on."""

    def __init__(self, data, part2=False):
        lines = re.split(r"\n\n+", data)
        # Take the example,the almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.
        self.seeds = [int(e) for e in lines[0][6:].strip().split(" ")]
        if part2:
            self.seeds_group = []
            for sect in range(int(len(self.seeds) / 2)):
                # seeds_group is a list of [start, range]
                self.seeds_group.append([self.seeds[2 * sect], self.seeds[2 * sect] - 1 + self.seeds[2 * sect + 1]])
            sorted(self.seeds_group)
            # print("Seed groups made")
        self.next = []
        self.inter = []
        self.base = {}
        self.dest = {}

        for map in lines[1:]:
            map_split = map.split("\n")
            map_info = re.match(r"(?P<from>\w+)-to-(?P<to>\w+) map:", map_split[0])
            self.base[map_info['from']] = map_info['to']
            self.dest[map_info['to']] = [
                # road = [start_dest, start_source, range] => [start_source, start_dest, range]
                self.road(line.split(" ")) for line in map_split[1:]
            ]

    @staticmethod
    def road(e):
        start_source = int(e[1])
        start_dest = int(e[0])
        range_size = int(e[2])
        road = [
            start_source, start_dest, range_size,
            range_size + start_source - 1,  # 3: add end_source
            start_dest - start_source  # 4: add affine transformation
        ]
        return road

    @staticmethod
    def in_range(elem, road):
        # start_source <= elem <= end_source
        return road[0] <= elem <= road[3]

    def range_in_range(self, group, road):
        # print(f"  range_in_range : {group} against {road}")
        # print(f"  {self.next}")
        start = group[0]
        end = group[1]
        f_start = road[0]
        f_end = road[3]
        # print(f"  [{start};{end}]::[{f_start};{f_end}]")
        if (end < f_start) or (start > f_end):
            # Intersection is void
            # print("  => Intersection is void")
            return False  # [start, end]
        if end < f_end:
            if start < f_start:
                # case group inter road min => 2 groups
                # print("  => case group inter road min")
                # print(f"    --> {[[start, f_start - 1], [road[1], end + road[4]]]}")
                self.next.append([start, f_start - 1])
                self.next.append([road[1], end + road[4]])
            else:
                # case group in road => 1 group
                # print("  => case group in road")
                # print(f"    --> {[[start + road[4], end + road[4]]]}")
                self.next.append([start + road[4], end + road[4]])
        else:
            if start < f_start:
                # case road in group => 3 groups
                # print("  => case road in group")
                # print(f"    --> {[[start, f_start - 1], [road[1], f_end + road[4]], [f_end + 1, end]]}")
                self.next.append([start, f_start - 1])
                self.next.append([road[1], f_end + road[4]])
                self.next.append([f_end + 1, end])
            else:
                # case group inter road max => 2 groups
                # print("  => case group inter road max")
                # print(f"    --> {[[start + road[4], f_end + road[4]], [f_end + 1, end]]}")
                self.next.append([start + road[4], f_end + road[4]])
                self.next.append([f_end + 1, end])
        # print(f"  :{self.next}")
        return True  # (f_start <= start <= f_end) or (f_start <= end <= f_end) or (start <= f_start <= end)

    def transform_elem(self, elem, road):
        self.next.append(road[4] + elem)


class Day(DayBase):
    def do(self):
        self.test(4361, 467835, example)
        self.run(520135, 72514855)

    @staticmethod
    def part1(data=example):
        pass

    @staticmethod
    def part2(data=example):
        pass


def c2023d5p1(data=example):
    """Part 1

    :param data:
        Rather than list every source number and its corresponding destination number one by one,
        the maps describe entire ranges of numbers that can be converted.
        Each line within a map contains three numbers:
        the destination range start, the source range start, and the range length.

        Consider again the example seed-to-soil map:

        50 98 2
        52 50 48
        The first line has a destination range start of 50, a source range start of 98, and a range length of 2.
        This line means that the source range starts at 98 and contains two values: 98 and 99.
        The destination range is the same length, but it starts at 50, so its two values are 50 and 51.
        With this information, you know that seed number 98 corresponds to soil number 50 and
        that seed number 99 corresponds to soil number 51.

        The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97.
        This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99.
        So, seed number 53 corresponds to soil number 55.

        Any source numbers that aren't mapped correspond to the same destination number.
        So, seed number 10 corresponds to soil number 10.

        So, the entire list of seed numbers and their corresponding soil numbers looks like this:

        seed  soil
        0     0
        1     1
        ...   ...
        48    48
        49    49
        50    52
        51    53
        ...   ...
        96    98
        97    99
        98    50
        99    51
        With this map, you can look up the soil number required for each initial seed number:

        Seed number 79 corresponds to soil number 81.
        Seed number 14 corresponds to soil number 14.
        Seed number 55 corresponds to soil number 57.
        Seed number 13 corresponds to soil number 13.
    :return:
        The gardener and his team want to get started as soon as possible,
        so they'd like to know the closest location that needs a seed.
        Using these maps, find the lowest location number that corresponds to any of the initial seeds.
        To do this, you'll need to convert each seed number through other categories until
        you can find its corresponding location number. In this example, the corresponding types are:

        Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
        Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
        Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
        Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
        So, the lowest location number in this example is 35.

        What is the lowest location number that corresponds to any of the initial seed numbers?
    """
    almanac = Almanac(data)
    cursor = "seed"
    almanac.next = almanac.seeds
    while cursor in almanac.base:
        cursor = almanac.base[cursor]
        mapper = almanac.dest[cursor]
        current_list = almanac.next
        almanac.next = []
        for elem_id in range(len(current_list)):
            elem = current_list[elem_id]
            found = False
            for road in mapper:
                if almanac.in_range(elem, road):
                    almanac.transform_elem(elem, road)
                    found = True
                    break
            if not found:
                almanac.next.append(elem)
    return min(almanac.next)


def c2023d5p2(data=example):
    """--- Part Two ---
    Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac,
    it looks like the seeds: line actually describes ranges of seed numbers.

    The values on the initial seeds: line come in pairs. Within each pair,
    the first value is the start of the range and the second value is the length of the range.
    So, in the first line of the example above:

    seeds: 79 14 55 13
    This line describes two ranges of seed numbers to be planted in the garden.
    The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92.
    The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

    Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

    In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84,
    fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46.
    So, the lowest location number is 46.

    Consider all of the initial seed numbers listed in the ranges on the first line of the almanac.
    What is the lowest location number that corresponds to any of the initial seed numbers?
    """
    start_time = time.time()
    almanac = Almanac(data, True)
    cursor = "seed"
    almanac.next = almanac.seeds_group
    # print(cursor)
    # print(almanac.next)
    while cursor in almanac.base:
        cursor = almanac.base[cursor]
        mapper = almanac.dest[cursor]
        current_list = almanac.next
        almanac.next = []
        for elem_id in range(len(current_list)):
            elem = current_list[elem_id]
            found = False
            for road in mapper:
                found = almanac.range_in_range(elem, road)
                if found:
                    break
            if not found:
                # print("  => Intersection is void")
                # print(f"    --> {elem}")
                almanac.next.append(elem)
        # Sorting list to merge duplicate
        sorted_list = sorted(almanac.next)
        almanac.next = []
        curr = sorted_list[0]
        for e in sorted_list:
            if curr[1] > e[0]:
                curr[1] = e[1]
            else:
                almanac.next.append(curr)
                curr = e
        if curr != almanac.next[-1]:
            almanac.next.append(curr)
        # print(cursor)
        # print(almanac.next)

        # exit()
    print(sorted(almanac.next))
    end = time.time()
    total_time = end - start_time
    seconds = int(total_time)
    print("#" * 80)
    print(f"TIME ELAPSED FOR THE TESTS : {seconds} sec")
    return sorted(almanac.next)[0][0]


if __name__ == "__main__":
    print("########################")
    print("####    TEST ALGO   ####")
    ok = "ok" if c2023d5p1() == 35 else "ko"
    print(f"##  c2023d5p1 => {ok}    #")
    ok = "ok" if c2023d5p2() == 46 else "ko"
    print(f"##  c2023d5p2 => {ok}    #")
    print("########################")
    print("#   WITH PUZZLE INPUT  #")
    with open('2023/d5.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2023d5p1 => {c2023d5p1(input_data)} #")
        print(f"# c2023d5p2 => {c2023d5p2(input_data)} #")
        # [
        #  [88465636, 90439079], [104012185, 108824346], [131615290, 140661495], [177581361, 183590122],
        #  [200806553, 204277704], [427651238, 433354040], [471665171, 500574870], [618663056, 624365145],
        #  [663669634, 690844426], [1003659815, 1010543475], [1013518473, 1019376783], [1170039042, 1181170115],
        #  [1240453204, 1246534460], [1448114805, 1459261177], [1463667543, 1477788232], [1670156628, 1681546949],
        #  [1773044595, 1825091987], [1869523774, 1892052515], [2064729022, 2072659782], [2241476012, 2263995309],
        #  [2450179186, 2514776169], [2535771579, 2605842840], [2769405749, 2780638748], [2830521679, 2840339603],
        #  [2868834448, 2875774425], [2915672936, 2929631959], [2982163110, 2983873804], [3054939753, 3074089993],
        #  [3135836573, 3144325243], [3182772926, 3247886474], [3394879235, 3442085054], [3494879649, 3554945924],
        #  [3576751991, 3593250011], [3866824018, 3880397122], [4012252500, 4029569284], [4294967296, 4294967295]
        # ]
    print("########################")
