from copy import deepcopy
from collections import defaultdict
from sentence import Sentence
from predicate import Predicate
from constants import Consts
from itertools import combinations


class Logic:
    @staticmethod
    def merge_sentence(sentence):
        drop_counter = defaultdict(list)
        for name, pred_list in sentence.predicate_name_map.items():
            if len(pred_list) > 1:
                for pred1, pred2 in combinations(pred_list, 2):
                    if Predicate.are_equal(pred1, pred2):
                        if pred1 not in drop_counter[name]:
                            drop_counter[name].append(pred1)
                        elif pred2 not in drop_counter[name]:
                            drop_counter[name].append(pred2)
        for key, drop_list in drop_counter.items():
            lst = sentence.predicate_name_map[key]

            for item in drop_list:
                if len(lst) == 1:
                    break
                lst.remove(item)
        new_preds = []
        for k, lst in sentence.predicate_name_map.items():
            new_preds.extend(lst)
        if new_preds:
            sentence.ord_preds = new_preds

    @staticmethod
    def factor_sentence(sentence):
        can_factor = False
        preds_to_factor = None

        for name, pred_list in sentence.predicate_name_map.items():
            if len(pred_list) > 1:
                can_factor = True
                preds_to_factor = pred_list
                break

        if not can_factor:
            return

        for pred1, pred2 in combinations(preds_to_factor, 2):
            if pred1.negated ^ pred2.negated:
                continue
            subs = Logic.unify(pred1, pred2)

            if subs is not None:
                for pred in sentence.ord_preds:
                    pred.subst(subs)
        Logic.merge_sentence(sentence)
        sentence.ord_preds.sort(key=lambda x: x.name)

    @staticmethod
    def is_variable(var):
        return isinstance(var, str) and var[0].islower()

    @staticmethod
    def cyclic_vars(var1, var2, mapping):
        if var1 == var2:
            return True
        elif Logic.is_variable(var2) and var1 in mapping:
            return Logic.cyclic_vars(var1, mapping[var2], mapping)
        else:
            return False

    @staticmethod
    def unify_variable(var1, var2, mapping):
        if var1 in mapping:
            return Logic.unify(mapping[var1], var2, mapping)
        elif var2 in mapping:
            return Logic.unify(var1, mapping[var2], mapping)
        elif Logic.cyclic_vars(var1, var2, mapping):
            return None
        else:
            temp_mapping = mapping.copy()
            temp_mapping[var1] = var2
            return temp_mapping

    @staticmethod
    def unify(args1, args2, mapping=dict()):
        if mapping is None:
            return None
        elif args1 == args2:
            return mapping
        elif isinstance(args1, Predicate) and isinstance(args2, Predicate):
            return Logic.unify(args1.ordered_args, args2.ordered_args)
        elif Logic.is_variable(args1):
            return Logic.unify_variable(args1, args2, mapping)
        elif Logic.is_variable(args2):
            return Logic.unify_variable(args2, args1, mapping)
        elif isinstance(args1, list) and \
                isinstance(args2, list) and len(args1) == len(args2):
            if not args1:
                return mapping
            return Logic.unify(args1[1:], args2[1:],
                               Logic.unify(args1[0], args2[0], mapping))
        return None

    @staticmethod
    def resolve(sentence1, sentence2):
        new_sentences = []

        s1_preds = sentence1.ord_preds
        s2_preds = sentence2.ord_preds

        # sentence 2 is always the single predicate sentence
        if len(s2_preds) > len(s1_preds):
            sentence1, sentence2 = sentence2, sentence1

        for pred1 in s1_preds:
            for pred2 in s2_preds:
                if pred1.name == pred2.name and \
                        (pred1.negated ^ pred2.negated):
                    # None or mapping {x: Dan, y: Bella}
                    # {x: y, z: Shawn}

                    substs = Logic.unify(pred1, pred2)

                    if substs is None:
                        continue

                    new_sent = []

                    for pred in s1_preds:
                        if pred == pred1:
                            continue
                        new_pred = deepcopy(pred)
                        new_pred.subst(substs)
                        new_sent.append(new_pred)

                    for pred in s2_preds:
                        if pred == pred2:
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
                if len(s1.ord_preds) > 15 and \
                        len(s2.ord_preds) > 15:
                    continue
                resolvents = Logic.resolve(s1, s2)

                if False in resolvents:
                    return True

                usable_resolvents = []
                for resolvent in resolvents:
                    Logic.factor_sentence(resolvent)

                    rlen = len(resolvent.ord_preds)
                    if rlen <= len(s1.ord_preds) or rlen <= len(s2.ord_preds):
                        usable_resolvents.append(resolvent)

                for item in usable_resolvents:
                    print(item)
                new = new.union(set([str(r) for r in usable_resolvents]))

            if new.issubset(sentence_set):
                return False

            for new_sentence in new:
                if new_sentence not in sentence_set:
                    sentences.append(Sentence(new_sentence))
                    sentence_set.add(new_sentence)
