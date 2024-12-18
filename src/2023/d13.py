"""--- Day 13: Point of Incidence ---
    With your help, the hot springs team locates an appropriate spring which launches you neatly and
    precisely up to the edge of Lava Island.

    There's just one problem: you don't see any lava.

    You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around.
    After a while, you make your way to a nearby cluster of mountains only to discover that the valley
    between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way;
    perhaps you should head in that direction?

    As you move through the valley of mirrors, you find that several of them have fallen from the large
    metal frames keeping them in place.
    The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles.
    Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to
    run into a mirror.

    You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input);
    perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

    For example:

    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.

    #...##..#
    #....#..#
    ..##..###
    #####.##.
    #####.##.
    ..##..###
    #....#..#
    To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal
    line between two rows or across a vertical line between two columns.

    In the first pattern, the reflection is across a vertical line between two columns;
    arrows on each of the two columns point at the line between the columns:

    123456789
        ><
    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.
        ><
    123456789
    In this pattern, the line of reflection is the vertical line between columns 5 and 6.
    Because the vertical line is not perfectly in the middle of the pattern,
    part of the pattern (column 1) has nowhere to reflect onto and can be ignored;
    every other column has a reflected column within the pattern and must match exactly:
    column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

    The second pattern reflects across a horizontal line instead:

    1 #...##..# 1
    2 #....#..# 2
    3 ..##..### 3
    4v#####.##.v4
    5^#####.##.^5
    6 ..##..### 6
    7 #....#..# 7
    This pattern reflects across the horizontal line between rows 4 and 5.
    Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern,
    row 1 doesn't need to match anything.
    The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

    To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection;
    to that, also add 100 multiplied by the number of rows above each horizontal line of reflection.
    In the above example, the first pattern's vertical line has 5 columns to its left and
    the second pattern's horizontal line has 4 rows above it, a total of 405.

    Find the line of reflection in each of the patterns in your notes.
    What number do you get after summarizing all of your notes?
"""
import re
from ..day import DayBase

example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


class Mirror:
    def __init__(self, data):
        # To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection;
        #     to that, also add 100 multiplied by the number of rows above each horizontal line of reflection.
        #     In the above example, the first pattern's vertical line has 5 columns to its left and
        #     the second pattern's horizontal line has 4 rows above it, a total of 405.
        self.mirror = data.splitlines()
        self.height = len(self.mirror)
        self.width = len(self.mirror[0])
        # print("[w, h]", [self.width, self.height])
        self.t_mirror = ["".join([self.mirror[j][i] for j in range(self.height)]) for i in range(self.width)]
        self.vertical = None
        self.horizontal = None
        self.value = 0

        # Check horizontal mirroring
        self.check_horizontal_mirroring()
        # Check vertical mirroring
        self.check_vertical_mirroring()

        # Process value
        self.value = self.val()
        # print(f"Vertical : {self.vertical}")
        # print(f"Horizontal : {self.horizontal}")

    def val(self):
        value = 0
        if self.vertical is not None:
            value += self.vertical + 1
        if self.horizontal is not None:
            value += 100 * (self.horizontal + 1)
        return value

    def val2(self, base):
        value = 0
        if self.vertical is not None and base.vertical != self.vertical:
            value += self.vertical + 1
        if self.horizontal is not None and base.horizontal != self.horizontal:
            value += 100 * (self.horizontal + 1)
        return value

    @staticmethod
    def check_line(mirror: list, line: int, length: int):
        check = True
        # print("Got line ", line)
        # print([length - line - 2, line])
        for reflect_line in range(max(0, min(length - line - 2, line)) + 1):
            if mirror[line - reflect_line] != mirror[line + 1 + reflect_line]:
                check = False
                break
        return check

    def check_horizontal_mirroring(self):
        for line in range(self.height - 1):
            if self.mirror[line] == self.mirror[line + 1]:
                if Mirror.check_line(self.mirror, line, self.height):
                    self.horizontal = line
                    break

    def check_vertical_mirroring(self):
        # Check vertical mirroring
        for line in range(self.width - 1):
            if self.t_mirror[line] == self.t_mirror[line + 1]:
                if Mirror.check_line(self.t_mirror, line, self.width):
                    self.vertical = line
                    break

    @staticmethod
    def find_smudge(data):
        mirror = data.splitlines()
        mirror_base = Mirror(data)
        res = []
        mirror_x = [i for i in mirror]
        for x in range(len(mirror)):
            for y in range(len(mirror[0])):
                mirror_x[x] = Mirror.set_char(mirror[x], y, "." if mirror[x][y] == "#" else "#")
                mirror_c = Mirror("\n".join(mirror_x))
                res.append(mirror_c.val2(mirror_base))
            mirror_x[x] = mirror[x]
        return max(res) if len(res) > 0 else 0

    @staticmethod
    def set_char(string, position, valeur):
        s = list(string)
        s[position] = valeur
        return "".join(s)


class Day(DayBase):
    def do(self):
        self.test(405, 400, example)
        self.run(34_918, None)  # 22_820 < res_p2 < 40_938

    @staticmethod
    def part1(data=example):
        mirrors = re.split("\n\n+", data)
        res = 0
        for m in mirrors:
            res += Mirror(m).value
            # print(res)
        return res

    @staticmethod
    def part2(data=example):
        """--- Part Two ---
            You resume walking through the valley of mirrors and - SMACK! - run directly into one.
            Hopefully nobody was watching, because that must have been pretty embarrassing.

            Upon closer inspection, you discover that every mirror has exactly one smudge:
            exactly one . or # should be the opposite type.

            In each pattern, you'll need to locate and fix the smudge
            that causes a different reflection line to be valid.
            (The old reflection line won't necessarily continue being valid after the smudge is fixed.)

            Taking the above example, the first pattern's smudge is in the top-left corner.
            If the top-left # were instead ., it would have a different, horizontal line of reflection:

            1 ..##..##. 1
            2 ..#.##.#. 2
            3v##......#v3
            4^##......#^4
            5 ..#.##.#. 5
            6 ..##..##. 6
            7 #.#.##.#. 7
            With the smudge in the top-left corner repaired, a new horizontal line of reflection
            between rows 3 and 4 now exists.
            Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly:
            row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

            In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:

            1v#...##..#v1
            2^#...##..#^2
            3 ..##..### 3
            4 #####.##. 4
            5 #####.##. 5
            6 ..##..### 6
            7 #....#..# 7
            Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

            Summarize your notes as before, but instead use the new different reflection lines.
            In this example, the first pattern's new horizontal line has 3 rows above it and
            the second pattern's new horizontal line has 1 row above it, summarizing to the value 400.

            In each pattern, fix the smudge and find the different line of reflection.
            What number do you get after summarizing the new reflection line in each pattern in your notes?
        :param data:
        :return:
        """
        mirrors = re.split("\n\n+", data)
        res = 0
        for m in mirrors:
            res += Mirror.find_smudge(m)
        return res
