from copy import deepcopy
from sentence import Sentence
from constants import Consts


class Logic:
    """
    Takes in two sentences and returns a unifier for them if one exists.
    """
    @staticmethod
    def can_unify(pred1, pred2):
        if pred1.name != pred2.name:
            return False

        args1 = pred1.ordered_args
        args2 = pred2.ordered_args
        var_mapping = {}

        if len(args1) != len(args2):
            return False

        if args1 == args2:
            return True

        for i in range(len(args1)):
            arg1 = args1[i]
            arg2 = args2[i]

            if arg1[0].isupper() and arg2[0].isupper() and arg1 != arg2:
                return False

            if arg1.islower():
                if arg1 in var_mapping and arg2 != var_mapping[arg1]:
                    return False
                var_mapping[arg1] = arg2
            elif arg2.islower():
                if arg2 in var_mapping and arg1 != var_mapping[arg2]:
                    return False
                var_mapping[arg2] = arg1
        return True

    @staticmethod
    def unify_predicates(pred1, pred2):
        # Sub for pred1
        args1 = pred1.ordered_args
        args2 = pred2.ordered_args
        subst1 = []
        subst2 = []
        var_mapping = {}

        if len(args1) != len(args2):
            return None

        for i in range(len(args1)):
            arg1 = args1[i]
            arg2 = args2[i]

            if arg1[0].isupper() and arg2[0].isupper() and arg1 != arg2:
                return None

            if arg1.islower():
                if arg1 in var_mapping and arg2 != var_mapping[arg1]:
                    return None
                var_mapping[arg1] = arg2
                subst1.append((arg1, arg2))
            elif arg2.islower():
                if arg2 in var_mapping and arg1 != var_mapping[arg2]:
                    return None
                var_mapping[arg2] = arg1
                subst2.append((arg2, arg1))

        return var_mapping

    @staticmethod
    def is_contradiction(sentence1, sentence2):
        pred1 = sentence1.ordered_predicates[0]
        pred2 = sentence2.ordered_predicates[0]

        if len(sentence1.ordered_predicates) != 1:
            return False
        if len(sentence2.ordered_predicates) != 1:
            return False
        if not (pred1.negated ^ pred2.negated):
            return False
        if pred1.name != pred2.name:
            return False
        if pred1.ordered_args != pred2.ordered_args:
            return False
        return True

    @staticmethod
    def resolve(sentence1, sentence2):
        new_sentences = []

        # sentence 2 is always the single predicate sentence
        if len(sentence2.ordered_predicates) > len(sentence1.ordered_predicates):
            sentence1, sentence2 = sentence2, sentence1

        for pred1 in sentence1.ordered_predicates:
            for pred2 in sentence2.ordered_predicates:
                if pred1.name == pred2.name and (pred1.negated ^ pred2.negated):
                    # None or mapping {x: Dan, y: Bella}
                    # {x: y, z: Shawn}
                    if not Logic.can_unify(pred1, pred2):
                        continue
                    
                    substs = Logic.unify_predicates(pred1, pred2)

                    new_sent = []

                    for pred in sentence1.ordered_predicates:
                        if pred == pred1:
                            continue
                        new_pred = deepcopy(pred)
                        new_pred.subst(substs)
                        new_sent.append(new_pred)

                    if not new_sent:
                        new_sentences.append(False)
                    else:
                        new_sentences.append(Sentence(new_sent))

        return new_sentences

    @staticmethod
    def resolution(KB, alpha):
        sentences = deepcopy(KB.sentences) + [Sentence(Consts.NOT + alpha)]

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
