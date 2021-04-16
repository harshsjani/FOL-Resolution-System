import unittest
from kb import KB
import sentence


class LogicTest(unittest.TestCase):
    def __init__(self):
        self.kb = KB()

    def testSentence(self):
        expr1 = "Start(x) & Healthy(x) => Ready(x)"
        sentence1 = sentence.Sentence(expr1)
        print(sentence1.predicates)

    def testMultiply(self):
        self.assertEqual((0 * 10), 0)
        self.assertEqual((5 * 8), 40)


if __name__ == '__main__':
    unittest.main()
