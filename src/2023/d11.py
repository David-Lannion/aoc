"""--- Day 11: Cosmic Expansion ---
    You continue following signs for "Hot Springs" and eventually come across an observatory.
    The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

    He doesn't know anything about the missing machine parts; he's only visiting for this research project.
    However, he confirms that the hot springs are the next-closest area likely to have people;
    he'll even take you straight there once he's done with today's observation analysis.

    Maybe you can help him with the analysis to speed things up?

    The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input).
    The image includes empty space (.) and galaxies (#). For example:

    ...#......
    .......#..
    #.........
    ..........
    ......#...
    .#........
    .........#
    ..........
    .......#..
    #...#.....
    The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies.
    However, there's a catch: the universe expanded in the time it took the light from those galaxies
    to reach the observatory.

    Due to something involving gravitational effects, only some space expands.
    In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

    In the above example, three columns and two rows contain no galaxies:

       v  v  v
     ...#......
     .......#..
     #.........
    >..........<
     ......#...
     .#........
     .........#
    >..........<
     .......#..
     #...#.....
       ^  ^  ^
    These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

    ....#........
    .........#...
    #............
    .............
    .............
    ........#....
    .#...........
    ............#
    .............
    .............
    .........#...
    #....#.......
    Equipped with this expanded universe, the shortest path between every pair of galaxies can be found.
    It can help to assign every galaxy a unique number:

    ....1........
    .........2...
    3............
    .............
    .............
    ........4....
    .5...........
    ............6
    .............
    .............
    .........7...
    8....9.......
    In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter.
    For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right
    exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

    For example, here is one of the shortest paths between galaxies 5 and 9:

    ....1........
    .........2...
    3............
    .............
    .............
    ........4....
    .5...........
    .##.........6
    ..##.........
    ...##........
    ....##...7...
    8....9.......
    This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9
    (the eight locations marked # plus the step onto galaxy 9 itself).
    Here are some other example shortest path lengths:

    Between galaxy 1 and galaxy 7: 15
    Between galaxy 3 and galaxy 6: 17
    Between galaxy 8 and galaxy 9: 5
    In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

    Expand the universe, then find the length of the shortest path between every pair of galaxies.
    What is the sum of these lengths?
"""
from ..day import DayBase

example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


class Universe:
    def __init__(self, data: str, size):
        self.initial = data.splitlines()
        self.galaxies = []
        self.nb_line = len(self.initial)
        self.nb_col = len(self.initial[0])
        self.galaxies_lines = [1] * self.nb_line
        self.galaxies_cols = [1] * self.nb_col
        self.expanded_galaxies = []
        for line in range(self.nb_line):
            for col in range(self.nb_col):
                if self.initial[line][col] != ".":
                    self.galaxies_lines[line] = 0
                    self.galaxies_cols[col] = 0
                    self.galaxies.append([line, col])
        for galaxy in self.galaxies:
            self.expanded_galaxies.append([galaxy[0] + (size - 1) * sum(self.galaxies_lines[:galaxy[0]]),
                                           galaxy[1] + (size - 1) * sum(self.galaxies_cols[:galaxy[1]])])

    @staticmethod
    def distance(g_1, g_2):
        return abs(g_1[0] - g_2[0]) + abs(g_1[1] - g_2[1])


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
def c2023d11p1(data=example):
    uni = Universe(data, 2)
    res = 0
    count = 0
    for galaxy in uni.expanded_galaxies:
        count += 1
        for paired in uni.expanded_galaxies[count:]:
            res += uni.distance(galaxy, paired)
    return res


def c2023d11p2(data=example, size=1):
    """--- Part Two ---
        The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

        Now, instead of the expansion you did before, make each empty row or column one million times larger.
        That is, each empty row should be replaced with 1000000 empty rows,
        and each empty column should be replaced with 1000000 empty columns.

        (In the example above, if each empty row or column were merely 10 times larger,
        the sum of the shortest paths between every pair of galaxies would be 1030.
        If each empty row or column were merely 100 times larger,
        the sum of the shortest paths between every pair of galaxies would be 8410.
        However, your universe will need to expand far beyond these values.)

        Starting with the same initial image, expand the universe according to these new rules,
        then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
    """
    uni = Universe(data, size)
    res = 0
    count = 0
    for galaxy in uni.expanded_galaxies:
        count += 1
        for paired in uni.expanded_galaxies[count:]:
            res += uni.distance(galaxy, paired)
    return res


if __name__ == "__main__":
    print("########################")
    print("####    TEST ALGO   ####")
    res = c2023d11p1()
    ok = "ok" if res == 374 else "ko"
    print(f"##  c2023d11p1 => {ok} {res}   #")
    res = c2023d11p2(example, 10)
    ok = "ok" if res == 1030 else "ko"
    print(f"##  c2023d11p2 => {ok} {res}  #")
    res = c2023d11p2(example, 100)
    ok = "ok" if res == 8410 else "ko"
    print(f"##  c2023d11p2 => {ok} {res}   #")
    print("########################")
    print("#   WITH PUZZLE INPUT  #")
    with open('2023/d11.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2023d11p1 => {c2023d11p1(input_data)} #")  # 13771
        print(f"# c2023d11p2 => {c2023d11p2(input_data, 1000000)} #")
    # print("########################")
