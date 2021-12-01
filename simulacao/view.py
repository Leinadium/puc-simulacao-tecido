import pygame
import pygame.freetype
from time import perf_counter

from typing import List

TAMANHO_TELA = COMPRIMENTO_TELA, ALTURA_TELA = (800, 600)
COR_PRETO = (0, 0, 0)
COR_BRANCO = (255, 255, 255)


def coods_to_abs(tam_corda):
    """
    Coordenadas são relativas a uma corda pendurada no eixo y
    Coordenadas absolutas são as coordenadas para o pygame
    :return:
    """
    return lambda c: [
        COMPRIMENTO_TELA / 2.0 * (1 + c[0] / tam_corda),
        ALTURA_TELA * (1 - 0.8 * c[1] / tam_corda)
    ]


class Visualizacao:
    def __init__(self, tam_corda: float, fps: float = 60.0):
        """
        Inicia um objeto de Visualização
        :param tam_corda: tamanho da corda
        :param fps: FPS da simulação
        """
        # inicia o pygame
        if not pygame.get_init():
            pygame.init()

        self.screen = pygame.display.set_mode(TAMANHO_TELA)
        self.tempo = 0
        self.tam_corda = tam_corda
        self.fps_simulacao = fps
        self.fonte = pygame.freetype.SysFont("Arial", 14, bold=True, italic=False)
        self.conversor = coods_to_abs(self.tam_corda)
        pygame.display.set_caption("Visualizacao")

        return

    @classmethod
    def _fechar(cls):
        pygame.quit()

    @classmethod
    def _checa_eventos(cls):
        """
        Interacao com a interface grafica
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cls._fechar()
                exit(0)

    def atualizar(self, pontos: List[List[int]]):
        """
        Recebe os pontos, e atualiza o desenho
        os pontos são uma lista de tuplas, em que cada tupla contem o x e y;
        """

        tempo_decorrido = perf_counter() - self.tempo
        fps_decorrido = 1 / tempo_decorrido if tempo_decorrido > 0 else 999

        textos = [
            f"FPS simulado: {self.fps_simulacao}",
            f"FPS real: {fps_decorrido}"
        ]

        # limpa a tela
        self.screen.fill(COR_PRETO)

        # escreve os textos
        for i, texto in enumerate(textos):
            t, rect = self.fonte.render(texto, fgcolor=COR_BRANCO)
            rect.x, rect.y = 10, 10 + 30 * i
            self.screen.blit(t, rect)

        # desenha a corda
        pontos_abs = list(map(self.conversor, pontos))
        pygame.draw.lines(self.screen, COR_BRANCO, closed=False, points=pontos_abs)

        # desenha a tela
        pygame.display.flip()

        while perf_counter() - self.tempo < 1 / self.fps_simulacao:
            type(self)._checa_eventos()

        # atualiza o tempo
        self.tempo = perf_counter()
        return
