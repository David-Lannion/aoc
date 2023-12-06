""""""
import re

example = """"""


def c2015d5p1(data_input="ugknbfddgicrmopn"):
    def nice(data):
        # does not have (ab|cd|pq|xy)
        nice = re.search(r"(ab|cd|pq|xy)", data) is None
        # contains [aeiou] at least 3 times
        nice = nice and (data.count("a") + data.count("e") + data.count("i") + data.count("o") + data.count("u")) > 2
        # contains at least a double letter
        nice = nice and re.search(r"(?P<letter>\w)(?P=letter)", data) is not None
        if nice:
            print("Nice !")
        else:
            print("Naughty O.O !")
        return 1 if nice else 0

    data_p = re.split(r"\s+", data_input)
    cnt = 0
    for d in data_p:
        cnt += nice(d)
    print(cnt)


def c2015d5p2(data_input="ugknbfddgicrmopn"):
    def nice(data):
        # contains at least one letter which repeats with exactly one letter between them
        nice = re.search(r"(?P<letter>\w)\w(?P=letter)", data) is not None
        # contains a pair of any two letters that appears at least twice in the string without overlapping
        nice = nice and re.search(r"(?P<pair>\w\w)\w*(?P=pair)", data) is not None
        if nice:
            print("Nice !")
        else:
            print("Naughty O.O !")
        return 1 if nice else 0

    data_p = re.split(r"\s+", data_input)
    cnt = 0
    for d in data_p:
        cnt += nice(d)
    print(cnt)


if __name__ == "__main__":
    print("######################")
    print("####  TEST ALGO   ####")
    ok = "ok" if c2015d5p1() == 142 else "ko"
    print(f"##  c2015d5p1 => {ok}  #")
    ok = "ok" if c2015d5p2() == 281 else "ko"
    print(f"##  c2015d5p2 => {ok}  #")
    print("######################")
    print("# WITH PUZZLE INPUT  #")
    with open('2015/d5.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2015d5p1 => {c2015d5p1(input_data)} #")
        print(f"# c2015d5p2 => {c2015d5p2(input_data)} #")
    print("######################")
