"""--- Day 1: Trebuchet?! ---

    Something is wrong with global snow production, and you've been selected to take a look.
    The Elves have even given you a map; on it, they've used stars to mark the top fifty locations
    that are likely to be having problems.

    You've been doing this long enough to know that to restore snow operations,
    you need to check all fifty stars by December 25th.

    Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar;
    the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

    You try to ask why they can't just use a weather machine ("not powerful enough") and
    where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions")
    and hang on did you just say the sky ("of course, where do you think snow comes from")
    when you realize that the Elves are already loading you into a trebuchet
    ("please hold still, we need to strap you in").

    As they're making the final adjustments, they discover that their calibration document (your puzzle input)
    has been amended by a very young Elf who was apparently just excited to show off her art skills.
    Consequently, the Elves are having trouble reading the values on the document.
"""
import re
from ..day import DayBase

example = """z1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

example_p2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


class Day(DayBase):
    def do(self):
        self.test(142, 281, example, example_p2)
        self.run(54388, 53515)

    @staticmethod
    def part1(data=example):
        """Part 1

        The newly-improved calibration document consists of lines of text; each line originally contained
        a specific calibration value that the Elves now need to recover.
        On each line, the calibration value can be found by combining the first digit and the last digit
        (in that order) to form a single two-digit number.

        :param data: str
            Default is an example.
            In this example, the calibration values of these four lines are 12, 38, 15, and 77.
            Adding these together produces 142.

        :return: Consider your entire calibration document. What is the sum of all of the calibration values?
        """
        lines = re.split(r"\n+", data)
        counter = 0
        for lin in lines:
            no_alpha = re.sub(r"[a-zA-Z\s]+", "", lin)
            counter += int(no_alpha[0] + no_alpha[-1])
        # print(f"c2023d1p1 -> {counter}")
        return counter

    @staticmethod
    def part2(data=example_p2):
        """Part 2

        Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters:
        one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

        Equipped with this new information, you now need to find the real first and last digit on each line.

        :param data:
            Default is an example.
            In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76.
            Adding these together produces 281.
        :return:
            What is the sum of all of the calibration values?
        """
        lines = re.split(r"\n+", data)
        counter = 0
        for lin in lines:
            lin2 = re.sub(r"one", "o1ne", lin)
            lin2 = re.sub(r"two", "t2wo", lin2)
            lin2 = re.sub(r"three", "t3hree", lin2)
            lin2 = re.sub(r"four", "f4our", lin2)
            lin2 = re.sub(r"five", "f5ive", lin2)
            lin2 = re.sub(r"six", "s6ix", lin2)
            lin2 = re.sub(r"seven", "se7ven", lin2)
            lin2 = re.sub(r"eight", "ei8ght", lin2)
            lin2 = re.sub(r"nine", "ni9ne", lin2)
            no_alpha = re.sub(r"[a-zA-Z\s]+", "", lin2)
            # print(lin2)
            # print(int(no_alpha[0] + no_alpha[-1]))
            counter += int(no_alpha[0] + no_alpha[-1])
        # print(f"c2023d1p2 -> {counter}")
        return counter
