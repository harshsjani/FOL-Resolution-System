from sentence import Sentence
from logic import Logic


class KB:
    def __init__(self):
        self.sentences = []
        self.consts = set()
        self.vars = set()

    def tell(self, sentence):
        sentence = Sentence(sentence)
        self.sentences.append(sentence)
        # self.vars |= sentence.get_vars()
        # self.consts |= sentence.get_consts()

    def ask(self, KB, query):
        return Logic.resolution(KB, query)

    def _debug_print_kb(self):
        print("Sentences: {}\nConstants: {}\n Variables: {}".format(
            list(map(lambda x: x.raw_sentence, self.sentences)),
            self.consts, self.vars))
