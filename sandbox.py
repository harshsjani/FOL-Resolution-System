from logic import Logic
from sentence import Sentence


def f(x):
    return x.ordered_predicates[0].ordered_args

# he1 = Sentence('A(y,Bob)')
# he2 = Sentence('A(x,x)')


he1 = Sentence("FA(y1,y1,x1)")
he2 = Sentence("~FA(x2,y2,y2)")
he3 = Sentence("AB(x2,y2,z1)")

subs = Logic.unify2(he1.ordered_predicates[0].ordered_args, f(he2))
print(subs)

he3.ordered_predicates[0].subst(subs)
print(str(he3))

he4 = Sentence("A(x,y)")
subs2 = {"y": "Bob", "x": "y"}
he4.ordered_predicates[0].subst(subs2)
print(str(he4))
