"""--- Day 10: Pipe Maze ---
    You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island.
    This island is surprisingly cold and there definitely aren't any thermals to glide on,
    so you leave your hang glider behind.

    You wander around for a while, but you don't find any people or animals.
    However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction;
    maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

    The landscape here is alien; even the flowers and trees are made of metal.
    As you stop to admire some metal grass, you notice something metallic scurry away
    in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen;
    if you want a better look, you'll need to get ahead of it.

    Scanning the area, you discover that the entire field you're standing on is densely packed with pipes;
    it was hard to tell at first because they're the same metallic silver color as the "ground".
    You make a quick sketch of all of the surface pipes you can see (your puzzle input).

    The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile,
    but your sketch doesn't show what shape the pipe has.
    Based on the acoustics of the animal's scurrying, you're confident
    the pipe that contains the animal is one large, continuous loop.

    For example, here is a square loop of pipe:

    .....
    .F-7.
    .|.|.
    .L-J.
    .....
    If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

    .....
    .S-7.
    .|.|.
    .L-J.
    .....
    In the above diagram, the S tile is still a 90-degree F bend:
    you can tell because of how the adjacent pipes connect to it.

    Unfortunately, there are also many pipes that aren't connected to the loop!
    This sketch shows the same loop as above:

    -L|F7
    7S-7|
    L|7||
    -L-J|
    L|-JF
    In the above diagram, you can still figure out which pipes form the main loop:
    they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on.
    Every pipe in the main loop connects to its two neighbors
    (including S, which will have exactly two pipes connecting to it, and which is assumed
    to connect back to those two pipes).

    Here is a sketch that contains a slightly more complex main loop:

    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...
    Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

    7-F7-
    .FJ|7
    SJLL7
    |F--J
    LJ.LJ
    If you want to get out ahead of the animal, you should find the tile in the loop
    that is farthest from the starting position. Because the animal is in the pipe,
    it doesn't make sense to measure this by direct distance.
    Instead, you need to find the tile that would take the longest number of steps along
    the loop to reach from the starting point - regardless of which way around the loop the animal went.

    In the first example with the square loop:

    .....
    .S-7.
    .|.|.
    .L-J.
    .....
    You can count the distance each tile in the loop is from the starting point like this:

    .....
    .012.
    .1.3.
    .234.
    .....
    In this example, the farthest point from the start is 4 steps away.

    Here's the more complex loop again:

    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...
    Here are the distances for each tile on that loop:

    ..45.
    .236.
    01.78
    14567
    23...
    Find the single giant loop starting at S.
    How many steps along the loop does it take to get from the starting position
    to the point farthest from the starting position?
"""
import re
from PIL import Image
from ..day import DayBase

example = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

example2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


