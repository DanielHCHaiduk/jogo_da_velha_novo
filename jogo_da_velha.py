import tkinter as tk
from tkinter import messagebox
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
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
X, y = [], []  # Dados para o treino do modelo
 
# Função para reiniciar o jogo
def reiniciar_jogo():
    global tabuleiro, jogador_atual, jogadas_feitas
    tabuleiro = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    jogador_atual = jogador1
    jogadas_feitas = 0
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
        else:
            jogador_atual = jogador2 if jogador_atual == jogador1 else jogador1
 
# Função para treinar o modelo
def treinar_modelo():
    global X, y, modelo, treino_pronto
 
    # Preparar os dados para o treino (estado do tabuleiro -> próxima jogada)
    X = []
    y = []
    for partida in historicoTab:
        for i in range(len(partida)):
            for j in range(len(partida[i])):
                if partida[i][j] != '-':
                    X.append([ord(c) for linha in partida for c in linha])
                    y.append(partida[i][j])
    if len(X) > 0:
        clf = DecisionTreeClassifier()
        clf.fit(X, y)
        modelo = clf
        treino_pronto = True
        messagebox.showinfo("Treinamento", "Modelo treinado com sucesso!")
    else:
        messagebox.showinfo("Erro", "Dados insuficientes para treinamento!")
 
# Função para calcular a acurácia do modelo
def calcular_acuracia():
    if not treino_pronto:
        messagebox.showinfo("Erro", "Treine o modelo primeiro!")
        return
    X_teste = []
    y_teste = []
    for partida in historicoTab:
        for i in range(len(partida)):
            for j in range(len(partida[i])):
                if partida[i][j] != '-':
                    X_teste.append([ord(c) for linha in partida for c in linha])
                    y_teste.append(partida[i][j])
 
    if len(X_teste) > 0:
        y_pred = modelo.predict(X_teste)
        acuracia = accuracy_score(y_teste, y_pred)
        messagebox.showinfo("Acurácia", f"Acurácia do modelo: {acuracia * 100:.2f}%")
    else:
        messagebox.showinfo("Erro", "Dados insuficientes para calcular a acurácia.")
 
# Função para simular uma partida
def simular_partida():
    if not treino_pronto:
        messagebox.showinfo("Erro", "Treine o modelo primeiro!")
        return
    reiniciar_jogo()
    for i in range(9):
        X_atual = [ord(c) for linha in tabuleiro for c in linha]
        movimento = modelo.predict([X_atual])[0]
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == '-':
                    tabuleiro[i][j] = movimento
                    botoes[i][j].config(text=movimento, state="disabled")
                    break
            break
        if verificar_vencedor():
            break
 
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
 
# Botão para ver o histórico
botao_historico = tk.Button(janela, text="Mostrar Histórico", command=lambda: messagebox.showinfo("Histórico", str(historicoTab)))
botao_historico.grid(row=3, column=0, columnspan=3)
 
# Botão para treinar o modelo
botao_treinar = tk.Button(janela, text="Treinar Modelo", command=treinar_modelo)
botao_treinar.grid(row=4, column=0, columnspan=3)
 
# Botão para calcular acurácia
botao_acuracia = tk.Button(janela, text="Calcular Acurácia", command=calcular_acuracia)
botao_acuracia.grid(row=5, column=0, columnspan=3)
 
# Botão para simular uma partida
botao_simular = tk.Button(janela, text="Simular Partida", command=simular_partida)
botao_simular.grid(row=6, column=0, columnspan=3)
 
# Iniciar a interface gráfica
janela.mainloop()
