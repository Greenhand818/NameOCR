import argparse


def init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--bg_path", type=str, default="./background")
    parser.add_argument("--target_path", type=str, default="./data_pic")
    parser.add_argument("--ttf_path", type=str, default="./ttf")
    parser.add_argument("--email_suffix", type=str, default="./email_suffix.txt")
    parser.add_argument("--domain_path", type=str, default="./domains.txt")
    parser.add_argument("--ch_last_name_path", type=str, default="./ch_last_name.txt")
    parser.add_argument("--ch_first_name_path", type=str, default="./ch_first_name.txt")
    parser.add_argument("--en_first_name_path", type=str, default="./en_first_name.txt")
    parser.add_argument("--en_last_name_path", type=str, default="./en_last_name.txt")
    parser.add_argument("-n", "--amount", type=int, default=1000)
    parser.add_argument("-d", "--database", type=bool, default=True)
    return parser


def parse_args():
    parser = init_args()
    return parser.parse_args()


if __name__ == '__main__':
    pass
