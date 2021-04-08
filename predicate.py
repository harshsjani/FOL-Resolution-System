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
        self.vars = set()

        for arg in args:
            if arg.istitle():
                self.consts.add(arg)
            else:
                self.vars.add(arg)

    def get_consts(self):
        return self.consts

    def get_vars(self):
        return self.vars
