from typing import List

DEFAULT_FPS = 1.0 / 60


def _gera_pontos_iniciais(dist_minima: float, tam_corda: float) -> List[List[float]]:
    return [[0, tam_corda - dist_minima * i] for i in range(int(tam_corda / dist_minima))]


class CordaSimul:
    def __init__(self,
                 tam_corda: float,
                 tempo_passo: float = DEFAULT_FPS,
                 vento: float = None,
                 dist_minima: float = None,
                 pontos: List[List[float]] = None
                 ):
        """
        Inicia um objeto de simulacao
        :param tam_corda: tamanho da corda, em metros
        :param tempo_passo: tempo, em fraçao de segundos, do passo.
                default -> 1 / 60 = 60 FPS
        :param vento: força do vento, em Newtons. Opcional.
                O sinal da força (positivo ou negativo) aponta pra direção em relação ao eixo x.
        :param dist_minima: distancia entre os pontos.
                se for None, sera usado a os pontos passados em ```pontos```.
        :param pontos: lista contendo os pontos da corda da simulacao.
                default -> gerado por _gera_pontos_iniciais(
        :param
        """
        self.tam_corda = tam_corda
        self.tempo_passo = tempo_passo
        if dist_minima is not None:
            self.dist_minima = dist_minima
            self.pontos = _gera_pontos_iniciais(dist_minima, tam_corda)
        elif pontos is not None:
            self.pontos = pontos
            self.dist_minima = None
        else:
            print("especifique dist_minima ou pontos")
            exit(0)
        return

    def proxima_avaliacao(self):
        # TODO: avaliacao verdadeira

        # EXEMPLO
        from random import uniform
        for i, p in enumerate(self.pontos):
            anterior = self.pontos[i - 1] if i > 0 else p
            if self.dist_minima is None:
                dist_x = abs(anterior[0] - p[0])
                # dist_y = abs(anterior[1] - p[1])
            else:
                dist_x = self.dist_minima

            p[0] = anterior[0] + dist_x * (1 if uniform(0, 1) >= 0.5 else -1)
        return

    def get_pontos(self):
        return self.pontos
