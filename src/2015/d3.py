""""""
import re

example = """"""


def c2015d3p1(data="^>v<"):
    position = [0, 0]
    map_cdo = {"0": {"0": 1}}
    visited_house = 1
    data_part = re.split(r"\s+", data)
    for line in data_part:
        for c in line:
            match c:
                case "<":
                    position[0] -= 1
                case ">":
                    position[0] += 1
                case "^":
                    position[1] += 1
                case "v":
                    position[1] -= 1
                case "_":
                    raise Exception("Unknown char")
            x = str(position[0])
            y = str(position[1])
            if x not in map_cdo:
                map_cdo[x] = {}
            if y not in map_cdo[x]:
                map_cdo[x][y] = 1
                visited_house += 1
            else:
                map_cdo[x][y] += 1
    print(visited_house)


def c2015d3p2(data="^>v<"):
    position_santa = [0, 0]
    position_robot = [0, 0]
    map_cdo = {"0": {"0": 1}}
    visited_house = 1
    toggle = True

    def move(pos, map_):
        vis = 0
        match c:
            case "<":
                pos[0] -= 1
            case ">":
                pos[0] += 1
            case "^":
                pos[1] += 1
            case "v":
                pos[1] -= 1
            case "_":
                raise Exception("Unknown char")
        x = str(pos[0])
        y = str(pos[1])
        if x not in map_:
            map_[x] = {}
        if y not in map_[x]:
            map_[x][y] = 1
            vis += 1
        else:
            map_[x][y] += 1
        return vis

    data_part = re.split(r"\s+", data)
    for line in data_part:
        for c in line:
            visited_house += move(position_santa if toggle else position_robot, map_cdo)
            toggle = not toggle
    print(visited_house)


if __name__ == "__main__":
    print("######################")
    print("####  TEST ALGO   ####")
    ok = "ok" if c2015d3p1() == 142 else "ko"
    print(f"##  c2015d3p1 => {ok}  #")
    ok = "ok" if c2015d3p2() == 281 else "ko"
    print(f"##  c2015d3p2 => {ok}  #")
    print("######################")
    print("# WITH PUZZLE INPUT  #")
    with open('2015/data/d3.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2015d3p1 => {c2015d3p1(input_data)} #")
        print(f"# c2015d3p2 => {c2015d3p2(input_data)} #")
    print("######################")
