import random
from tqdm import tqdm

match = {
    'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K',
    'l': 'L',
    'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W',
    'x': 'X',
    'y': 'Y', 'z': 'Z', '@': '@', '_': '_', '.': 'dot', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F',
    'G': 'G',
    'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R',
    'S': 'S',
    'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z', '0': '0', '1': '1', '2': '2', '3': '3',
    '4': '4',
    '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'
}


class RandEmail(object):
    def __init__(self, suffix_path=None):
        if suffix_path is None:
            print("missing email suffix!")
        else:
            with open(suffix_path, encoding='utf-8') as suffix_f:
                email_suffix = suffix_f.read()
                self.suffix = email_suffix.split()

    def __call__(self, amount=0, *args, **kwargs):
        words = []
        print("generate email:")
        for i in tqdm(range(amount), ncols=100):
            word = []
            length = random.randint(4, 18)
            suffix_len = len(self.suffix)
            email_index = random.randint(0, suffix_len - 1)
            # print(length)
            # print(i)
            for j in range(length):  ### @之前部分
                key = random.sample(match.keys(), 1)
                if key[0] != '@':
                    if j == 0:
                        if key[0] != '_' and key[0] != '.':
                            word.append(key[0])
                        else:
                            j -= 1
                    else:
                        word.append(key[0])
                else:
                    j -= 1
            for k in self.suffix[email_index]:  ### @之后部分
                word.append(k)
            words.append("".join(word))
        print("finish!")
        return words