class Node:
    bkd_north = "-LJ."
    bkd_south = "-7F."
    bkd_west = "|7J."
    bkd_est = "|LF."

    def __init__(self, x: int, y: int, mapped):
        self.t_tube = mapped[x][y]
        self.value = None
        self.x = x
        self.y = y
        self.road = None
        # neighbours
        self.n = None
        self.s = None
        self.e = None
        self.w = None
        # angles
        self.nw = 0
        self.sw = 0
        self.ne = 0
        self.se = 0

    @staticmethod
    def map_north(map_, x, y):
        return map_[x - 1][y]

    @staticmethod
    def map_south(map_, x, y):
        return map_[x + 1][y]

    @staticmethod
    def map_west(map_, x, y):
        return map_[x][y - 1]

    @staticmethod
    def map_est(map_, x, y):
        return map_[x][y + 1]

    @staticmethod
    def blocked_north(map_, x, y):
        return map_[x - 1][y] in Node.bkd_north

    @staticmethod
    def blocked_south(map_, x, y):
        return map_[x + 1][y] in Node.bkd_south

    @staticmethod
    def blocked_west(map_, x, y):
        return map_[x][y - 1] in Node.bkd_west

    @staticmethod
    def blocked_est(map_, x, y):
        return map_[x][y + 1] in Node.bkd_est

    def clean(self, mapped, mapping):
        # The pipes are arranged in a two-dimensional grid of tiles:
        x = self.x
        y = self.y
        width = len(mapped[self.y]) - 1
        height = len(mapped) - 1
        changed = False
        match self.t_tube:
            case "|":
                # | is a vertical pipe connecting north and south.
                if x == 0 or x == height or self.blocked_north(mapped, x, y) or self.blocked_south(mapped, x, y):
                    self.t_tube = "."
                    mapped[x][y] = "."
                    changed = True
                else:
                    self.n = self.map_north(mapping, x, y)
                    self.s = self.map_south(mapping, x, y)
                    self.road = [self.n, self.s]
            case "-":
                # - is a horizontal pipe connecting east and west.
                # print(x, y, height, width)
                if y == 0 or y == width or self.blocked_west(mapped, x, y) or self.blocked_est(mapped, x, y):
                    self.t_tube = "."
                    mapped[x][y] = "."
                    changed = True
                else:
                    self.e = self.map_est(mapping, x, y)
                    self.w = self.map_west(mapping, x, y)
                    self.road = [self.e, self.w]
            case "L":
                # L is a 90-degree bend connecting north and east.
                if x == 0 or y == width or self.blocked_est(mapped, x, y) or self.blocked_north(mapped, x, y):
                    self.t_tube = "."
                    mapped[x][y] = "."
                    changed = True
                else:
                    self.n = self.map_north(mapping, x, y)
                    self.e = self.map_est(mapping, x, y)
                    self.road = [self.n, self.e]
            case "J":
                # J is a 90-degree bend connecting north and west.
                if x == 0 or y == 0 or self.blocked_north(mapped, x, y) or self.blocked_west(mapped, x, y):
                    self.t_tube = "."
                    mapped[x][y] = "."
                    changed = True
                else:
                    self.n = self.map_north(mapping, x, y)
                    self.w = self.map_west(mapping, x, y)
                    self.road = [self.n, self.w]
            case "7":
                # 7 is a 90-degree bend connecting south and west.
                if y == 0 or x == height or self.blocked_west(mapped, x, y) or self.blocked_south(mapped, x, y):
                    self.t_tube = "."
                    mapped[x][y] = "."
                    changed = True
                else:
                    self.w = self.map_west(mapping, x, y)
                    self.s = self.map_south(mapping, x, y)
                    self.road = [self.w, self.s]
            case "F":
                # F is a 90-degree bend connecting south and east.
                if y == width or x == height or self.blocked_south(mapped, x, y) or self.blocked_est(mapped, x, y):
                    self.t_tube = "."
                    mapped[x][y] = "."
                    changed = True
                else:
                    self.s = self.map_south(mapping, x, y)
                    self.e = self.map_est(mapping, x, y)
                    self.road = [self.s, self.e]
            # case ".":
            #     # . is ground; there is no pipe in this tile.
            #     pass
            case "S":
                # S is the starting position of the animal; there is a pipe on this tile,
                # but your sketch doesn't show what shape the pipe has
                self.n = self.map_north(mapping, x, y)
                self.s = self.map_south(mapping, x, y)
                self.e = self.map_est(mapping, x, y)
                self.w = self.map_west(mapping, x, y)
                Labi.start = self
        return 1 if changed else 0

    def go(self):
        # road_a = []
        # road_b = []
        # t_tube = None
        self.value = 0
        walker_a = [self, None]
        walker_b = [self, None]
        if self.n.s is None:
            if self.s.n is None:
                # t_tube = "-"
                walker_a[1] = self.e
                # road_a.append(self.e)
                walker_b[1] = self.w
                # road_b.append(self.w)
            elif self.w.e is None:
                # t_tube = "F"
                walker_a[1] = self.s
                # road_a.append(self.s)
                walker_b[1] = self.e
                # road_b.append(self.e)
            else:
                # t_tube = "7"
                walker_a[1] = self.s
                # road_a.append(self.s)
                walker_b[1] = self.w
                # road_b.append(self.w)
        else:
            if self.s.n is not None:
                # t_tube = "|"
                walker_a[1] = self.s
                # road_a.append(self.s)
                walker_b[1] = self.n
                # road_b.append(self.n)
            elif self.w.e is not None:
                # t_tube = "J"
                walker_a[1] = self.n
                # road_a.append(self.n)
                walker_b[1] = self.w
                # road_b.append(self.w)
            else:
                # t_tube = "L"
                walker_a[1] = self.n
                # road_a.append(self.n)
                walker_b[1] = self.e
                # road_b.append(self.e)
        # if t_tube is None:
        #     raise Exception("Starting point type evaluation failed !")
        res = 1
        walker_a[1].value = 1
        walker_b[1].value = 1
        while self.next(walker_a, walker_b):
            res += 1
        return res

    @staticmethod
    def next(w_a, w_b):
        # print("#######################")
        # print(w_a[1].x, w_a[1].y, w_a[1].t_tube, w_a[0].value)
        # print(w_b[1].x, w_b[1].y, w_b[1].t_tube, w_b[0].value)
        # val = w_a[0].value + 1
        val = w_b[1].value + 1
        if w_a[0] == w_a[1].road[0]:
            w_a[0] = w_a[1]
            w_a[1] = w_a[1].road[1]
        else:
            w_a[0] = w_a[1]
            w_a[1] = w_a[1].road[0]
        # #####
        if w_b[0] == w_b[1].road[0]:
            w_b[0] = w_b[1]
            w_b[1] = w_b[1].road[1]
        else:
            w_b[0] = w_b[1]
            w_b[1] = w_b[1].road[0]
        # #####
        if w_b[1].value is not None or w_a[1].value is not None:
            return False
        else:
            w_b[1].value = val
            w_a[1].value = val
            return True


