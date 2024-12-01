"""--- Day 1: Not Quite Lisp ---
Santa was hoping for a white Christmas, but his weather machine's "snow" function is powered by stars, and he's fresh out! To save Christmas, he needs you to collect fifty stars by December 25th.

Collect stars by helping Santa solve puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't find the right floor - the directions he got are a little confusing. He starts on the ground floor (floor 0) and then follows the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will never find the top or bottom floors.

For example:

(()) and ()() both result in floor 0.
((( and (()(()( both result in floor 3.
))((((( also results in floor 3.
()) and ))( both result in floor -1 (the first basement level).
))) and )())()) both result in floor -3.
To what floor do the instructions take Santa?

Your puzzle answer was 138.

--- Part Two ---
Now, given the same instructions, find the position of the first character that causes him to enter the basement (floor -1). The first character in the instructions has position 1, the second character has position 2, and so on.

For example:

) causes him to enter the basement at character position 1.
()()) causes him to enter the basement at character position 5.
What is the position of the character that causes Santa to first enter the basement?
"""
example = "))((((("


def c2015d1p1(input_str=example):
    floor = input_str.count('(') - input_str.count(')')
    # print(floor)
    return floor


def c2015d1p2(input_str=example):
    floor = 0
    position = 0
    for i in input_str:
        position += 1
        if i == "(":
            floor += 1
        elif i == ")":
            floor -= 1
        if floor == -1:
            break
    # print(position)
    return position


if __name__ == "__main__":
    print("######################")
    print("####  TEST ALGO   ####")
    ok = "ok" if c2015d1p1() == 3 else "ko"
    print(f"##  c2015d1p1 => {ok}  #")
    ok = "ok" if c2015d1p2() == 1 else "ko"
    print(f"##  c2015d1p2 => {ok}  #")
    print("######################")
    print("# WITH PUZZLE INPUT  #")
    with open('2015/data/d1.txt', 'r') as file:
        input_data: str = file.read()
        print(f"# c2015d1p1 => {c2015d1p1(input_data)} #")
        print(f"# c2015d1p2 => {c2015d1p2(input_data)} #")
    print("######################")
