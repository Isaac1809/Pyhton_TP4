from TP3 import Noeud

n1 = Noeud("exp")
n2 = Noeud("+")
n3 = Noeud(2)
n4 = Noeud("y")

n1.add_noeud(n2)
n2.add_noeud(n3)
n2.add_noeud(n4)

print(n1.affiche())

d1 = dict(x=3, y=0, l=[1,2])

print(n1.evaluer(d1))
print(n2.evaluer(d1))
print(n3.evaluer(d1))
print(n4.evaluer(d1))

y1 = [i * 0.1 for i in range(0, 100)]
n1.tracer("y",y1)

d_brute = n1.derivee("y")
print("Dérivée brute :", d_brute.affiche())
# Affiche : * + 0 1 exp + 2 y

d_simplifiee = d_brute.simplifiee()
print("Dérivée simplifiée :", d_simplifiee.affiche())
# Affiche : exp + 2 y  (car (0 + 1) * exp(2 + y) = exp(2 + y))