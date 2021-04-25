from constants import Consts
from predicate import Predicate


class Sentence:
    # Quite literally a bunch of predicates joined together by ORs
    def __init__(self, sentence):
        self.predicate_name_map = dict()
        self.ordered_predicates = []
        self.vars = dict()
        self.ordered_vars = []
        self.consts = dict()
        self.ordered_consts = []

        if isinstance(sentence, str):
            self.raw_sentence = sentence
            self.__parse_str_sentence__()
        else:
            self.__parse_pred_list__(sentence)

    def __parse_str_sentence__(self):
        sentence = self.raw_sentence

        if Consts.AND not in sentence and Consts.OR not in sentence and Consts.IMPLIES not in sentence:
            pred = Predicate(sentence)
            self.predicate_name_map[pred.name] = pred
            self.ordered_predicates.append(pred)
            # self.vars |= pred.get_vars()
            # self.consts |= pred.get_consts()
        else:
            # Vaccinated(x) ^ Person(x) => Safe(x)
            # ~Vaccinated(x) v ~Person(x) v ~ Safe(x)
            sentence = sentence.replace(Consts.IMPLIES, Consts.IMPLIES_REPL)

            splitter = Consts.AND if Consts.AND in sentence else Consts.OR

            for predicate in sentence.split(splitter):
                # ~Vaccinated(x)
                if splitter == Consts.AND:
                    predicate = Consts.NOT + predicate
                pred = Predicate(predicate)
                self.predicate_name_map[pred.name] = pred
                self.ordered_predicates.append(pred)
                # self.vars |= pred.get_vars()
                # self.consts |= pred.get_consts()

    def __parse_pred_list__(self, pred_list):
        for pred in pred_list:
            self.predicate_name_map[pred.name] = pred
            self.ordered_predicates.append(pred)
            # self.vars |= pred.get_vars()
            # self.consts |= pred.get_consts()

    def __str__(self):
        return " | ".join(map(str, self.ordered_predicates))

    def get_vars(self):
        return self.vars

    def get_consts(self):
        return self.consts
