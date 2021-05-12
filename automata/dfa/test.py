import sys

from .automata import compute, get_accept_test, check_accepted_type, accepts


def main():
    if len(sys.argv) < 2:
        print('usage: state.py ("sometex to test"|sometext!23)')
    if len(sys.argv) > 1:
        for word in sys.argv[1:]:
            print('string is: ' + word)
            matched = compute(word)
            valid = get_accept_test(accepts)(matched)
            t = check_accepted_type(accepts)(matched)
            print(f"Did match: {valid} type matched: {t}")


if __name__ == '__main__':
    main()