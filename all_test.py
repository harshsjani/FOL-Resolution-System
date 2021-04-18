import sentence


def test_one():
    print("5")


def testSentence():
    expr1 = "Start(x) & Healthy(x) => Ready(x)"
    _ = sentence.Sentence(expr1)


def testMultiply():
    assert (0 * 10) == 0
    assert (5 * 8) == 40
