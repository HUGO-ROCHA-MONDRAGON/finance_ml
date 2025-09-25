
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

    # ---------- DUNDER METHODS ----------
    def __str__(self):
        return self.afficher()

    def __len__(self):
        return self.donnees.shape[0]

    def __getitem__(self, key):
        if key not in self.colonnes:
            raise KeyError(f"Colonne {key} inexistante.")
        return self.select_colonne(key)

    def __setitem__(self, key, value):
        value = np.array(value)
        if value.shape[0] != self.donnees.shape[0]:
            raise ValueError("La longueur de la colonne ne correspond pas au DataFrame.")
        if key in self.colonnes:
            index = self.colonnes.index(key)
            self.donnees[:, index] = value
        else:
            self.colonnes.append(key)
            self.donnees = np.column_stack([self.donnees, value])

    def __iter__(self):
        return iter(self.colonnes)

    def __add__(self, other):
        """Addition avec un scalaire, numpy array ou un autre DataFrameSimple"""
        if isinstance(other, (int, float, np.floating)):   # ✅ marche avec np 2.0
            return DataFrameSimple({col: self.donnees[:, i] + other
                                    for i, col in enumerate(self.colonnes)})

        elif isinstance(other, DataFrameSimple):
            if self.colonnes != other.colonnes or self.donnees.shape != other.donnees.shape:
                raise ValueError("Les DataFrames doivent avoir les mêmes dimensions et colonnes.")
            return DataFrameSimple({col: self.donnees[:, i] + other.donnees[:, i]
                                    for i, col in enumerate(self.colonnes)})

        elif isinstance(other, np.ndarray):
            if other.shape != self.donnees.shape:
                raise ValueError("Dimensions incompatibles avec le DataFrame.")
            return DataFrameSimple({col: self.donnees[:, i] + other[:, i]
                                    for i, col in enumerate(self.colonnes)})

        else:
            raise TypeError(f"Addition non supportée entre DataFrameSimple et {type(other)}")


import unittest
import numpy as np

class TestDataFrameSimpleDunder(unittest.TestCase):
    def setUp(self):
        self.df = DataFrameSimple({'A': [1, 2, 3], 'B': [4, 5, 6]})

    def test_len(self):
        self.assertEqual(len(self.df), 3)

    def test_getitem(self):
        np.testing.assert_array_equal(self.df['A'], np.array([1, 2, 3]))

    def test_setitem(self):
        self.df['C'] = [7, 8, 9]
        np.testing.assert_array_equal(self.df['C'], np.array([7, 8, 9]))

    def test_iter(self):
        self.assertEqual(list(self.df), ['A', 'B'])

    def test_add_scalar(self):
        result = self.df + 1
        np.testing.assert_array_equal(result.donnees, np.array([[2, 5], [3, 6], [4, 7]]))

    def test_add_dataframe(self):
        other = DataFrameSimple({'A': [10, 20, 30], 'B': [40, 50, 60]})
        result = self.df + other
        np.testing.assert_array_equal(result.donnees, np.array([[11, 44], [22, 55], [33, 66]]))

    def test_add_array(self):
        arr = np.array([[10, 40], [20, 50], [30, 60]])
        result = self.df + arr
        np.testing.assert_array_equal(result.donnees, np.array([[11, 44], [22, 55], [33, 66]]))

    def test_add_invalid(self):
        with self.assertRaises(TypeError):
            _ = self.df + "invalid"

def run_tests():
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()