import sys

from twcontroller import TWController


def main():
    twc = TWController(sys.argv[1])
    twc.run()


if __name__ == '__main__':
    main()
