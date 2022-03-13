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