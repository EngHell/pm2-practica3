from predicates import PredicateType, predicate_g_is_dot, predicate_generator_is_specific_character, \
    predicate_is_number


def cond(predicate: PredicateType):
    def guess(value):
        should = predicate(value) if hasattr(predicate, '__call__') else predicate
        if should:
            return value, True
        return value, False

    return guess


def cond_g_is_dot():
    return cond(predicate_g_is_dot())


def cond_is_specific_character(char: str):
    return cond(predicate_generator_is_specific_character(char))


def cond_g_is_digit():
    return cond(predicate_is_number)


def cond_any():
    return cond(lambda value: True)
