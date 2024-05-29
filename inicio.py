import tkinter as tk

janela = tk.Tk()

parte1 = tk.Label(text='Olá, Tiago',foreground='white',background='black',width=30,height=15)

parte2 = tk.Label(text='Como vai você?',foreground='red',background='blue',width=30,height=10)

resposta_feliz = tk.Button(text='Estou bem', foreground='yellow',background='red', width=25, height=5)

resposta_mm = tk.Button(text='Mais ou Menos nem pra mais nem pra menos',foreground='orange',background='red', width=35, height=5)

resposta_triste = tk.Button(text='Estou mal',foreground='grey',background='blue', width=25, height=5)

parte1.pack()

parte2.pack()

resposta_feliz.pack()

resposta_mm.pack()

resposta_triste.pack()

janela.mainloop()

janela_credenciais = tk.Tk()

rotulo_nome = tk.Label(text='Nome: ')

entrada_nome = tk.Entry()

nome = entrada_nome.get()

rotulo_senha = tk.Label(text='Senha')

entrada_senha = tk.Entry()

botao_entrar = tk.Button(text='Entrar')

rotulo_nome.pack()
entrada_nome.pack()
rotulo_senha.pack()
entrada_senha.pack()
botao_entrar.pack()

janela_credenciais.mainloop()