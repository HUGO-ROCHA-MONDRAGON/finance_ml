import numpy as np

class DataFrameSimple:
    def __init__(self, data):
        self.donnees = np.array(list(data.values())).T
        self.colonnes = list(data.keys())

    def afficher(self):
        header = " ".join(f"{col:>10}" for col in self.colonnes)
        rows = [" ".join(f"{val:10}" for val in row) for row in self.donnees[:5]]
        return "\n".join([header] + rows)

    def moyenne(self, nom_colonne):
        return np.mean(self.select_colonne(nom_colonne))

    def somme(self, nom_colonne):
        return np.sum(self.select_colonne(nom_colonne))

    def min(self, nom_colonne):
        return np.min(self.select_colonne(nom_colonne))

    def max(self, nom_colonne):
        return np.max(self.select_colonne(nom_colonne))

    def select_colonne(self, nom_colonne):
        index = self.colonnes.index(nom_colonne)
        return self.donnees[:, index]