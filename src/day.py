import os


class DayBase:
    def __init__(self, year, day):
        self.year = year
        self.day = day
        # file_path = __file__.split(os.sep)
        # self.year = file_path[-2]
        # file_path = file_path[-1]
        # self.day = file_path.split('.')[0]

    @staticmethod
    def part1(data=None):
        return 0

    @staticmethod
    def part2(data=None):
        return 0

    def test(self, res_part1, res_part2, input_data1=None, input_data2=None):
        print("########################")
        print("####    TEST ALGO   ####")
        self.write(1, input_data1, res_part1)
        self.write(2, input_data1 if input_data2 is None else input_data2, res_part2)

    def run(self, part1=None, part2=None):
        print("########################")
        print("#   WITH PUZZLE INPUT  #")
        with open(f'.{os.sep}src{os.sep}{self.year}{os.sep}data{os.sep}d{self.day}.txt', 'r') as file:
            input_data: str = file.read()
            self.write(1, input_data, part1)
            self.write(2, input_data, part2)
        print("########################")

    def write(self, part, data, expectation):
        response = self.part1(data) if part == 1 else self.part2(data)
        ok = " ok" if (expectation is not None and response == expectation) else f" ko, expected {expectation} got"
        print(f"# c{self.year}d{self.day}p{part} =>{ok} {response} #")

    def do(self):
        print(f"Challenge of day {self.day} year {self.year} not ready")
