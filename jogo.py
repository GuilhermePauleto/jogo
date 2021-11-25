import pygame
import time
import random
pygame.init()
largura = 900
altura = 700
configTela = (largura, altura)
gameDisplay = pygame.display.set_mode(configTela)
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
pygame.display.set_caption("Flash ")
icone = pygame.image.load("assets/flashIcone.jpg")
pygame.display.set_icon(icone)
flash = pygame.image.load("assets/flash.png")
larguraflash = 70
fundo = pygame.image.load("assets/cidade.jpg")
missel = pygame.image.load("assets/missile.png")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
misselSound = pygame.mixer.Sound("assets/missil.wav")
misselSound.set_volume(0.2)
def mostraflash(x, y):
    gameDisplay.blit(flash, (x, y))
def mostraMissel(x, y):
    gameDisplay.blit(missel, (x, y))
def text_objects(texto, font):
    textSurface = font.render(texto, True, black)
    return textSurface, textSurface.get_rect()
def escreverTela(texto):
    fonte = pygame.font.Font("freesansbold.ttf", 115)
    TextSurf, TextRect = text_objects(texto, fonte)
    TextRect.center = ((largura/2, altura/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(5)
    game()
def escreverPlacar(contador):
    fonte = pygame.font.SysFont(None, 30)
    texto = fonte.render("Desvios:"+str(contador), True, black)
    gameDisplay.blit(texto, (10, 10))
def dead():
    pygame.mixer.Sound.play(explosaoSound)
    pygame.mixer.music.stop()
    escreverTela("Você Morreu!")
def game():
    pygame.mixer.music.load("assets/lutasound.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    flashPosicaoX = largura*0.42
    flashPosicaoY = altura*0.76
    movimentoX = 0
    velocidade = 20
    misselAltura = 250
    misselLargura = 50
    misselVelocidade = 3
    misselX = random.randrange(0, largura)
    misselY = -200
    desvios = 0
    pygame.mixer.Sound.play(misselSound)
    while True:
        # pega as ações da tela. Ex.: fechar, click de uma tecla ou do mouse
        acoes = pygame.event.get()  # devolve uma lista de ações
        # [ini] mapeando as ações
        for acao in acoes:
            if acao.type == pygame.QUIT:
                pygame.quit()
                quit()
            if acao.type == pygame.KEYDOWN:
                if acao.key == pygame.K_LEFT:
                    movimentoX = velocidade*-1
                elif acao.key == pygame.K_RIGHT:
                    movimentoX = velocidade
            if acao.type == pygame.KEYUP:
                movimentoX = 0
        # [end] mapeando as ações
        # definindo o fundo do game
        gameDisplay.fill(white)
        gameDisplay.blit(fundo, (0, 0))
        # definindo o fundo do game]
        escreverPlacar(desvios)
        misselY = misselY + misselVelocidade
        mostraMissel(misselX, misselY)
        if misselY > altura:
            misselY = -200
            misselX = random.randrange(0, largura)
            desvios = desvios+1
            misselVelocidade += 3
            pygame.mixer.Sound.play(misselSound)
        flashPosicaoX += movimentoX
        if flashPosicaoX < 0:
            flashPosicaoX = 0
        elif flashPosicaoX > largura-larguraflash:
            flashPosicaoX = largura-larguraflash
        # analise de colisão com o flash
        if flashPosicaoY < misselY + misselAltura:
            if flashPosicaoX < misselX and flashPosicaoX+larguraflash > misselX or misselX+misselLargura > flashPosicaoX and misselX+misselLargura < flashPosicaoX+larguraflash:
                dead()
        # analise de colisão com o flash
        mostraflash(flashPosicaoX, flashPosicaoY)
        pygame.display.update()
        clock.tick(60)  # faz com que o while execute 60x por segundo
game()