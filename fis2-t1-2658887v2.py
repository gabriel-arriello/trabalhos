# Autor: Gabriel Arriello Santana
# RA: 2658887
# SIMULADOR DE OSCILAÇÕES ACOPLADAS #

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import pi, sqrt, sin, cos
from scipy.integrate import odeint

# Mensagem de abertura
print("\nSIMULADOR DE OSCILAÇÕES ACOPLADAS DE MASSAS-MOLAS\nFísica 2 - APS 1 | Professor: Rafael Barreto\nGabriel Arriello Santana - 2658887\n")

# Função para interpretar entradas que incluem "pi" ou "π"
def input_pi(value):
    return eval(value.replace("π", "pi").replace("pi", str(pi)))

# Definição da classe para os objetos oscilantes
class ObjOscilante:
    def __init__(self, Xo, A, fase):
        self.m = m # Massa de cada objeto (kg)
        self.w = w # Frequência angular de cada objeto (rad/s)
        self.Xo = Xo  # Posição inicial (m)
        self.A = A  # Amplitude (m)
        self.fase = fase  # Constante de fase (rad)
        self.Vo = Vo # Velocidade inicial (m/s)

# Declaração de parâmetros fixos
tam = 20  # Tamanho do eixo horizontal (m)
m = 4  
k = 100  # Constante elástica (N/m)
w = sqrt(k/m)  

# Solicita entradas do usuário
n_massas = int(input("Número de massas (2 a 10): "))
while not (2 <= n_massas <= 10):
    print("Por favor, insira um número entre 2 e 10.")
    n_massas = int(input("Número de massas (2 a 10): "))

masses = []
for i in range(n_massas):
    print(f"\nDados para a massa {i + 1}:")
    Xo = float(input(f"    Posição inicial (Xo) [m] (0 a 20): "))
    A = float(input(f"    Amplitude (A) [m]: "))
    print(f"    Frequência angular (w) [rad/s]: {w:.0f}")
    fase = float(input_pi(input(f"    Constante de fase (φ) [rad]: ")))
    Vo = w * A * sin(fase)  # Velocidade inicial
    print(f"    Velocidade inicial (Vo) [m/s]: {Vo:.2f}")

    # Cria o objeto oscilante para cada massa
    masses.append(ObjOscilante(Xo, A, fase))

# Função para calcular as forças e derivadas
def sistema_dinamico(Y, t, m, k, n_massas):
    # Y é o vetor que contém as posições e velocidades das massas
    posicoes = Y[:n_massas]
    velocidades = Y[n_massas:]

    # Vetor de forças
    forcas = np.zeros(n_massas)

    # Forças das molas internas e nas extremidades
    for i in range(n_massas):
        if i == 0:
            # A primeira massa tem mola com a parede
            forcas[i] = -k * (posicoes[i] - 0)
        else:
            # Forças de molas internas entre as massas
            forcas[i] += -k * (posicoes[i] - posicoes[i - 1])

        if i == n_massas - 1:
            # A última massa tem mola com a parede
            forcas[i] += -k * (posicoes[i] - tam)
        else:
            # Forças de molas internas entre as massas
            forcas[i] += -k * (posicoes[i] - posicoes[i + 1])

    # As equações diferenciais: m * a = F => a = F / m
    aceleracoes = forcas / m

    # Retorna as derivadas: velocidade e aceleração
    return np.concatenate([velocidades, aceleracoes])

# Definir as condições iniciais para as equações diferenciais
condicoes_iniciais = np.zeros(2 * n_massas)

# Posições iniciais das massas
for i in range(n_massas):
    condicoes_iniciais[i] = masses[i].Xo

# Velocidades iniciais das massas
for i in range(n_massas):
    condicoes_iniciais[n_massas + i] = masses[i].Vo

# Resolução do sistema de equações diferenciais
t = np.linspace(0, 300, 30000)  # Intervalo de tempo para a simulação
solucao = odeint(sistema_dinamico, condicoes_iniciais, t, args=(m, k, n_massas))

# Posições das massas ao longo do tempo
posicoes = solucao[:, :n_massas]

# Configuração da animação
fig, ax = plt.subplots(figsize=(10, 3))
ax.set_xlim(0, tam)
ax.set_ylim(-0.5, 0.5)
ax.set_title("Simulador de Oscilações Acopladas de Massas-Molas", fontsize=14, pad=20)

# Adiciona o timer ao gráfico
timer = ax.text(0.95, 0.9, '', transform=ax.transAxes, fontsize=12, ha='right')

# Elementos gráficos: linha da mola e massas
linha_mola = ax.plot([0, tam], [0, 0], lw=2, color='gray')[0]  # Linha preta fixa representando a mola
caixa_massa = [
    ax.add_patch(plt.Rectangle((0, -0.1), 0.5, 0.2, color='blue')) for _ in range(n_massas)
]

def init():
    linha_mola.set_data([0, tam], [0, 0])  # Linha fixa para a mola
    for patch in caixa_massa:
        patch.set_xy((0, -0.1))
    timer.set_text('t = 0.00 s')
    return [linha_mola] + caixa_massa + [timer]

def update(frame):
    t_frame = t[frame]  # Obtém o tempo correspondente ao frame atual
    pos_massa = posicoes[frame]  # Atualiza a posição das massas com base na solução

    # Atualiza as posições das massas
    for i, patch in enumerate(caixa_massa):
        patch.set_xy((pos_massa[i], -0.1))

    # Atualiza o timer na tela
    timer.set_text(f't = {t_frame:.2f} s')
    return [linha_mola] + caixa_massa + [timer]

# Cria a animação
ani = FuncAnimation(
    fig, update, frames=len(t), init_func=init, blit=True, interval=15, cache_frame_data=False
)

plt.show()