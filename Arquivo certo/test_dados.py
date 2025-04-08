import unittest
import os
from dados import Dados, ler_dados

class TestDados(unittest.TestCase):

    def setUp(self):
        self.pessoa = Dados(nome="Teste", idade, peso, altura)

    def test_classificar_imc(self):
        self.assertEqual(self.pessoa.classificar_imc(18.5), "Abaixo do peso")
        self.assertEqual(self.pessoa.classificar_imc(25), "Peso normal")
        self.assertEqual(self.pessoa.classificar_imc(30), "Sobrepeso")
        self.assertEqual(self.pessoa.classificar_imc(31), "Obesidade")

if __name__ == '__main__':
    unittest.main()