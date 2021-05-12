from typing import Callable
from automata.dfa.automata import state0, transition, get_accept_test, accepts, check_accepted_type
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

    def __init__(self, stream: StringStream):
        self.stream = stream

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
            left = transition(left, right)

        is_matched = get_accept_test(accepts)(left)

        if is_matched:
            t = check_accepted_type(accepts)(left)
            if t == "palabra":
                if word in math_words:
                    word = f'<span class="grammar-{t}" data-img="{t}">{word}</span>'
            else:
                word = f'<span class="grammar-{t}">{word}</span>'

        self.parsed += word

        self.parse()
