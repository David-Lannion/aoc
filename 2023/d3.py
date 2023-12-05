"""--- Day 3: Gear Ratios ---
    You and the Elf eventually reach a gondola lift station;
    he says the gondola lift will take you up to the water source, but this is as far as he can bring you.
    You go inside.

    It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

    "Aaah!"
    You turn around to see a slightly-greasy Elf with a wrench and a look of surprise.
    "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now;
    it'll still be a while before I can fix it."
    You offer to help.
"""
import re

example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


class NBV:
    def __init__(self, lines, test, is_part2=False):
        self.lines = lines
        self.length = len(lines)
        self.test = test
        self.is_part2 = is_part2
        self.numbers = []
        self.gears = []

    def is_nb_valid(self, level, start, end, nb):
        search_from = max(0, int(start) - 1)
        search_to = max(0, int(end) + 1)
        level_min = max(0, level - 1)
        level_max = min(self.length - 1, level + 1)
        is_valid = False
        for l in range(level_min, level_max + 1):
            for c in range(search_from, min(search_to, len(self.lines[l]) - 1) + 1):
                if self.test(self.lines[l][c]):
                    is_valid = True
                    break
            if is_valid:
                if self.is_part2:
                    self.numbers.append([level, int(start), int(end), int(nb)])
                break
        return int(nb) if is_valid else 0

    def process_lines(self):
        cur_line = 0
        res = 0
        for line in self.lines:
            nb_start = None
            nb_end = None
            nb = ""
            for c in range(len(line)):
                if line[c] == "*":
                    self.gears.append([cur_line, c])
                if line[c] in "0123456789":
                    nb_start = c if nb_start is None else nb_start
                    nb_end = c
                    nb += line[c]
                    if c == len(line) - 1:
                        res += self.is_nb_valid(cur_line, nb_start, nb_end, nb)
                elif nb_start is not None:
                    res += self.is_nb_valid(cur_line, nb_start, nb_end, nb)
                    nb_start = None
                    nb_end = None
                    nb = ""
            cur_line += 1
        return res


def c2023d3p1(data=example):
    """Part 1

    The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one.
    If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

    :param data:
        The engine schematic (your puzzle input) consists of a visual representation of the engine.
        There are lots of numbers and symbols you don't really understand,
        but apparently any number adjacent to a symbol, even diagonally, is a "part number" and
        should be included in your sum. (Periods (.) do not count as a symbol.)
    :return:
        In this schematic, two numbers are not part numbers because they are not adjacent to a symbol:
        114 (top right) and 58 (middle right).
        Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

        Of course, the actual engine schematic is much larger.
        What is the sum of all of the part numbers in the engine schematic?
    """
    lines = re.split(r"\n+", data)
    nbv = NBV(lines, lambda a: a not in ".0123456789")
    res = nbv.process_lines()
    # print(f"Got {res}")
    return res


def c2023d3p2(data=example):
    """Part 2

    The engineer finds the missing part and installs it in the engine! As the engine springs to life,
    you jump in the closest gondola, finally ready to ascend to the water source.

    You don't seem to be going very fast, though. Maybe something is still wrong?
    Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

    Before you can explain the situation, she suggests that you look out the window.
    There stands the engineer, holding a phone in one hand and waving with the other.
    You're going so slowly that you haven't even left the station. You exit the gondola.

    :param data:
        Same as part 1
    :return:
        The missing part wasn't the only issue - one of the gears in the engine is wrong.
        A gear is any * symbol that is adjacent to exactly two part numbers.
        Its gear ratio is the result of multiplying those two numbers together.

        This time, you need to find the gear ratio of every gear and add them all up
        so that the engineer can figure out which gear needs to be replaced.

        In this schematic, there are two gears.
        The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345.
        The second gear is in the lower right; its gear ratio is 451490.
        (The * adjacent to 617 is not a gear because it is only adjacent to one part number.)
        Adding up all of the gear ratios produces 467835.

        What is the sum of all of the gear ratios in your engine schematic?
    """
    lines = re.split(r"\n+", data)
    nbv = NBV(lines, lambda a: a == "*", True)
    nbv.process_lines()

    # Got gears and numbers, now process
    gear_ratio = 0
    for gear in nbv.gears:
        adjacent = []
        for number in nbv.numbers:
            # check if number [level, start, end, nb] is adjacent to gear [level, position]
            if number[0] == gear[0]:
                if (number[2] == gear[1] - 1) or (number[1] == gear[1] + 1):
                    adjacent.append(number[3])
            elif number[0] == gear[0] + 1 or number[0] == gear[0] - 1:
                if number[1] - 1 <= gear[1] <= number[2] + 1:
                    adjacent.append(number[3])
        if len(adjacent) == 2:
            gear_ratio += adjacent[0] * adjacent[1]
    # print(f"Out of {len(nbv.gears)} gears and {len(nbv.numbers)}, got gear_ratio {gear_ratio}")
    return gear_ratio


if __name__ == "__main__":
    print("#########################")
    print("####    TEST ALGO    ####")
    ok = "ok" if c2023d3p1() == 4361 else "ko"
    print(f"##  c2023d3p1 => {ok}     #")
    ok = "ok" if c2023d3p2() == 467835 else "ko"
    print(f"##  c2023d3p2 => {ok}     #")
    print("#########################")
    print("#   WITH PUZZLE INPUT   #")
    with open('2023/d3.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2023d3p1 => {c2023d3p1(input_data)}   #")
        print(f"# c2023d3p2 => {c2023d3p2(input_data)} #")
    print("#########################")
