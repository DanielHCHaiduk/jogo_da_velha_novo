import tkinter as tk
from tkinter import messagebox
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import random

# Variáveis globais
tabuleiro = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
historicoTab = []
ganhadores = []
jogador1 = "X"
jogador2 = "O"
jogador_atual = jogador1
modelo = None
jogadas_feitas = 0  # Contador de jogadas
treino_pronto = False  # Indica se o modelo foi treinado

# Função para reiniciar o jogo
def reiniciar_jogo():
    global tabuleiro, jogador_atual, jogadas_feitas
    tabuleiro = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    jogador_atual = jogador1
    jogadas_feitas = 0  # Reinicia o contador de jogadas
    for i in range(3):
        for j in range(3):
            botoes[i][j].config(text="", state="normal")

# Função para verificar se há um vencedor
def verificar_vencedor():
    linha = ganharEmLinha()
    coluna = ganharEmColuna()
    diagonal = ganharEmDiagonal()

    if linha or coluna or diagonal:
        for i in range(3):
            for j in range(3):
                botoes[i][j].config(state="disabled")
        return True
    return False

# Funções de vitória
def ganharEmLinha():
    for a in range(3):
        if tabuleiro[a][0] == tabuleiro[a][1] == tabuleiro[a][2] != '-':
            messagebox.showinfo("Fim de jogo", f"O jogador {tabuleiro[a][0]} ganhou!")
            ganhadores.append(f"Jogador {tabuleiro[a][0]} ganhou!")
            return True
    return False

def ganharEmColuna():
    for a in range(3):
        if tabuleiro[0][a] == tabuleiro[1][a] == tabuleiro[2][a] != '-':
            messagebox.showinfo("Fim de jogo", f"O jogador {tabuleiro[0][a]} ganhou!")
            ganhadores.append(f"Jogador {tabuleiro[0][a]} ganhou!")
            return True
    return False

def ganharEmDiagonal():
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != '-':
        messagebox.showinfo("Fim de jogo", f"O jogador {tabuleiro[0][0]} ganhou!")
        ganhadores.append(f"Jogador {tabuleiro[0][0]} ganhou!")
        return True
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != '-':
        messagebox.showinfo("Fim de jogo", f"O jogador {tabuleiro[0][2]} ganhou!")
        ganhadores.append(f"Jogador {tabuleiro[0][2]} ganhou!")
        return True
    return False

def darVelha():
    for linha in tabuleiro:
        if "-" in linha:
            return False
    messagebox.showinfo("Fim de jogo", "Deu velha!")
    ganhadores.append("Deu velha!")
    return True

# Função executada quando um botão é clicado
def clique_botao(i, j):
    global jogador_atual, tabuleiro, jogadas_feitas

    if tabuleiro[i][j] == "-":
        tabuleiro[i][j] = jogador_atual
        botoes[i][j].config(text=jogador_atual, state="disabled")
        jogadas_feitas += 1

        if verificar_vencedor():
            historicoTab.append([linha[:] for linha in tabuleiro])
            reiniciar_jogo()
        elif darVelha():
            historicoTab.append([linha[:] for linha in tabuleiro])
            reiniciar_jogo()
        else:
            jogador_atual = jogador2 if jogador_atual == jogador1 else jogador1

# Função para treinar o modelo de IA com base no histórico de jogadas
def treinar_modelo():
    global modelo, treino_pronto
    if len(historicoTab) < 5:  # Verifica se há dados suficientes para treinar o modelo
        messagebox.showinfo("Erro", "É necessário pelo menos 5 partidas para treinar o modelo!")
        return
    
    # Coleta os dados do histórico
    X = []
    y = []
    for partida in historicoTab:
        estado_partida = []
        for i in range(3):
            for j in range(3):
                estado = 1 if partida[i][j] == jogador1 else -1 if partida[i][j] == jogador2 else 0
                estado_partida.append(estado)
        X.append(estado_partida)
        y.append(random.choice([jogador1, jogador2]))  # Gera rótulos aleatórios para o treino

    X = np.array(X)  # Organiza o tabuleiro como uma única lista
    y = np.array(y)

    # Treina o modelo com base nos dados
    clf = DecisionTreeClassifier(max_depth=5)  # Árvore de decisão
    clf.fit(X, y)

    modelo = clf
    treino_pronto = True
    messagebox.showinfo("Treino", "Modelo treinado com sucesso!")

# Função para simular jogadas automáticas
def simular_jogada():
    global jogador_atual, tabuleiro, modelo, treino_pronto
    if not treino_pronto:
        messagebox.showinfo("Erro", "O modelo precisa ser treinado primeiro!")
        return

    jogada_feita = False
    while not jogada_feita:
        i, j = random.randint(0, 2), random.randint(0, 2)  # Seleciona uma posição aleatória
        if tabuleiro[i][j] == "-":
            tabuleiro[i][j] = jogador_atual
            botoes[i][j].config(text=jogador_atual, state="disabled")
            jogada_feita = True

    if verificar_vencedor():
        historicoTab.append([linha[:] for linha in tabuleiro])
        reiniciar_jogo()
    elif darVelha():
        historicoTab.append([linha[:] for linha in tabuleiro])
        reiniciar_jogo()
    else:
        jogador_atual = jogador2 if jogador_atual == jogador1 else jogador1

# Função para mostrar o histórico das jogadas
def mostrar_historico():
    historico_str = ""
    for partida in historicoTab:
        for linha in partida:
            historico_str += " ".join(linha) + "\n"
        historico_str += "\n"
    messagebox.showinfo("Histórico", historico_str)

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

# Botão para treinar o modelo
botao_treinar = tk.Button(janela, text="Treinar Modelo", command=treinar_modelo)
botao_treinar.grid(row=3, column=0, columnspan=3)

# Botão para simular jogada
botao_simular = tk.Button(janela, text="Simular Jogada", command=simular_jogada)
botao_simular.grid(row=4, column=0, columnspan=3)

# Botão para mostrar histórico
botao_historico = tk.Button(janela, text="Mostrar Histórico", command=mostrar_historico)
botao_historico.grid(row=5, column=0, columnspan=3)

# Iniciar a interface gráfica
janela.mainloop()
