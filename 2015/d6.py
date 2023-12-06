""""""
import re

example = """"""



def c2015d6p1(data_input="turn on 0,0 through 999,999"):
    screen = [[False] * 1000 for i in range(1000)]

    def parse(data, sc):
        line = re.match(r"(?P<instruction>turn on|turn off|toggle) "
                        r"(?P<x>\d+),(?P<y>\d+) through (?P<xb>\d+),(?P<yb>\d+)", data)
        match line["instruction"]:
            case "turn on":
                for x in range(int(line["x"]), int(line["xb"]) + 1):
                    for y in range(int(line["y"]), int(line["yb"]) + 1):
                        sc[x][y] = True
            case "turn off":
                for x in range(int(line["x"]), int(line["xb"]) + 1):
                    for y in range(int(line["y"]), int(line["yb"]) + 1):
                        sc[x][y] = False
            case "toggle":
                for x in range(int(line["x"]), int(line["xb"]) + 1):
                    for y in range(int(line["y"]), int(line["yb"]) + 1):
                        sc[x][y] = not sc[x][y]
            case "_":
                raise Exception("Unknown instruction")

    data_p = re.split(r"\n+", data_input)
    for d in data_p:
        print(d)
        parse(d, screen)
    cnt = 0
    for x in range(1000):
        for y in range(1000):
            cnt += 1 if screen[x][y] else 0
    print(cnt)


def c2015d6p2(data_input="turn on 0,0 through 999,999"):
    screen = [[0] * 1000 for i in range(1000)]

    def parse(data, sc):
        line = re.match(r"(?P<instruction>turn on|turn off|toggle) "
                        r"(?P<x>\d+),(?P<y>\d+) through (?P<xb>\d+),(?P<yb>\d+)", data)
        match line["instruction"]:
            case "turn on":
                for x in range(int(line["x"]), int(line["xb"]) + 1):
                    for y in range(int(line["y"]), int(line["yb"]) + 1):
                        sc[x][y] += 1
            case "turn off":
                for x in range(int(line["x"]), int(line["xb"]) + 1):
                    for y in range(int(line["y"]), int(line["yb"]) + 1):
                        sc[x][y] = max(0, sc[x][y] - 1)
            case "toggle":
                for x in range(int(line["x"]), int(line["xb"]) + 1):
                    for y in range(int(line["y"]), int(line["yb"]) + 1):
                        sc[x][y] += 2
            case "_":
                raise Exception("Unknown instruction")

    data_p = re.split(r"\n+", data_input)
    for d in data_p:
        # print(d)
        parse(d, screen)
    cnt = 0
    for x in range(1000):
        for y in range(1000):
            cnt += screen[x][y]
    print(cnt)


if __name__ == "__main__":
    print("######################")
    print("####  TEST ALGO   ####")
    ok = "ok" if c2015d6p1() == 142 else "ko"
    print(f"##  c2015d6p1 => {ok}  #")
    ok = "ok" if c2015d6p2() == 281 else "ko"
    print(f"##  c2015d6p2 => {ok}  #")
    print("######################")
    print("# WITH PUZZLE INPUT  #")
    with open('2015/d6.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2015d6p1 => {c2015d6p1(input_data)} #")
        print(f"# c2015d6p2 => {c2015d6p2(input_data)} #")
    print("######################")
