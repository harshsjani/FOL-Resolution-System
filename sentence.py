from constants import Consts
from predicate import Predicate


class Sentence:
    # Quite literally a bunch of predicates joined together by ORs
    def __init__(self, sentence):
        self.predicate_names = set()
        self.ordered_predicates = []
        self.vars = set()
        self.ordered_vars = []
        self.consts = set()
        self.ordered_consts = []
        self.raw_sentence = sentence
        self.__parse_sentence__()

    def __parse_sentence__(self):
        sentence = self.raw_sentence

        if Consts.AND not in sentence:
            pred = Predicate(sentence)
            self.predicate_names.add(pred.name)
            self.vars |= pred.get_vars()
            self.consts |= pred.get_consts()
        else:
            # Vaccinated(x) ^ Person(x) => Safe(x)
            # ~Vaccinated(x) v ~Person(x) v ~ Safe(x)
            sentence = sentence.replace(Consts.IMPLIES, Consts.IMPLIES_REPL)

            for predicate in sentence.split(Consts.AND):
                # ~Vaccinated(x)
                pred = Predicate(predicate)
                self.predicate_names.add(pred.name)
                self.ordered_predicates.append(pred)
                self.vars |= pred.get_vars()
                self.consts |= pred.get_consts()

    def get_vars(self):
        return self.vars

    def get_consts(self):
        return self.consts
