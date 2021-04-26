from logic import Logic
from copy import deepcopy


class KB:
    def __init__(self):
        self.sentences = []
        self.consts = set()
        self.vars = set()

    def tell(self, sentence):
        self.sentences.append(sentence)

    def ask(self, KB, query):
        ret = Logic.resolution(KB, query, False)

        if ret is False:
            kb2 = deepcopy(KB)
            for sent in kb2.sentences:
                Logic.factor_sentence(sent)
            ret = Logic.resolution(kb2, query, True)
        return ret
        # return Logic.linear_resolution(KB, query)
        # return Logic.sos_resolution(KB, query)

    def _debug_print_kb(self):
        print("Sentences: {}\nConstants: {}\n Variables: {}".format(
            list(map(lambda x: x.raw_sentence, self.sentences)),
            self.consts, self.vars))
