"""--- Day 2: Cube Conundrum ---

    You're launched high into the atmosphere! The apex of your trajectory just barely reaches
    the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves.
    It's quite cold, but you don't see much snow. An Elf runs over to greet you.

    The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow.
    He'll be happy to explain the situation, but it's a bit of a walk, so you have some time.
    They don't get many visitors up here; would you like to play a game in the meantime?
"""
import re

example = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def c2023d2p1(games=example):
    """Part 1

    As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue.
    Each time you play this game, he will hide a secret number of cubes of each color in the bag,
    and your goal is to figure out information about the number of cubes.

    To get information, once a bag has been loaded with cubes, the Elf will reach into the bag,
    grab a handful of random cubes, show them to you, and then put them back in the bag.
    He'll do this a few times per game.


    :param games:
        You play several games and record the information from each game (your puzzle input).
        Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated
        list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).
    :return:
        Default is the example.
        In game 1, three sets of cubes are revealed from the bag (and then put back again).
        The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes;
        the third set is only 2 green cubes.

        The Elf would first like to know which games would have been possible
        if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

        In the example above, games 1, 2, and 5 would have been possible
        if the bag had been loaded with that configuration.
        However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once;
        similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once.
        If you add up the IDs of the games that would have been possible, you get 8.

        Determine which games would have been possible if the bag had been loaded with
        only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
    """
    base = {"green": 13, "red": 12, "blue": 14}
    data_p = re.split(r"\n+", games)
    game_add = 0
    for d in data_p:
        sp1 = re.match(r"Game (?P<game_id>\d+): (?P<sets>.*)", d)
        sets = re.split(";", sp1["sets"])
        valid_game = True
        for s in sets:
            colors = re.split(",", s)
            for c in colors:
                # print(c)
                c_info = re.match(r"\s*(?P<nb>\d+)\s+(?P<color>[a-z]+)", c)
                if int(c_info["nb"]) > base.get(c_info["color"], 0):
                    valid_game = False
        if valid_game:
            game_add += int(sp1["game_id"])
    # print(f"Got {game_add}")
    return game_add


def c2023d2p2(games=example):
    """Part 2

    The Elf says they've stopped producing snow because they aren't getting any water!
    He isn't sure why the water stopped;
    however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!

    :param games:
        Same as part1
    :return:
        As you continue your walk, the Elf poses a second question: in each game you played,
        what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

        The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
        The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively.
        Adding up these five powers produces the sum 2286.

        For each game, find the minimum set of cubes that must have been present.
        What is the sum of the power of these sets?
    """
    data_p = re.split(r"\n+", games)
    game_add = 0
    for d in data_p:
        sp1 = re.match(r"Game (?P<game_id>\d+): (?P<sets>.*)", d)
        sets = re.split(";", sp1["sets"])
        base = {"green": 0, "red": 0, "blue": 0}
        for s in sets:
            colors = re.split(",", s)
            for c in colors:
                # print(c)
                c_info = re.match(r"\s*(?P<nb>\d+)\s+(?P<color>[a-z]+)", c)
                if int(c_info["nb"]) > base.get(c_info["color"], 0):
                    base[c_info["color"]] = int(c_info["nb"])
        mult = 1
        for c in base:
            mult *= base[c]
        game_add += mult
    # print(f"Got {game_add}")
    return game_add


if __name__ == "__main__":
    print("######################")
    print("####  TEST ALGO   ####")
    ok = "ok" if c2023d2p1() == 8 else "ko"
    print(f"##  c2023d2p1 => {ok}  #")
    ok = "ok" if c2023d2p2() == 2286 else "ko"
    print(f"##  c2023d2p2 => {ok}  #")
    print("######################")
    print("# WITH PUZZLE INPUT  #")
    with open('2023/d2.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2023d2p1 => {c2023d2p1(input_data)}  #")
        print(f"# c2023d2p2 => {c2023d2p2(input_data)} #")
    print("######################")
