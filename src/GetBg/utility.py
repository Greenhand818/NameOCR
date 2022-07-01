import argparse


def init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--source", type=str, default="./source", help="source business card path")
    parser.add_argument("--result", type=str, default="./result", help="result background path")

    return parser


def parse_args():
    parser = init_args()
    return parser.parse_args()


if __name__ == '__main__':
    pass
