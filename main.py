import pygame
import random
import os

pygame.init()

# 🖥️ TELA CHEIA
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
largura, altura = tela.get_size()

pygame.display.set_caption("Cobra PRO 🐍")

# 🎨 CORES
preto = (15, 15, 15)
verde = (0, 255, 0)
vermelho = (255, 70, 70)
branco = (240, 240, 240)
azul = (0, 170, 255)
cinza = (40, 40, 40)

fonte_titulo = pygame.font.SysFont("arial", 38, bold=True)
fonte = pygame.font.SysFont("arial", 24)

# 🏆 RECORDE
# No Android, a pasta de trabalho pode não ser gravável.
# Usamos a pasta de dados do próprio app (definida pelo android/SDL2),
# com fallback para a pasta atual quando corres no PC.
try:
    from android.storage import app_storage_path
    pasta_dados = app_storage_path()
except Exception:
    pasta_dados = os.path.dirname(os.path.abspath(__file__))

arquivo = os.path.join(pasta_dados, "highscore.txt")

if os.path.exists(arquivo):
    try:
        highscore = int(open(arquivo).read())
    except:
        highscore = 0
else:
    highscore = 0

# 🎮 ESTADOS
MENU = "menu"
JOGO = "jogo"
estado = MENU

# ⚙️ DIFICULDADE
velocidade_base = 10

# 🗺️ MAPA
mapa = "normal"

# 🐍 COBRA
cobra = [[100, 100]]
direcao = "DIREITA"

# 🍎 COMIDA
def nova_comida():
    return [
        random.randrange(1, largura // 10) * 10,
        random.randrange(1, altura // 10) * 10
    ]

comida = nova_comida()

# 📊 JOGO
pontos = 0
game_over = False
clock = pygame.time.Clock()
rodando = True

# 📱 SWIPE
start_x = 0
start_y = 0
swiping = False


# ⚡ VELOCIDADE POR DIFICULDADE
def velocidade():
    return velocidade_base + pontos // 2


# 🔁 RESET
def reset():
    global cobra, direcao, pontos, game_over, comida
    cobra = [[100, 100]]
    direcao = "DIREITA"
    pontos = 0
    game_over = False
    comida = nova_comida()


# 💾 RECORD
def salvar_recorde():
    global highscore
    if pontos > highscore:
        highscore = pontos
        try:
            open(arquivo, "w").write(str(highscore))
        except Exception:
            pass


# 🐍 MOVIMENTO
def movimento():
    global pontos, game_over, comida

    cabeca = cobra[0].copy()

    if direcao == "DIREITA":
        cabeca[0] += 10
    if direcao == "ESQUERDA":
        cabeca[0] -= 10
    if direcao == "CIMA":
        cabeca[1] -= 10
    if direcao == "BAIXO":
        cabeca[1] += 10

    cobra.insert(0, cabeca)

    # comer
    if cabeca == comida:
        pontos += 1
        comida = nova_comida()
    else:
        cobra.pop()

    # ♾️ MAPA NORMAL (infinito)
    if mapa == "normal":
        if cabeca[0] < 0:
            cabeca[0] = largura - 10
        if cabeca[0] >= largura:
            cabeca[0] = 0
        if cabeca[1] < 0:
            cabeca[1] = altura - 10
        if cabeca[1] >= altura:
            cabeca[1] = 0

    # 🧱 MAPA DIFÍCIL (paredes mortais)
    elif mapa == "dificil":
        if cabeca[0] < 0 or cabeca[0] >= largura or cabeca[1] < 0 or cabeca[1] >= altura:
            salvar_recorde()
            return True

    # 💥 corpo
    if cabeca in cobra[1:]:
        salvar_recorde()
        return True

    return False


# 🎮 BOTÃO MENU
def botao(txt, y, cor):
    rect = pygame.Rect(largura//2 - 150, y, 300, 60)
    pygame.draw.rect(tela, cor, rect, border_radius=12)
    tela.blit(fonte.render(txt, True, branco), (rect.x + 30, rect.y + 15))
    return rect


# 🎮 LOOP
while rodando:
    tela.fill(preto)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        # MENU
        if estado == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = event.pos

                # Fácil
                if 200 <= y <= 260:
                    velocidade_base = 8
                    mapa = "normal"
                    estado = JOGO
                    reset()

                # Médio
                if 280 <= y <= 340:
                    velocidade_base = 12
                    mapa = "normal"
                    estado = JOGO
                    reset()

                # Difícil
                if 360 <= y <= 420:
                    velocidade_base = 15
                    mapa = "dificil"
                    estado = JOGO
                    reset()

        # SWIPE
        elif estado == JOGO:
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_x, start_y = event.pos
                swiping = True

            if event.type == pygame.MOUSEBUTTONUP and swiping:
                end_x, end_y = event.pos
                dx = end_x - start_x
                dy = end_y - start_y

                if abs(dx) > abs(dy):
                    direcao = "DIREITA" if dx > 0 else "ESQUERDA"
                else:
                    direcao = "BAIXO" if dy > 0 else "CIMA"

                swiping = False

    # 🟦 MENU
    if estado == MENU:
        tela.blit(fonte_titulo.render("🐍 COBRA PRO", True, branco), (largura//2 - 120, 80))

        tela.blit(fonte.render("Escolhe a dificuldade:", True, azul), (largura//2 - 120, 140))

        botao("🟢 FÁCIL (infinito)", 200, (0, 180, 0))
        botao("🟡 MÉDIO", 280, (180, 180, 0))
        botao("🔴 DIFÍCIL (paredes)", 360, (180, 0, 0))

    # 🎮 JOGO
    else:

        if not game_over:
            game_over = movimento()

        # 🐍 cobra
        for p in cobra:
            pygame.draw.rect(tela, verde, (p[0], p[1], 10, 10))

        # 🍎 comida
        pygame.draw.rect(tela, vermelho, (comida[0], comida[1], 10, 10))

        # 📊 HUD
        tela.blit(fonte.render(f"Pontos: {pontos}", True, branco), (20, 20))
        tela.blit(fonte.render(f"Recorde: {highscore}", True, branco), (20, 50))
        tela.blit(fonte.render(f"Mapa: {mapa}", True, azul), (20, 80))

        # 💥 GAME OVER
        if game_over:
            tela.blit(fonte_titulo.render("GAME OVER", True, vermelho),
                      (largura//2 - 120, altura//2 - 60))

            tela.blit(fonte.render(f"Pontuação: {pontos}", True, branco),
                      (largura//2 - 100, altura//2))

            tela.blit(fonte.render("Toque para menu", True, branco),
                      (largura//2 - 90, altura//2 + 40))

            if pygame.mouse.get_pressed()[0]:
                estado = MENU

    pygame.display.update()
    clock.tick(velocidade())

pygame.quit()
