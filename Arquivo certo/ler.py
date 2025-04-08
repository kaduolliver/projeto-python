import struct
from datetime import datetime

class Dados:  
    def _init_(self, string1: str, string2: str, string3: str, float1: float, float2: float):
        self.nome = string1
        self.nascimento = string2
        self.genero = string3
        self.peso = float1
        self.altura = float2

    def calc_idade(self) -> int:
        try:
            n = datetime.strptime(self.nascimento, "%Y-%m-%d") 
            return (datetime.now() - n).days // 365
        except ValueError:
            print("Formato de data inválido. Use YYYY-MM-DD")
            return 0

    def calc_imc(self) -> float:
        if self.altura <= 0:
            return 0.0
        return self.peso / (self.altura ** 2)

    def classificar_imc(self, imc: float) -> str:
        if imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidade"

    def get_imc(self) -> str:
        idade = self.calc_idade()
        if idade < 18: 
            imc = self.calc_imc()
            classificacao = self.classificar_imc(imc)
            return f"{imc:.2f} ({classificacao})"
        else:
            return "IMC não calculado para adultos"

    def _str_(self) -> str:
        return (
            f"Nome: {self.nome}\n"
            f"Data de nascimento: {self.nascimento}\n"
            f"Gênero: {self.genero}\n"
            f"Idade: {self.calc_idade()}\n"
            f"Peso: {self.peso}\n"
            f"Altura: {self.altura}\n"
            f"IMC: {self.get_imc()}"
        )

def ler_dados(arq: str) -> list[Dados]:
    form = '30s 11s 4s f f i' 
    tam = struct.calcsize(form)
    pessoas = []

    with open(arq, 'rb') as f:
        while True:
            record_data = f.read(tam)
            if not record_data:
                break
            record = struct.unpack(form, record_data)
            string1 = record[0].decode().strip('\x00')
            string2 = record[1].decode().strip('\x00')
            string3 = record[2].decode().strip('\x00')
            float1 = record[3]
            float2 = record[4]
            integer = record[5]
            
            pessoa = Dados(string1, string2, string3, float1, float2)
            pessoas.append(pessoa)
            
            print(pessoa) 
            print()
    
    return pessoas

if _name_ == '_main_':
    arquivo = 'dados.bin'  
    pessoas = ler_dados(arquivo)