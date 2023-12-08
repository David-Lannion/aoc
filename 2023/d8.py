"""--- Day 8: Haunted Wasteland ---
You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""
import json
import math
import re
import time

example = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

example2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def is_end(s):
    # print("Is end :", s)
    for i in s:
        if i[2] != "Z":
            return False
    return True


def make_map(lines):
    map_data = {}
    positions = []
    for i in range(len(lines) - 1):
        cross = lines[i + 1]
        map_data[cross[0:3]] = {
            "L": cross[7:10],
            "R": cross[12:15]
        }
        if cross[2] == "A":
            positions.append(cross[0:3])
    with open('2023/d8.dot', 'w') as file:
        file.write("digraph day8 {\n")
        for m in map_data:
            file.write(f'  "{m}" -> "{map_data[m]["L"]}" \n')
            file.write(f'  "{m}" -> "{map_data[m]["R"]}" \n')
        file.write("}\n")
        file.close()
        exit()
    return map_data, positions


def c2023d8p1(data=example):
    lines = re.split(r"\n+", data)
    map_data, positions = make_map(lines)
    # print(json.dumps(map_data, indent=1))
    current_position = "AAA"
    directions = lines[0]
    dir_len = len(lines[0])
    step = 0
    while current_position != "ZZZ":
        current_position = map_data[current_position][directions[step % dir_len]]
        step += 1
    return step


def c2023d8p2(data=example2):
    lines = re.split(r"\n+", data)
    map_data, positions = make_map(lines)
    # print(json.dumps(map_data, indent=1))
    directions = lines[0]
    dir_len = len(lines[0])
    print(f"Found {len(map_data)} crossroads and {len(positions)} starting positions : ", positions)
    step = 0
    next_log = 100

    while not is_end(positions):
        dir_step = directions[step % dir_len]
        for i in range(len(positions)):
            positions[i] = map_data[positions[i]][dir_step]
        step += 1
        if step > next_log:
            print(f"Already took {step} steps, got ", positions)
            next_log *= 2

    print(f"It took {step} steps")
    return step


if __name__ == "__main__":
    print("########################")
    print("####    TEST ALGO   ####")
    # ok = "ok" if c2023d8p1() == 2 else "ko"
    # print(f"##  c2023d8p1 => {ok}    #")
    ok = "ok" if c2023d8p2() == 6 else "ko"
    print(f"##  c2023d8p2 => {ok}    #")
    print("########################")
    print("#   WITH PUZZLE INPUT  #")
    with open('2023/d8.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2023d8p1 => {c2023d8p1(input_data)} #")  # 13771
        print(f"# c2023d8p2 => {c2023d8p2(input_data)} #")
    print("########################")
