class Liste():
    def __init__(self):
        self._elements = {} 
        self._count = 0 

    def append(self, element):
        """Ajoute un élément à la fin de la liste"""#
        self._elements[self._count] = element
        self._count += 1

    def remove(self, valeur): 
        """Supprime la première occurrence de la valeur donnée."""
        index = self.get_index(valeur)
        if index != -1:
            self.pop(index)
        else:
            raise ValueError(f"{valeur} n'est pas dans la liste")

    def pop(self, index):
        valeur = self._elements[index] #On récupère la valeur stockée à cet index → c’est ce qu’on va retourner à la fin.
        # Décale les éléments
        for j in range(index, self._count - 1):
            self._elements[j] = self._elements[j + 1]
        del self._elements[self._count - 1]
        self._count -= 1
        return valeur
    
    def get_index(self, valeur): 
        for i in range(self._count):
            if self._elements[i] == valeur:
                return i
        return -1 


import unittest

class TestListe(unittest.TestCase):
    def setUp(self):
        self.liste = Liste()

    def test_append(self):
        self.liste.append(1)
        self.liste.append("deux")
        self.liste.append([3, 4])
        self.assertEqual(self.liste._elements, {0: 1, 1: "deux", 2: [3, 4]})
        self.assertEqual(self.liste._count, 3)

    def test_remove(self):
        self.liste.append(1)
        self.liste.append(2)
        self.liste.append(1)
        self.liste.remove(1)
        self.assertEqual(self.liste._elements, {0: 2, 1: 1})
        self.assertEqual(self.liste._count, 2)

    def test_pop(self):
        self.liste.append(1)
        self.liste.append(2)
        self.liste.append(3)
        element = self.liste.pop(1)
        self.assertEqual(element, 2)
        self.assertEqual(self.liste._elements, {0: 1, 1: 3})
        self.assertEqual(self.liste._count, 2)

    def test_get_index(self):
        self.liste.append(1)
        self.liste.append(2)
        self.liste.append(3)
        self.liste.append(2)
        self.assertEqual(self.liste.get_index(2), 1)
        self.assertEqual(self.liste.get_index(4), -1)

def run_tests():
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()