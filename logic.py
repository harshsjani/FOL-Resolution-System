from copy import deepcopy
from sentence import Sentence
from constants import Consts


class Logic:
    """
    Takes in two sentences and returns a unifier for them if one exists.
    """
    @staticmethod
    def unify(x, y, substs=dict()):
        if x.ordered_predicates != y.ordered_predicates:
            return None

    @staticmethod
    def unify_predicates(pred1, pred2):
        # Plays(x, John), ~Plays(Ralph, y)
        # {x/Ralph, y/John}
        # [sent1: [(x, Ralph)], sent2: [(y, John)]]
        args1 = pred1.ordered_args
        args2 = pred2.ordered_args
        subst1 = []
        subst2 = []

        if len(args1) != len(args2):
            return None

        for i in range(len(args1)):
            arg1 = args1[i]
            arg2 = args2[i]

            if arg1[0].isupper() and arg2[0].isupper() and arg1 != arg2:
                return None

            if arg1.islower() and arg2.islower():
                return None

            if arg1.islower():
                subst1.append((arg1, arg2))
            else:
                subst2.append((arg2, arg1))

        return [subst1, subst2]

    @staticmethod
    def resolve(sentence1, sentence2):
        new_sentences = []

        for pred1 in sentence1.ordered_predicates:
            for pred2 in sentence2.ordered_predicates:
                if pred1.name == pred2.name and (pred1.negated ^ pred2.negated):
                    substs = Logic.unify_predicates(pred1, pred2)

                    if substs is not None:
                        new_sent = []

                        if substs[0]:
                            for pred in sentence1.ordered_predicates:
                                if pred == pred1:
                                    continue
                                new_pred = deepcopy(pred)
                                new_pred.subst(substs[0])
                                new_sent.append(new_pred)
                        else:
                            for pred in sentence1.ordered_predicates:
                                if pred == pred1:
                                    continue
                                new_pred = deepcopy(pred)
                                new_sent.append(new_pred)
                        if substs[1]:
                            for pred in sentence2.ordered_predicates:
                                if pred == pred2:
                                    continue
                                new_pred = deepcopy(pred)
                                new_pred.subst(substs[1])
                                new_sent.append(new_pred)
                        else:
                            for pred in sentence2.ordered_predicates:
                                if pred == pred2:
                                    continue
                                new_pred = deepcopy(pred)
                                new_sent.append(new_pred)
                        if not new_sent:
                            new_sentences.append(False)
                        else:
                            new_sentences.append(Sentence(new_sent))
        return new_sentences

    @staticmethod
    def resolution(KB, alpha):
        sentences = KB.sentences + [Sentence(Consts.NOT + alpha)]

        sentence_set = set([str(x) for x in sentences])
        new = set()

        while True:
            N = len(sentences)

            pairs = [(sentences[i], sentences[j])
                     for i in range(N - 1) for j in range(i + 1, N)]

            for s1, s2 in pairs:
                if len(s1.ordered_predicates) > 1 and len(s2.ordered_predicates) > 1:
                    continue
                resolvents = Logic.resolve(s1, s2)
                # for item in resolvents:
                #     print(item)

                if False in resolvents:
                    return True
                new = new.union(set([str(r) for r in resolvents]))

            if new.issubset(sentence_set):
                return False

            for new_sentence in new:
                if new_sentence not in sentence_set:
                    sentences.append(Sentence(new_sentence))
                    sentence_set.add(new_sentence)
