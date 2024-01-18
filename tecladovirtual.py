# Importar o módulo tkinter
import tkinter as tk

# Criar uma janela principal
root = tk.Tk()
root.title("Teclado Virtual")

# Criar uma entrada de texto
entry = tk.Entry(root)
entry.grid(row=0, columnspan=15)

# Criar uma função para inserir um caractere na entrada
def insert(char):
    entry.insert(tk.END, char)

# Criar uma função para apagar o último caractere da entrada
def delete():
    entry.delete(len(entry.get())-1, tk.END)

# Criar uma função para limpar a entrada
def clear():
    entry.delete(0, tk.END)

# Criar uma lista com os caracteres do teclado
keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ç"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", ";"],
    ["Del", "Espaço", "Enter"]
]

# Criar um loop para criar os botões do teclado
row = 1
for keyrow in keys:
    col = 0
    for key in keyrow:
        # Se o caractere for especial, criar um botão com uma função específica
        if key == "Del":
            button = tk.Button(root, text=key, width=5, command=delete)
        elif key == "Espaço":
            button = tk.Button(root, text=key, width=5, command=lambda: insert(" "))
        elif key == "Enter":
            button = tk.Button(root, text=key, width=5, command=root.destroy)
        # Se o caractere for normal, criar um botão com a função de inserir
        else:
            button = tk.Button(root, text=key, width=5, command=lambda x=key: insert(x))
        # Posicionar o botão na janela
        button.grid(row=row, column=col)
        col += 1
    row += 1

# Criar um botão para limpar a entrada
button = tk.Button(root, text="Limpar", width=5, command=clear)
button.grid(row=row, columnspan=15)

# Iniciar o loop principal da janela
root.mainloop()