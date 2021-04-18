from constants import Consts
from sentence import Sentence


class Logic:
    """
    Takes in two sentences and returns a unifier for them if one exists.
    """
    @staticmethod
    def unify(x, y, substs=dict()):
        if x.ordered_predicates != y.ordered_predicates:
            return None

    @staticmethod
    def resolve(sentence1, sentence2):
        pass

    @staticmethod
    def resolution(KB, alpha):
        sentences = KB.sentences + Sentence(Consts.NOT + alpha)

        sentence_set = set(sentences)
        new = set()

        while True:
            N = len(sentences)

            pairs = [(sentences[i], sentences[j]
                        for i in range(N - 1) for j in range(i + 1, N)]

            for s1, s2 in pairs:
                resolvents = resolve(s1, s2)

                if False in resolvents:
                    return True
                new = new.union(set(resolvents))

            if new.issubset(sentence_set):
                return False

            for new_sentence in new:
                if new_sentence not in sentence_set:
                    sentences.append(new_sentence)
                    sentence_set.add(new_sentence)
