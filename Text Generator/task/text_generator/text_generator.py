from nltk.tokenize import WhitespaceTokenizer
from collections import Counter, defaultdict
from random import choices, choice


class TextGenerator:
    def __init__(self):
        filename = input()
        with open(filename) as f:
            self.corpus = f.read()
        self.tokens = []
        self.token_freq = {}
        self.unique_tokens = set()
        self.unique_bigrams = set()
        self.unique_capitalized_tokens = []
        self.unique_capitalized_bigrams = []
        self.bigrams = []
        self.trigrams = []
        self.tokenize()
        self.bigramize()
        self.trigramize()
        self.model_dict = {}
        self.model()
        self.first_word = ''

    def tokenize(self):
        # wst = WhitespaceTokenizer()
        # self.tokens = wst.tokenize(self.corpus)
        self.tokens = self.corpus.split()
        self.unique_tokens = set(self.tokens)
        self.unique_capitalized_tokens = \
            [word for word in self.unique_tokens if word[0].isupper() and word[-1] not in '?.!']
        self.token_freq = Counter(self.tokens)
        # print('Corpus statistics')
        # print(f'All tokens: {len(self.tokens)}')
        # print(f'Unique tokens: {len(self.unique_tokens)}')

    def bigramize(self):
        self.bigrams = [bg for bg in zip(self.tokens[:-1], self.tokens[1:])]
        self.unique_bigrams = set(self.bigrams)
        self.unique_capitalized_bigrams = \
            [bg for bg in self.unique_bigrams if bg[0][0].isupper() and bg[0][-1] not in '?.!']
        # print(f'Number of bigrams: {len(self.bigrams)}')

    def trigramize(self):
        self.trigrams = [tg for tg in zip(self.bigrams[:-1], self.tokens[2:])]
        # print(self.trigrams[0])

    def show_bigrams(self):
        while True:
            user_input = input()
            if user_input == 'exit':
                exit()
            else:
                try:
                    i = int(user_input)
                    if -len(self.bigrams) - 1 < i < len(self.bigrams):
                        print(f'Head: {self.bigrams[i][0]} Tail: {self.bigrams[i][1]}')
                    else:
                        print('Index Error. Please input a value that is not greater than the number of all bigrams.')
                except ValueError:
                    print('Type Error. Please input an integer.')

    def show_token(self):
        while True:
            user_input = input()
            if user_input == 'exit':
                exit()
            else:
                try:
                    i = int(user_input)
                    if -len(self.tokens) - 1 < i < len(self.tokens):
                        print(self.tokens[i])
                    else:
                        print('Index Error. Please input an integer that is in the range of the corpus.')
                except ValueError:
                    print('Type Error. Please input an integer.')

    def model(self):
        self.model_dict = defaultdict(Counter)
        for (h, t) in self.trigrams:
        # for (h, t) in self.bigrams:
            self.model_dict[h][t] += 1

    def show_model(self):
        while True:
            user_input = input()
            if user_input == 'exit':
                exit()
            else:
                key = user_input
                print(f'Head: {key}')
                if key in self.model_dict:
                    for tail, count in self.model_dict[key].most_common():
                        print(f'Tail: {tail}      Count: {count}')
                else:
                    print('Key Error. The requested word is not in the model. Please input another word.')

    def generate(self):
        if not self.first_word:
            # start_word = choices(self.token_freq.keys(), self.token_freq.values())
            # start_word = choice(self.tokens)
            # start_word = choice(self.unique_capitalized_tokens)
            start_bigram = choice(self.unique_capitalized_bigrams)
        else:
            start_word = self.first_word

        sentence = [*start_bigram]
        while True:
            # next_word = self.model_dict[start_word].most_common(1)[0][0]
            # print(start_bigram, self.model_dict[start_bigram])
            # print('Most common', self.model_dict[start_bigram].most_common(1))
            next_word = self.model_dict[start_bigram].most_common(1)[0][0]
            sentence.append(next_word)
            if len(sentence) > 4 and next_word[-1] in '?.!':
                break
            start_bigram = (start_bigram[-1], next_word)

        return ' '.join(sentence)
        # self.first_word = next_word






if __name__ == '__main__':
    tkn = TextGenerator()
    i = 0
    while i < 10:
        sentence = tkn.generate()
        if sentence:
            print(sentence)
            i += 1
