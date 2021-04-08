from sentence import Sentence


class KB:
    def __init__(self):
        self.sentences = []
        self.consts = set()
        self.vars = set()

    def tell(self, sentence):
        sentence = Sentence(sentence)
        self.sentences.append(sentence)
        self.vars |= sentence.get_vars()
        self.consts |= sentence.get_consts()

    def ask(self, query):
        raise NotImplementedError("Ask method in KB not yet implemented!")

    def _debug_print_kb(self):
        print("Sentences: {}\nConstants: {}\n Variables: {}".format(
            self.sentences, self.consts, self.vars))
