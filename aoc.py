import datetime
import os
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description='Script to run Advent of Code')
    # Required arguments
    parser.add_argument('-y', '--year', dest='year', required=False, default=datetime.date.today().year)
    parser.add_argument('-d', '--day', dest='day', required=True)
    options, args = parser.parse_known_args()

    try:
        day = getattr(__import__(f"src.{options.year}.d{options.day}", fromlist=["Day"]), "Day")
        day(options.year, options.day).do()
    except ModuleNotFoundError as e:
        print(e)
        print(f"Challenge of day {options.day} year {options.year} not found.")
        print("Create ? y/n")
        create = input() == 'y'
        if create:
            base_name = f".{os.sep}src{os.sep}{options.year}{os.sep}"
            dirname = os.path.dirname(f"{base_name}{os.sep}data")
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            open(f"{base_name}data{os.sep}d{options.day}.txt", "x").close()
            with open(f"{base_name}d{options.day}.py", "w") as file:
                file.write('''""""""
from ..day import DayBase

example = """"""


class Day(DayBase):
    def do(self):
        self.test(None, None, example)
        self.run(None, None)

    @staticmethod
    def part1(data=example):
        pass

    @staticmethod
    def part2(data=example):
        pass
        ''')
                file.close()
