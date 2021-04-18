import kb
import logic
from sentence import Sentence


he1 = Sentence('Cat(x) | Dog(Dobby)')
he2 = Sentence('Dog(y) | Cat(Bella)')

if len(he1.predicate_names) != len(he2.predicate_names):
    return False
print(he1.predicate_names == he2.predicate_names)