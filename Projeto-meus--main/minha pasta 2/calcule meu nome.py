
def count_letter(name, letter):
    name = name.lower()
    letter = letter.lower()
    count = name.count(letter)
    return count

name = input("Digite o seu nome: ")
letter = input("Digite a letra que deseja contar: ")
print(f"A letra '{letter}' aparece {count_letter(name, letter)} vez(es) no nome '{name}'.")