class Labi:
    lc = 255 << 16
    bc = 255 << 8
    sc = 255

    png = {
        "|": ((0, 1, 0), (0, 1, 0), (0, 1, 0)),
        "-": ((0, 0, 0), (1, 1, 1), (0, 0, 0)),
        "L": ((0, 1, 0), (0, 1, 1), (0, 0, 0)),
        "J": ((0, 1, 0), (1, 1, 0), (0, 0, 0)),
        "7": ((0, 0, 0), (1, 1, 0), (0, 1, 0)),
        "F": ((0, 0, 0), (0, 1, 1), (0, 1, 0)),
        ".": ((0, 0, 0), (0, 0, 0), (0, 0, 0)),
        "S": ((1, 1, 1), (1, 1, 1), (1, 1, 1)),
    }
    start = None

    def __init__(self, data):
        self.lines = [list(line) for line in re.split(r"\n+", data)]
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        self.mapping: list[list[Node]] = [
            [Node(x, y, self.lines) for y in range(self.width)] for x in range(self.height)
        ]

    def clean(self):
        changed = 1
        while changed > 0:
            changed = self.clean0()

    def clean0(self):
        change = 0
        # print("Cleaning")
        for x in range(self.height):
            for y in range(self.width):
                change += self.mapping[x][y].clean(self.lines, self.mapping)
        return change

    def clean2(self):
        # print("Cleaning 2")
        for x in range(self.height):
            for y in range(self.width):
                n = self.mapping[x][y]
                if n != Labi.start and n.value is None:
                    n.t_tube = "."
                    n.s = n.e = n.w = n.n = None

    def make_png(self, png):
        print("Make PNG")
        img = Image.new("RGB", [self.width * 3, self.height * 3])
        for i in range(self.width):
            for j in range(self.height):
                block = self.png[self.lines[j][i]]
                for a in range(3):
                    for b in range(3):
                        img.putpixel([3 * i + a, 3 * j + b], block[b][a] * Labi.lc)
        img.show()
        img.save(png)

    def make_png2(self, png):
        print("Make PNG")
        img = Image.new("RGB", [self.width * 3, self.height * 3])
        for i in range(self.width):
            for j in range(self.height):
                block = self.png[self.mapping[j][i].t_tube]
                for a in range(3):
                    for b in range(3):
                        img.putpixel([3 * i + a, 3 * j + b], block[b][a])
        # for i in range(self.width * 3):
        #     for j in range(self.height * 3):
        #         img.getpixel([i, j])
        #         pass
        img.show()
        img.save(png)


