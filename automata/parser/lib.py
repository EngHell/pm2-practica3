from typing import Callable
from automata.dfa.automata import state0, transition, get_accept_test, accepts, check_accepted_type, compute
from automata.parser.words import math_words


class StringStream:
    def __init__(self, to_parse: str):
        self.to_parse = to_parse
        self.index: int = -1

    def __len__(self):
        return len(self.to_parse)

    def next(self):
        self.index += 1
        return self.to_parse[self.index]

    def peek(self, n: int = None):
        k = self.index + 1

        if n is not None:
            k = n

        return self.to_parse[k]


class Parser:
    parsed: str = ''
    relevant: [str] = []

    def __init__(self, stream: StringStream, words: [str]):
        self.stream = stream
        self.words = words
        self.relevant = []
        self.remainder = ''

    def has_ended(self):
        return self.stream.index >= (len(self.stream)-1)

    def parse(self):
        if self.has_ended():
            return

        c = self.stream.peek()
        if c.isspace():
            self.parsed += self.stream.next()
            self.parse()
        else:
            self.parse_word()

    def parse_word(self):
        if self.has_ended():
            return

        word: str = ''
        left: Callable = state0

        while not self.has_ended() and not self.stream.peek().isspace():
            right = self.stream.next()
            word += right

        word = self.process_word(word, '')

        self.parsed += word

        self.parse()

    def process_word(self, word, remainder):
        self.remainder = remainder + self.remainder
        left = compute(word)
        is_matched = get_accept_test(accepts)(left)

        if is_matched:
            temp = self.remainder
            self.remainder = ''
            word = self.add_tag_to_word(word, left) + self.process_word(temp, '')
        else:
            if len(word) > 1:
                cut = len(word) - 1
                word = self.process_word(word[:cut], word[cut])
            else:
                temp = self.remainder
                self.remainder = ''
                if not temp == '':
                    word = word + self.process_word(temp, '')

        return word

    def add_tag_to_word(self, word, left):
        t = check_accepted_type(accepts)(left)
        if t == "palabra":
            if word in self.words:
                if word not in self.relevant:
                    self.relevant.append(word)
                word = f'<span class="grammar-{t}" data-img="{t}">{word}</span>'
        else:
            word = f'<span class="grammar-{t}">{word}</span>'

        return word
