from logic import Logic
from sentence import Sentence


def f(x):
    return x.ordered_predicates[0].ordered_args

he1 = Sentence('A(y,Bob)')
he2 = Sentence('A(x,x)')

# print(Logic.unify_predicates(he1.ordered_predicates[0], he2.ordered_predicates[0]))
print(Logic.unify2(f(he1), f(he2)))

he1 = Sentence('A(Bob,y)')
he2 = Sentence('A(x,x)')

# print(Logic.unify_predicates(he1.ordered_predicates[0], he2.ordered_predicates[0]))
print(Logic.unify2(f(he1), f(he2)))

he1 = Sentence('A(x,x)')
he2 = Sentence('A(y,Bob)')

# print(Logic.unify_predicates(he1.ordered_predicates[0], he2.ordered_predicates[0]))
print(Logic.unify2(f(he1), f(he2)))

he1 = Sentence('A(x,x)')
he2 = Sentence('A(y,Bob)')

# print(Logic.unify_predicates(he1.ordered_predicates[0], he2.ordered_predicates[0]))
print(Logic.unify2(f(he1), f(he2)))

he1 = Sentence('A(Chad,x,x)')
he2 = Sentence('A(y,y,Bob)')

# print(Logic.unify_predicates(he1.ordered_predicates[0], he2.ordered_predicates[0]))
print(Logic.unify2(f(he1), f(he2)))
