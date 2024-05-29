from typing import Any


class Funcionario:
    def __init__(self,nome,cargo) -> None:
        self.nome = nome
        self.cargo = cargo
        self.salario = 0


flavio = Funcionario("flavio", "Professor Informatica Básico")

print(flavio.nome," Cargo: ",flavio.cargo," Salário: ",flavio.salario)

class Professor(Funcionario):
    def __init__(self, nome, cargo) -> None:
        super().__init__(nome, cargo)
        self.disciplina = ""
    def __setdisciplina__(self, __name: str) -> None:
        self.disciplina = __name

helber = Professor("Helber","Professor")
disc1 = input("Qual diciplina ensina o helber?")
helber.__setdisciplina__(disc1)

print("Disciplina do Helber:",helber.disciplina)
