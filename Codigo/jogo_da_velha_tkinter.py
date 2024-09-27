import tkinter as tk
from tkinter import messagebox

# Variáveis globais
tabuleiro = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
historicoTab = []
ganhadores = []
jogador1 = "X"
jogador2 = "O"
jogador_atual = jogador1

# Função para reiniciar o jogo
def reiniciar_jogo():
    global tabuleiro, jogador_atual
    tabuleiro = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    jogador_atual = jogador1
    for i in range(3):
        for j in range(3):
            botoes[i][j].config(text="", state="normal")

# Função para verificar se há um vencedor
def verificar_vencedor():
    velha = darVelha()
    linha = ganharEmLinha()
    coluna = ganharEmColuna()
    diagonal = ganharEmDiagonal()

    if velha or linha or coluna or diagonal:
        for i in range(3):
            for j in range(3):
                botoes[i][j].config(state="disabled")
        return True
    return False

# Funções de vitória
def ganharEmLinha():
    for a in range(3):
        if tabuleiro[a][0] == tabuleiro[a][1] == tabuleiro[a][2] != '_':
            messagebox.showinfo("Fim de jogo", f"O jogador {tabuleiro[a][0]} ganhou!")
            ganhadores.append(f"Jogador {tabuleiro[a][0]} ganhou!")
            return True
    return False

def ganharEmColuna():
    for a in range(3):
        if tabuleiro[0][a] == tabuleiro[1][a] == tabuleiro[2][a] != '_':
            messagebox.showinfo("Fim de jogo", f"O jogador {tabuleiro[0][a]} ganhou!")
            ganhadores.append(f"Jogador {tabuleiro[0][a]} ganhou!")
            return True
    return False

def ganharEmDiagonal():
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != '_':
        messagebox.showinfo("Fim de jogo", f"O jogador {tabuleiro[0][0]} ganhou!")
        ganhadores.append(f"Jogador {tabuleiro[0][0]} ganhou!")
        return True
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != '_':
        messagebox.showinfo("Fim de jogo", f"O jogador {tabuleiro[0][2]} ganhou!")
        ganhadores.append(f"Jogador {tabuleiro[0][2]} ganhou!")
        return True
    return False

def darVelha():
    for linha in tabuleiro:
        if "_" in linha:
            return False
    messagebox.showinfo("Fim de jogo", "Deu velha!")
    ganhadores.append("Deu velha!")
    return True

# Função executada quando um botão é clicado
def clique_botao(i, j):
    global jogador_atual, tabuleiro

    if tabuleiro[i][j] == "_":
        tabuleiro[i][j] = jogador_atual
        botoes[i][j].config(text=jogador_atual, state="disabled")

        if verificar_vencedor():
            historicoTab.append([linha[:] for linha in tabuleiro])
            reiniciar_jogo()
        else:
            jogador_atual = jogador2 if jogador_atual == jogador1 else jogador1

# Configurar a interface gráfica
janela = tk.Tk()
janela.title("Jogo da Velha")

botoes = [[None, None, None], [None, None, None], [None, None, None]]

# Criar os botões para o tabuleiro
for i in range(3):
    for j in range(3):
        botoes[i][j] = tk.Button(janela, text="", width=10, height=3, 
                                 font=("Arial", 24), 
                                 command=lambda i=i, j=j: clique_botao(i, j))
        botoes[i][j].grid(row=i, column=j)

# Exibir o histórico de jogos
def mostrar_historico():
    historico_str = ""
    for partida in historicoTab:
        for linha in partida:
            historico_str += " ".join(linha) + "\n"
        historico_str += "\n"
    messagebox.showinfo("Histórico", historico_str)

# Botão para ver o histórico
botao_historico = tk.Button(janela, text="Mostrar Histórico", command=mostrar_historico)
botao_historico.grid(row=3, column=0, columnspan=3)

# Iniciar a interface gráfica
janela.mainloop()
