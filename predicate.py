from constants import Consts


class Predicate:
    def __init__(self, literal):
        self.negated = literal.count(Consts.NOT) % 2 != 0
        literal = literal.replace(Consts.NOT, "").strip()
        lb_idx = literal.index(Consts.left_bracket)
        rb_idx = literal.index(Consts.right_bracket)

        self.name = literal[:lb_idx]
        args = literal[lb_idx + 1: rb_idx].split(Consts.args_sep)

        self.consts = set()
        self.ordered_consts = []
        self.vars = set()
        self.ordered_vars = []
        self.ordered_args = []

        for arg in args:
            if arg[0].isupper():
                self.consts.add(arg)
                self.ordered_consts.append(arg)
            else:
                self.vars.add(arg)
                self.ordered_vars.append(arg)
            self.ordered_args.append(arg)

    # def __eq__(self, other):
    #     return self.name == other.name and self.negated == other.negated

    # def __hash__(self):

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
        for var, const in subst_list:
            if var in self.vars:
                self.vars.discard(var)
                idx = self.ordered_args.index(var)
                self.ordered_vars.remove(var)
                self.ordered_consts.insert(idx, const)
                self.ordered_args.remove(var)
                self.ordered_args.insert(idx, const)
                self.consts.add(const)
