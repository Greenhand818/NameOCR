import random
from tqdm import tqdm


class RandName(object):
    def __init__(self, last_name_path=None, first_name_path=None):
        if last_name_path is None:
            print("missing last name!")
        elif first_name_path is None:
            print("missing first name!")
        else:
            with open(last_name_path, encoding='utf-8') as name_f:
                last_names = name_f.read()
                self.last_name = last_names.split()
            with open(first_name_path, encoding='utf-8') as name_f:
                first_names = name_f.read()
                self.first_name = first_names.split()

    def __call__(self, amount=0, en=False, *args, **kwargs):
        words = []
        if en:
            print("generate English name:")
        else:
            print("generate Chinese name:")
        for i in tqdm(range(amount), ncols=100):
            word = []
            last_name_len = len(self.last_name)
            first_name_len = len(self.first_name)
            last_name_index = random.randint(0, last_name_len - 1)
            first_name_index = random.randint(0, first_name_len - 1)
            if en is False:
                word.append(self.last_name[last_name_index])                    ### last_name
                word.append(self.first_name[first_name_index])                  ### first_name
                words.append("".join(word))
            else:
                word.append(self.last_name[last_name_index].capitalize())       ### last_name
                word.append(self.first_name[first_name_index].capitalize())     ### first_name
                words.append(" ".join(word))
        print("finish!")
        return words