class Day(DayBase):
    png_base = "./src/2023/data/d10_p"
    png_type = ""

    def do(self):
        Day.png_type = "e"
        self.test(8, 10, example)
        Day.png_type = ""
        self.run(6_846, None)

    @staticmethod
    def part1(data=example):
        labi = Labi(data)
        labi.make_png(f"{Day.png_base}1{Day.png_type}.png")
        labi.clean()
        if Labi.start is not None:
            return Labi.start.go()
        # labi.make_png()

    @staticmethod
    def part2(data=example):
        """--- Part Two ---
            You quickly reach the farthest point of the loop, but the animal never emerges.
            Maybe its nest is within the area enclosed by the loop?

            To determine whether it's even worth taking the time to search for such a nest,
            you should calculate how many tiles are contained within the loop. For example:

            ...........
            .S-------7.
            .|F-----7|.
            .||.....||.
            .||.....||.
            .|L-7.F-J|.
            .|..|.|..|.
            .L--J.L--J.
            ...........
            The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below).
            The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

            ...........
            .S-------7.
            .|F-----7|.
            .||OOOOO||.
            .||OOOOO||.
            .|L-7OF-J|.
            .|II|O|II|.
            .L--JOL--J.
            .....O.....
            In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside
            the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still
            outside the loop:

            ..........
            .S------7.
            .|F----7|.
            .||OOOO||.
            .||OOOO||.
            .|L-7F-J|.
            .|II||II|.
            .L--JL--J.
            ..........
            In both of the above examples, 4 tiles are enclosed by the loop.

            Here's a larger example:

            .F----7F7F7F7F-7....
            .|F--7||||||||FJ....
            .||.FJ||||||||L7....
            FJL7L7LJLJ||LJ.L-7..
            L--J.L7...LJS7F-7L7.
            ....F-J..F7FJ|L7L7L7
            ....L7.F7||L7|.L7L7|
            .....|FJLJ|FJ|F7|.LJ
            ....FJL-7.||.||||...
            ....L---J.LJ.LJLJ...
            The above sketch has many random bits of ground, some of which are in the loop (I) and
            some of which are outside it (O):

            OF----7F7F7F7F-7OOOO
            O|F--7||||||||FJOOOO
            O||OFJ||||||||L7OOOO
            FJL7L7LJLJ||LJIL-7OO
            L--JOL7IIILJS7F-7L7O
            OOOOF-JIIF7FJ|L7L7L7
            OOOOL7IF7||L7|IL7L7|
            OOOOO|FJLJ|FJ|F7|OLJ
            OOOOFJL-7O||O||||OOO
            OOOOL---JOLJOLJLJOOO
            In this larger example, 8 tiles are enclosed by the loop.

            Any tile that isn't part of the main loop can count as being enclosed by the loop.
            Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

            FF7FSF7F7F7F7F7F---7
            L|LJ||||||||||||F--J
            FL-7LJLJ||||||LJL-77
            F--JF--7||LJLJ7F7FJ-
            L---JF-JLJ.||-FJLJJ7
            |F|F-JF---7F7-L7L|7|
            |FFJF7L7F-JF7|JL---7
            7-L-JL7||F7|L7F-7F7|
            L.L7LFJ|||||FJL7||LJ
            L7JLJL-JLJLJL--JLJ.L
            Here are just the tiles that are enclosed by the loop marked with I:

            FF7FSF7F7F7F7F7F---7
            L|LJ||||||||||||F--J
            FL-7LJLJ||||||LJL-77
            F--JF--7||LJLJIF7FJ-
            L---JF-JLJIIIIFJLJJ7
            |F|F-JF---7IIIL7L|7|
            |FFJF7L7F-JF7IIL---7
            7-L-JL7||F7|L7F-7F7|
            L.L7LFJ|||||FJL7||LJ
            L7JLJL-JLJLJL--JLJ.L
            In this last example, 10 tiles are enclosed by the loop.

            Figure out whether you have time to search for the nest by calculating the area within the loop.
            How many tiles are enclosed by the loop?
        """
        labi = Labi(data)
        # labi.make_png(f"{Day.png_base}2{Day.png_type}.png")
        labi.clean0()
        if Labi.start is not None:
            res = Labi.start.go()
        labi.clean2()
        labi.make_png2(f"{Day.png_base}2{Day.png_type}.png")
        return res


if __name__ == "__main__":
    print("########################")
    print("####    TEST ALGO   ####")
    ok = "ok" if c2023d10p1() == 8 else "ko"
    print(f"##  c2023d10p1 => {ok}    #")
    ok = "ok" if c2023d10p2() == 10 else "ko"
    print(f"##  c2023d10p2 => {ok}    #")
    # print("########################")
    # print("#   WITH PUZZLE INPUT  #")
    # with open('2023/d10.txt', 'r') as file:
    #     input_data: str = file.read()
    #     print(f"# c2023d10p1 => {c2023d10p1(input_data, './2023/d10_p1.png')} #")  # 13771
    #     print(f"# c2023d10p2 => {c2023d10p2(input_data, './2023/d10_p1.png')} #")
    print("########################")
