"""--- Day 14: Parabolic Reflector Dish ---
    You reach the place where all of the mirrors were pointing:
    a massive parabolic reflector dish attached to the side of another large mountain.

    The dish is made up of many small mirrors, but while the mirrors themselves are roughly
    in the shape of a parabolic reflector dish,
    each individual mirror seems to be pointing in slightly the wrong direction.
    If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

    This system must be what provides the energy for the lava! If you focus the reflector dish,
    maybe you can go where it's pointing and use the light to fix the lava production.

    Upon closer inspection, the individual mirrors each appear to be connected via an elaborate
    system of ropes and pulleys to a large metal platform below the dish.
    The platform is covered in large rocks of various shapes.
    Depending on their position, the weight of the rocks deforms the platform,
    and the shape of the platform controls which ropes move and ultimately the focus of the dish.

    In short: if you move the rocks, you can focus the dish.
    The platform even has a control panel on the side that lets you tilt it in one of four directions!
    The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place.
    You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
    Start by tilting the lever so all of the rocks will slide north as far as they will go:

    OOOO.#.O..
    OO..#....#
    OO..O##..O
    O..#.OO...
    ........#.
    ..#....#.#
    ..O..#.O.O
    ..O.......
    #....###..
    #....#....
    You notice that the support beams along the north side of the platform are damaged;
    to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

    The amount of load caused by a single rounded rock (O) is equal to the number of rows
    from the rock to the south edge of the platform, including the row the rock is on.
    (Cube-shaped rocks (#) don't contribute to load.)
    So, the amount of load caused by each rock in each row is as follows:

    OOOO.#.O.. 10
    OO..#....#  9
    OO..O##..O  8
    O..#.OO...  7
    ........#.  6
    ..#....#.#  5
    ..O..#.O.O  4
    ..O.......  3
    #....###..  2
    #....#....  1
    The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

    Tilt the platform so that the rounded rocks all roll north.
    Afterward, what is the total load on the north support beams?
"""
import json
import math
import re
import time
from PIL import Image

example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def c2023d14p1(data=example):
    print("")


def c2023d14p2(data=example):
    pass


if __name__ == "__main__":
    print("########################")
    print("####    TEST ALGO   ####")
    res = c2023d14p1()
    ok = "ok" if res == 405 else "ko"
    print(f"##  c2023d14p1 => {ok} {res}   #")
    ok = "ok" if c2023d14p2() == 6 else "ko"
    print(f"##  c2023d14p2 => {ok}    #")
    print("########################")
    print("#   WITH PUZZLE INPUT  #")
    with open('2023/d14.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2023d14p1 => {c2023d14p1(input_data)} #")  # 13771
        print(f"# c2023d14p2 => {c2023d14p2(input_data)} #")
    print("########################")
