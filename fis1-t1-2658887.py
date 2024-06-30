# Autor: Gabriel Arriello Santana
# RA: 2658887
# SIMULADOR DE COLISÕES #

import pygame
import random
import math

# Inicializando o Pygame
pygame.init()

# Tamanhos da tela
sizes = {
    'G': (1120, 630),  # Grande
    'M': (880, 495),   # Médio
    'P': (640, 360)    # Pequeno
}

# Cor do fundo
preto = (0, 0, 0)

# Classe Bola
class Ball:
    def __init__(self, x, y, raio, massa, cor, vx, vy):
        self.x = x              # Posição em x
        self.y = y              # Posição em y
        self.raio = raio
        self.massa = massa
        self.cor = cor
        self.vx = vx            # Velocidade em x
        self.vy = vy            # Velocidade em y

    def mover_bola(self):
        self.x += self.vx
        self.y += self.vy

    def desenhar_bola(self, screen):
        pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.raio)

def colisoes_bolas(bola1, bola2, coef_restituicao):
    dx = bola2.x - bola1.x
    dy = bola2.y - bola1.y
    distancia = math.hypot(dx, dy)

    if distancia < bola1.raio + bola2.raio:
        # Ângulo e seno/cosseno da direção da colisão
        angulo = math.atan2(dy, dx)
        seno = math.sin(angulo)
        cosseno = math.cos(angulo)

        # Reposicionando as bolas para evitar sobreposição
        sobra = bola1.raio + bola2.raio - distancia
        bola1.x -= sobra * cosseno / 2
        bola1.y -= sobra * seno / 2
        bola2.x += sobra * cosseno / 2
        bola2.y += sobra * seno / 2

        # Componentes de velocidade ao longo e perpendicular à linha de colisão
        v1r = bola1.vx * cosseno + bola1.vy * seno
        v1t = -bola1.vx * seno + bola1.vy * cosseno
        v2r = bola2.vx * cosseno + bola2.vy * seno
        v2t = -bola2.vx * seno + bola2.vy * cosseno

        # Velocidade do centro de massa ao longo da linha de colisão
        vcm = (v1r * bola1.massa + v2r * bola2.massa) / (bola1.massa + bola2.massa)

        # Novas velocidades radiais após a colisão com coeficiente de restituição
        e = coef_restituicao
        v1r_final = vcm * (1 + e) - v1r * e
        v2r_final = vcm * (1 + e) - v2r * e

        # Convertendo de volta para as componentes originais
        bola1.vx = v1r_final * cosseno - v1t * seno
        bola1.vy = v1r_final * seno + v1t * cosseno
        bola2.vx = v2r_final * cosseno - v2t * seno
        bola2.vy = v2r_final * seno + v2t * cosseno

def colisoes_paredes(ball, screen_largura, screen_altura):
    # Verifica colisão com a parede esquerda
    if ball.x - ball.raio < 0:
        ball.x = ball.raio
        ball.vx = abs(ball.vx) if ball.vx < 0 else ball.vx
    # Verifica colisão com a parede direita
    elif ball.x + ball.raio > screen_largura:
        ball.x = screen_largura - ball.raio
        ball.vx = -abs(ball.vx) if ball.vx > 0 else ball.vx

    # Verifica colisão com a parede superior
    if ball.y - ball.raio < 0:
        ball.y = ball.raio
        ball.vy = abs(ball.vy) if ball.vy < 0 else ball.vy
    # Verifica colisão com a parede inferior
    elif ball.y + ball.raio > screen_altura:
        ball.y = screen_altura - ball.raio
        ball.vy = -abs(ball.vy) if ball.vy > 0 else ball.vy

# Função principal
def main():
    # Pergunta ao usuário o tamanho da tela
    print("Escolha o tamanho da tela (grande [G], medio [M], pequeno [P]): ", end="")
    tamanho_tela = input().strip().upper()

    # Define as dimensões da tela com base na escolha do usuário
    screen_largura, screen_altura = sizes.get(tamanho_tela, (880, 495))
    screen = pygame.display.set_mode((screen_largura, screen_altura))

    # Pergunta ao usuário o coeficiente de restituição
    while True:
        try:
            coef_restituicao = float(input("Digite o coeficiente de restituição (entre 0 e 1.5): ").strip())
            if 0 <= coef_restituicao <= 1.5:
                break
            else:
                print("Digite um valor entre 0 e 1.5.")
        except ValueError:
            print("Digite um valor numérico válido.")

    num_bolas = int(input("Digite o número de bolas: "))
    massas = []
    for i in range(num_bolas):
        massa = float(input(f"Digite a massa da bola {i+1}: "))
        massas.append(massa)
    
    balls = []
    raio_constante = 10  # Constante para calcular o raio

    for massa in massas:
        raio = int(math.log(massa + 1) * raio_constante)  # ln para normalizar visualmente o tam das bolas
        x = random.randint(raio, screen_largura - raio)
        y = random.randint(raio, screen_altura - raio)
        cor = [random.randint(0, 255) for _ in range(3)]
        vx = random.uniform(-2, 2)  # Faixa de velocidades iniciais
        vy = random.uniform(-2, 2)  # Faixa de velocidades iniciais
        balls.append(Ball(x, y, raio, massa, cor, vx, vy))

    clock = pygame.time.Clock()
    
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE):
                rodando = False

        screen.fill(preto)

        for i in range(num_bolas):
            for j in range(i + 1, num_bolas):
                colisoes_bolas(balls[i], balls[j], coef_restituicao)

        for ball in balls:
            ball.mover_bola()
            colisoes_paredes(ball, screen_largura, screen_altura)
            ball.desenhar_bola(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
