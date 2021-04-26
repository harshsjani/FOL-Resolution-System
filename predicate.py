from constants import Consts
from collections import defaultdict


class Predicate:
    def __init__(self, literal):
        self.negated = literal.count(Consts.NOT) % 2 != 0
        literal = literal.replace(Consts.NOT, "").strip()
        lb_idx = literal.index(Consts.left_bracket)
        rb_idx = literal.index(Consts.right_bracket)

        self.name = literal[:lb_idx]
        args = literal[lb_idx + 1: rb_idx].split(Consts.args_sep)

        self.consts = defaultdict(int)
        self.ordered_consts = []
        self.vars = defaultdict(int)
        self.ordered_vars = []
        self.ordered_args = []

        for arg in args:
            arg = arg.strip()
            if arg[0].isupper():
                self.consts[arg] += 1
                self.ordered_consts.append(arg)
            else:
                self.vars[arg] += 1
                self.ordered_vars.append(arg)
            self.ordered_args.append(arg)

    def __str__(self):
        ret = [Consts.NOT] if self.negated else []
        ret += [self.name]
        ret += ["("]
        for x in self.ordered_args:
            ret += [x + ","]
        ret[-1] += ")"
        ret[-1] = ret[-1].replace(",)", ")")
        return "".join(ret)

    def get_consts(self):
        return self.consts

    def get_vars(self):
        return self.vars

    def get_args(self):
        return self.ordered_args

    def subst(self, subst_list):
        if not subst_list:
            return
        # None or mapping {x: Dan, y: Bella}
        # {x: y, z: Shawn}
        for var, value in subst_list.items():
            while self.vars[var] > 0:
                self.vars[var] -= 1
                idx = self.ordered_args.index(var)
                self.ordered_vars.remove(var)
                self.ordered_args.remove(var)
                self.ordered_args.insert(idx, value)

                if (value[0].isupper()):
                    self.ordered_consts.insert(idx, value)
                    self.consts[value] += 1
                else:
                    self.ordered_vars.insert(idx, value)
                    self.vars[value] += 1

    @staticmethod
    def are_equal(pred1, pred2):
        if pred1.negated ^ pred2.negated:
            return False
        if pred1.name != pred2.name:
            return False
        return pred1.ordered_args == pred2.ordered_args
