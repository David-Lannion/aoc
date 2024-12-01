""""""
import re

example = """"""


def c2015d2p1(data="2x3x4"):
    size = 0
    data_part = re.split(r"\s+", data)
    for input_str in data_part:
        lengths = [int(i) for i in input_str.split("x")]
        if len(lengths) != 3:
            raise Exception("error with " + input_str)
        squares = [lengths[0] * lengths[1], lengths[2] * lengths[1], lengths[0] * lengths[2]]
        size += min(squares) + 2 * sum(squares)
    print(size)
    return size


def c2015d2p2(data="2x3x4"):
    size = 0
    data_part = re.split(r"\s+", data)
    for input_str in data_part:
        lengths = sorted([int(i) for i in input_str.split("x")])
        if len(lengths) != 3:
            raise Exception("error with " + input_str)
        # squares = sorted([lengths[0] * lengths[1], lengths[2] * lengths[1], lengths[0] * lengths[2]])
        size += 2 * lengths[0] + 2 * lengths[1] + lengths[0] * lengths[1] * lengths[2]
    print(size)
    return size


if __name__ == "__main__":
    print("######################")
    print("####  TEST ALGO   ####")
    ok = "ok" if c2015d2p1() == 142 else "ko"
    print(f"##  c2015d2p1 => {ok}  #")
    ok = "ok" if c2015d2p2() == 281 else "ko"
    print(f"##  c2015d2p2 => {ok}  #")
    print("######################")
    print("# WITH PUZZLE INPUT  #")
    with open('2015/data/d2.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2015d2p1 => {c2015d2p1(input_data)} #")
        print(f"# c2015d2p2 => {c2015d2p2(input_data)} #")
    print("######################")
