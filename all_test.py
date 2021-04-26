from sentence import Sentence
from logic import Logic


def test_one():
    print("5")


def testSentence():
    expr1 = "Start(x) & Healthy(x) => Ready(x)"
    _ = Sentence(expr1)


def testMultiply():
    assert (0 * 10) == 0
    assert (5 * 8) == 40


def test_merge():
    sent1 = Sentence("P(x) | P(x) | ~P(y) | ~P(y) | T(x) | ~P(y) | \
                    T(x) | ~T(x) | P(y) | P(Bob)")
    Logic.merge_sentence(sent1)
    assert(str(sent1)) == "P(x) | ~P(y) | T(x) | ~T(x) | P(Bob)"


def test_factoring():
    sent1 = Sentence("P(x) | P(y)")
    Logic.factor_sentence(sent1)
    assert(str(sent1)) == "P(y)"

    sent1 = Sentence("P(x,a) | P(b,y)")
    Logic.factor_sentence(sent1)
    assert(str(sent1)) == "P(b,y)"

    sent1 = Sentence("P(x) | P(a)")
    Logic.factor_sentence(sent1)
    assert(str(sent1)) == "P(a)"

    sent1 = Sentence("P(a,b) | P(a,b)")
    Logic.factor_sentence(sent1)
    assert(str(sent1)) == "P(a,b)"

    sent1 = Sentence("P(x,x) | P(a,y)")
    Logic.factor_sentence(sent1)
    assert(str(sent1)) == "P(y,y)"

    sent1 = Sentence("P(x,y) | P(x,x) | P(y,z)")
    Logic.factor_sentence(sent1)
    assert(str(sent1)) == "P(z,z)"

    sent1 = Sentence("~wise(x) | ~wise(y) | taller(x,y) | ~wise(p)")
    Logic.factor_sentence(sent1)
    assert(str(sent1)) == "~wise(p) | taller(p,p)"


def test_taut():
    sent1 = Sentence("P(x) | P(y)")
    bool = Logic.is_tautology(sent1)
    assert(bool) is False

    sent1 = Sentence("P(x) | Q(y) | ~Q(y) | R(z)")
    bool = Logic.is_tautology(sent1)
    assert(bool) is True

    sent1 = Sentence("~P(x) | P(y)")
    bool = Logic.is_tautology(sent1)
    assert(bool) is False
