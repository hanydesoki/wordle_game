import string

LETTERS = list(string.ascii_uppercase)

def load_words():

    result = {}

    for i in range(4, 12):

        with open(f'Words/francais_{i}.txt', 'r') as f:
            l1 = f.readlines()

        words = [w.replace('\n', '').upper() for w in l1]

        with open(f'Words/francais_common_{i}.txt', 'r') as f:
            l2 = f.readlines()

        common_words = [w.replace('\n', '').upper() for w in l2]

        result[i] = {'all_words': words, 'common_words': common_words}

    return result

def init_carac_count():
    return {c: 0 for c in LETTERS}


def get_carac_count(word, word_to_guess):
    carac_count = init_carac_count()

    for c1, c2 in zip(word, word_to_guess):
        if c1 != c2:
            carac_count[c2] += 1

    return carac_count