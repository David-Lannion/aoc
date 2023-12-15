""""""
import hashlib

example = """"""


def c2015d4p1(data="bgvyzdsv"):
    counter = -1
    found = False
    while not found:
        counter += 1
        md5 = hashlib.md5(f"{data}{counter}".encode()).hexdigest()
        if md5[0:5] == "00000":
            found = True
            print(f"{md5} at {counter}")
        if counter % 100000 == 0:
            print(f"Iteration {counter}")


def c2015d4p2(data="bgvyzdsv"):
    counter = -1
    found = False
    while not found:
        counter += 1
        md5 = hashlib.md5(f"{data}{counter}".encode()).hexdigest()
        if md5[0:6] == "000000":
            found = True
            print(f"{md5} at {counter}")
        if counter % 100000 == 0:
            print(f"Iteration {counter}")


if __name__ == "__main__":
    print("######################")
    print("####  TEST ALGO   ####")
    ok = "ok" if c2015d4p1() == 142 else "ko"
    print(f"##  c2015d4p1 => {ok}  #")
    ok = "ok" if c2015d4p2() == 281 else "ko"
    print(f"##  c2015d4p2 => {ok}  #")
    print("######################")
    print("# WITH PUZZLE INPUT  #")
    with open('2015/d4.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2015d4p1 => {c2015d4p1(input_data)} #")
        print(f"# c2015d4p2 => {c2015d4p2(input_data)} #")
    print("######################")
