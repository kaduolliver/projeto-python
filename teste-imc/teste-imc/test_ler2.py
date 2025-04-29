import pytest
import struct
import os
from datetime import datetime, timedelta
from unittest.mock import patch
from ler2 import dados, ler_dados

class TestClasseDados:
    def test_criacao_objeto_dados(self):
        pessoa = dados("João", "2017-01-01", "Masc", 25.0, 1.20)
        assert pessoa.nome == "João"
        assert pessoa.nasc == "2017-01-01"
        assert pessoa.genero == "Masc"
        assert pessoa.peso == 25.0
        assert pessoa.altura == 1.20

    def test_calculo_idade_corretamente(self):
        hoje = datetime.now()
        datas = {
            6: hoje - timedelta(days=365*6),
            7: hoje - timedelta(days=365*7),
            8: hoje - timedelta(days=365*8)
        }

        for idade, data in datas.items():
            pessoa = dados("Teste", data.strftime("%Y-%m-%d"), "Masc", 25.0, 1.20)
            assert pessoa.calcIdade() == idade

    def test_classificacao_imc_para_menino_6_anos(self):
        nascimento = (datetime.now() - timedelta(days=365*6)).strftime("%Y-%m-%d")

        baixo_peso = dados("João", nascimento, "Masc", 20.0, 1.20)
        peso_normal = dados("João", nascimento, "Masc", 24.0, 1.20)
        sobrepeso = dados("João", nascimento, "Masc", 26.0, 1.20)
        obeso = dados("João", nascimento, "Masc", 27.0, 1.20)

        assert baixo_peso.getTarget() == 0
        assert peso_normal.getTarget() == 1
        assert sobrepeso.getTarget() == 2
        assert obeso.getTarget() == 3

    def test_classificacao_imc_para_menina_7_anos(self):
        nascimento = (datetime.now() - timedelta(days=365*7)).strftime("%Y-%m-%d")

        baixo_peso = dados("Maria", nascimento, "Femi", 20.0, 1.20)
        peso_normal = dados("Maria", nascimento, "Femi", 25.0, 1.20)
        sobrepeso = dados("Maria", nascimento, "Femi", 27.0, 1.20)
        obesa = dados("Maria", nascimento, "Femi", 28.0, 1.20)

        assert baixo_peso.getTarget() == 0
        assert peso_normal.getTarget() == 2
        assert sobrepeso.getTarget() == 2
        assert obesa.getTarget() == 3

    def test_idade_ou_genero_invalidos_geram_erro(self):
        muito_novo = (datetime.now() - timedelta(days=365*5)).strftime("%Y-%m-%d")
        muito_velho = (datetime.now() - timedelta(days=365*9)).strftime("%Y-%m-%d")

        pessoa_com_idade_invalida = dados("João", muito_novo, "Masc", 25.0, 1.20)
        pessoa_com_genero_invalido = dados("João", muito_velho, "Outro", 25.0, 1.20)

        with pytest.raises(ValueError):
            pessoa_com_idade_invalida.getTarget()

        with pytest.raises(ValueError):
            pessoa_com_genero_invalido.getTarget()

    def test_formatacao_str_do_objeto(self):
        pessoa = dados("Maria", "2017-01-01", "Femi", 25.0, 1.20)
        resultado = str(pessoa)
        assert "Nome: Maria" in resultado
        assert "Data de Nascimento: 2017-01-01" in resultado
        assert "Gênero: Femi" in resultado
        assert "Peso: 25.0 Kg" in resultado
        assert "Altura: 1.2 m" in resultado

class TestFuncaoLerDados:
    def test_leitura_arquivo_com_um_registro(self, tmp_path):
        caminho = tmp_path / "registro_teste.bin"
        formato = '30s 11s 4s f f i'

        nome = "João Silva".ljust(30, '\x00').encode()
        nascimento = "2017-01-01".ljust(11, '\x00').encode()
        genero = "Masc".ljust(4, '\x00').encode()
        peso = 25.0
        altura = 1.20
        extra = 0  # não usado

        with open(caminho, 'wb') as f:
            f.write(struct.pack(formato, nome, nascimento, genero, peso, altura, extra))

        with patch('builtins.print') as mock_print:
            ler_dados(caminho)
            mock_print.assert_called()
            saida = str(mock_print.call_args[0][0])
            assert "João Silva" in saida
            assert "2017-01-01" in saida
            assert "Masc" in saida
            assert "25.0" in saida
            assert "1.2" in saida

    def test_leitura_arquivo_vazio(self, tmp_path):
        caminho = tmp_path / "arquivo_vazio.bin"
        caminho.write_bytes(b'')

        with patch('builtins.print') as mock_print:
            ler_dados(caminho)
            mock_print.assert_not_called()
