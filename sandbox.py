from logic import Logic
from sentence import Sentence


def f(x):
    return x.ordered_predicates[0].ordered_args


def test_merge():
    sent1 = Sentence("P(x) | P(x) | ~P(y) | ~P(y) | T(x) | ~P(y) | \
        T(x) | ~T(x) | P(y) | P(Bob)")
    Logic.merge_sentence(sent1)
    print(sent1)


def test_factoring():
    sent1 = Sentence("P(x) | P(y)")
    Logic.factor_sentence(sent1)
    print(sent1)


test_factoring()
