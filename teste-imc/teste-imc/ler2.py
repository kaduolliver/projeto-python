import struct
from datetime import datetime

class dados():
    def __init__(self, nome:str, nasc:str, genero:str, peso:float, altura:float):
        self.nome = nome
        self.nasc = nasc
        self.genero = genero
        self.peso = peso
        self.altura = altura
    
    def calcIdade(self):
        n = datetime.strptime(self.nasc, "%Y-%m-%d")
        return (datetime.now() - n).days // 365

    def getTarget(self):
        idade = self.calcIdade()
        imc = self.peso / (self.altura**2)

        if self.genero == 'Masc':
            if idade == 6:
                return self._avaliar_imc(imc, [14.5, 16.7, 18])
            elif idade == 7:
                return self._avaliar_imc(imc, [15, 17.4, 19.1])
            elif idade == 8:
                return self._avaliar_imc(imc, [15.6, 16.8, 20.3])

        elif self.genero == 'Femi':
            if idade == 6:
                return self._avaliar_imc(imc, [14.3, 16.2, 17.4])
            elif idade == 7:
                return self._avaliar_imc(imc, [14.9, 17.2, 18.9])
            elif idade == 8:
                return self._avaliar_imc(imc, [15.6, 18.2, 20.3])

        raise ValueError(f"Idade ou gênero inválido: idade={idade}, gênero={self.genero}")

    def _avaliar_imc(self, imc, limites):
        if imc < limites[0]:
            return 0
        elif imc < limites[1]:
            return 1
        elif imc < limites[2]:
            return 2
        else:
            return 3

    def __str__(self) -> str:
        return (f"Nome: {self.nome}\n"
                f"Data de Nascimento: {self.nasc}\n"
                f"Gênero: {self.genero}\n"
                f"Idade: {self.calcIdade()}\n"
                f"Peso: {self.peso} Kg\n"
                f"Altura: {self.altura} m\n"
                f"Interpretação IMC: {self.getTarget()}")

def ler_dados(arq):
    form = '30s 11s 4s f f i'
    tam = struct.calcsize(form)

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
            dado = dados(string1, string2, string3, float1, float2)
            print(dado)

if __name__ == '__main__':
    ler_dados('dados.bin')
