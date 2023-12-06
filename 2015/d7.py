""""""
import re
import numpy

example = """"""


class Wire:
    wires = {}

    def __init__(self, name, a=None, b=None, t=""):
        self.name = name
        self.a = a
        self.b = b
        self.t = t
        self.value = None

    def get(self):
        def get(val):
            return numpy.uint16(val) if val[0] in "0123456789" else Wire.wires[val].get()

        if self.value is not None:
            return self.value
        match self.t:
            case "AND":
                self.value = get(self.a) & get(self.b)
            case "OR":
                self.value = get(self.a) | get(self.b)
            case "LSHIFT":
                self.value = get(self.a) << get(self.b)
            case "RSHIFT":
                self.value = get(self.a) >> get(self.b)
            case "NOT":
                self.value = ~ get(self.b)
            case "":
                self.value = get(self.a)
            case "_":
                raise Exception("Unknown instruction")

        return self.value

    @staticmethod
    def process(data):
        data_p = re.split(r"\n+", data)
        line_cnt = 0

        for line in data_p:
            line_cnt += 1
            info = re.match(
                r"^(?P<x>[\da-z]*) *(?P<instruction>AND|OR|LSHIFT|RSHIFT|NOT|) *(?P<y>[\da-z]*) -> (?P<dest>[a-z]+)",
                line)
            Wire.wires[info["dest"]] = Wire(info["dest"], info["x"], info["y"], info["instruction"])


def c2015d7p1(data_input="123 -> x"):
    Wire.process(data_input)
    return Wire.wires["a"].get()


def c2015d7p2(data_input="123 -> x"):
    Wire.process(data_input)
    Wire.wires["b"] = Wire("b", f"{Wire.wires['a'].get()}", "", "")
    return Wire.wires["a"].get()


if __name__ == "__main__":
    print("######################")
    print("####  TEST ALGO   ####")
    ok = "ok" if c2015d7p1() == 142 else "ko"
    print(f"##  c2015d7p1 => {ok}  #")
    ok = "ok" if c2015d7p2() == 281 else "ko"
    print(f"##  c2015d7p2 => {ok}  #")
    print("######################")
    print("# WITH PUZZLE INPUT  #")
    with open('2015/d7.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2015d7p1 => {c2015d7p1(input_data)} #")
        print(f"# c2015d7p2 => {c2015d7p2(input_data)} #")
    print("######################")
