from collections import defaultdict


class KB:
    def __init__(self):
        self.sentences = []
        self.pred_to_sentence = defaultdict(set)
        self.consts = set()
        self.vars = set()

    def tell(self, sentence):
        self.sentences.append(sentence)
        for pred_name in sentence.predicate_name_map:
            self.pred_to_sentence[pred_name].add(sentence)

    def _debug_print_kb(self):
        print("Sentences: {}\nConstants: {}\n Variables: {}".format(
            list(map(lambda x: x.raw_sentence, self.sentences)),
            self.consts, self.vars))
