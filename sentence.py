from constants import Consts
from predicate import Predicate
from collections import defaultdict


class Sentence:
    # Quite literally a bunch of predicates joined together by ORs
    def __init__(self, sentence):
        self.predicate_name_map = defaultdict(list)
        self.ord_preds = []

        if isinstance(sentence, str):
            self.raw_sentence = sentence
            self.__parse_str_sentence__()
        else:
            self.__parse_pred_list__(sentence)

    def __parse_str_sentence__(self):
        sentence = self.raw_sentence

        if Consts.AND not in sentence and Consts.IMPLIES not in sentence:
            pred = Predicate(sentence)
            self.predicate_name_map[pred.name].append(pred)
            self.ord_preds.append(pred)
        else:
            sentence = sentence.replace(Consts.IMPLIES, Consts.AND)

            splitter = Consts.AND
            splt = sentence.split(splitter)

            for idx, predicate in enumerate(splt):
                predicate = predicate.strip()
                if idx != len(splt) - 1:
                    if predicate[0] != Consts.NOT:
                        predicate = Consts.NOT + predicate.strip()
                    else:
                        predicate = predicate[1:]
                pred = Predicate(predicate)
                self.predicate_name_map[pred.name].append(pred)
                self.ord_preds.append(pred)

    def __parse_pred_list__(self, pred_list):
        for pred in pred_list:
            self.predicate_name_map[pred.name].append(pred)
            self.ord_preds.append(pred)

    def __str__(self):
        return " | ".join(map(str, self.ord_preds))

    def __eq__(self, other):
        return self.__str__() == str(other)

    def __hash__(self):
        return hash(self.__str__())

    def __len__(self):
        return len(self.ord_preds)
