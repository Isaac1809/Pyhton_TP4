import math
import matplotlib.pyplot as plt

class Noeud: 

    def __init__(self, value):
        self.value = value
        self.enfants = []
    

    def add_noeud(self, enfant):
        if isinstance(enfant, Noeud):
            self.enfants.append(enfant)

    def affiche(self):
        chaine = str(self.value)
        for enfant in self.enfants:
            chaine += " " + enfant.affiche()
        return chaine

    def evaluer(self, variables):

        # Cas 1 : Le nœud est une constante
        if isinstance(self.value, (int, float)):
            return float(self.value)

        # Cas 2 : Le nœud est une feuille (aucun enfant), c'est donc une variable
        if len(self.enfants) == 0:
            if self.value not in variables:
                raise ValueError(f"Valeur manquante dans le dictionnaire pour la variable : '{self.value}'")
            return float(variables[self.value])

        # Cas 3 : Opérateurs binaires (+, -, *, /)
        if self.value == "+":
            return self.enfants[0].evaluer(variables) + self.enfants[1].evaluer(
                variables
            )
        elif self.value == "-":
            return self.enfants[0].evaluer(variables) - self.enfants[1].evaluer(
                variables
            )
        elif self.value == "*":
            return self.enfants[0].evaluer(variables) * self.enfants[1].evaluer(
                variables
            )
        elif self.value == "/":
            denominateur = self.enfants[1].evaluer(variables)
            if denominateur == 0:
                raise ZeroDivisionError("Division par zéro dans l'expression.")
            return self.enfants[0].evaluer(variables) / denominateur

        # Cas 4 : Fonctions unaires (exp, log, sin, cos)
        elif self.value == "exp":
            return math.exp(self.enfants[0].evaluer(variables))
        elif self.value == "log":
            val = self.enfants[0].evaluer(variables)
            if val <= 0:
                raise ValueError(
                    "Le logarithme n'est défini que pour des valeurs strictement positives."
                )
            return math.log(val)
        elif self.value == "sin":
            return math.sin(self.enfants[0].evaluer(variables))
        elif self.value == "cos":
            return math.cos(self.enfants[0].evaluer(variables))

        else:
            raise ValueError(f"Opérateur inconnu : {self.value}")

    def tracer(self, variable, x):

        y = []
        for val in x:
            y.append(self.evaluer({variable: val}))

        plt.plot(x,y)
        plt.xlabel(variable)
        plt.ylabel("resultat")
        plt.grid(True)
        plt.show()  # Obligatoire pour afficher le graphique à l'écran


    def simplifiee(self):
        # Cas 1 : constante ou feuille variable
        if isinstance(self.value, (int, float)) or len(self.enfants) == 0:
            return Noeud(self.value)

        # Simplification d'abord des sous-arbres (bottom-up)
        enfants_simp = [e.simplifiee() for e in self.enfants]

        # Si aucune variable n'est présente dans tout le sous-arbre, on évalue
        nouveau = Noeud(self.value)
        nouveau.enfants = enfants_simp
        if len(nouveau.variables()) == 0:
            return Noeud(nouveau.evaluer({}))

        # Simplifications algébriques pour opérateurs binaires
        if len(enfants_simp) == 2:
            g, d = enfants_simp[0], enfants_simp[1]
            op = self.value

        def est_valeur(noeud, v):
                return isinstance(noeud.value, (int, float)) and noeud.value == v

            if op == "*":
                if est_valeur(g, 0) or est_valeur(d, 0):
                    return Noeud(0)
                if est_valeur(g, 1):
                    return d
                if est_valeur(d, 1):
                    return g

            elif op == "/":
                if est_valeur(g, 0):
                    return Noeud(0)
                if est_valeur(d, 1):
                    return g

            elif op == "+":
                if est_valeur(g, 0):
                    return d
                if est_valeur(d, 0):
                    return g

            elif op == "-":
                if est_valeur(d, 0):
                    return g

        return nouveau

    def derivee(self, var):
        # Constante
        if isinstance(self.value, (int, float)):
            return Noeud(0)

        # Variable (feuille)
        if len(self.enfants) == 0:
            return Noeud(1 if self.value == var else 0)

        # Helpers pour créer rapidement des arbres
        def bin_op(op, a, b):
            n = Noeud(op)
            n.add_noeud(a)
            n.add_noeud(b)
            return n

        def un_op(op, a):
            n = Noeud(op)
            n.add_noeud(a)
            return n

        u = self.enfants[0]
        du = u.derivee(var)

        if self.value in ("+", "-"):
            dv = self.enfants[1].derivee(var)
            return bin_op(self.value, du, dv)

        elif self.value == "*":
            v = self.enfants[1]
            dv = v.derivee(var)
            # u'*v + u*v'
            return bin_op("+", bin_op("*", du, v), bin_op("*", u, dv))

        elif self.value == "/":
            v = self.enfants[1]
            dv = v.derivee(var)
            # (u'*v - u*v') / (v * v)
            num = bin_op("-", bin_op("*", du, v), bin_op("*", u, dv))
            denom = bin_op("*", v, v)
            return bin_op("/", num, denom)

        elif self.value == "exp":
            # u' * exp(u)
            return bin_op("*", du, un_op("exp", u))

        elif self.value == "log":
            # u' / u
            return bin_op("/", du, u)

        elif self.value == "sin":
            # u' * cos(u)
            return bin_op("*", du, un_op("cos", u))

        elif self.value == "cos":
            # 0 - (u' * sin(u))
            terme = bin_op("*", du, un_op("sin", u))
            return bin_op("-", Noeud(0), terme)

        raise ValueError(f"Opérateur inconnu : {self.value}")