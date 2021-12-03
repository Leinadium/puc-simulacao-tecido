from typing import List
import numpy as np

DEFAULT_FPS = 1.0 / 60


# Gera uma instância de partícula. Guarda a posição anterior da partícula, posição atual e um booleano indicando
# se a partícula está fixa ou não.
# Elementos de posição são do tipo numpy.array (facilita operações vetoriais).
class Particle:
    previous_pos = np.array([])
    current_pos = np.array([])
    is_fixed = False

    def __init__(self, previous_pos, current_pos, is_fixed=False):
        self.previous_pos = previous_pos
        self.current_pos = current_pos
        self.is_fixed = is_fixed

    def update_position(self, new_position):
        self.previous_pos = self.current_pos
        self.current_pos = new_position

    def get_current_pos(self):
        return self.current_pos


def _gera_pontos_iniciais(dist_minima: float, tam_corda: float) -> List[List[float]]:
    return [[0, tam_corda - dist_minima * i] for i in range(int(tam_corda / dist_minima))]


def _gera_pontos_iniciais2(dist_minima: float, tam_corda: float) -> List[Particle]:
    v0 = np.array([0.5, 0.5])
    particles = []
    # TODO: mark one of the particles as fixed
    for i in range(int(tam_corda / dist_minima)):
        previous_pos = np.array([0, tam_corda - dist_minima * i])
        current_pos = previous_pos + v0
        particles.append(Particle(previous_pos, current_pos))
    return particles


class CordaSimul:
    def __init__(self,
                 tam_corda: float,
                 tempo_passo: float = DEFAULT_FPS,
                 vento: float = None,
                 dist_minima: float = None,
                 pontos: List[Particle] = None
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
            self.pontos = _gera_pontos_iniciais2(dist_minima, tam_corda)
        elif pontos is not None:
            self.pontos = pontos
            self.dist_minima = None
        else:
            print("especifique dist_minima ou pontos")
            exit(0)
        return

    def proxima_avaliacao(self):
        # TODO: implementar relaxação
        # TODO: passar delta, m e h como parâmetros talvez
        delta = 0.02
        m = 0.2
        h = 0.05
        fg = np.array([0, -9.8])
        for i, p in enumerate(self.pontos):
            if p.is_fixed:
                continue
            previous_pos = p.previous_pos
            current_pos = p.current_pos
            next_pos = p.current_pos + (1 - delta) * (p.current_pos - previous_pos) + ((h * h) / m) * fg
            p.update_position(next_pos)
        return

    def get_pontos(self):
        # Converte posições das partículas de numpy.array para listas e lista de posições atuais/correntes
        # de todas as partículas.
        converted_pontos = []
        for point in self.pontos:
            converted_position = point.get_current_pos().tolist()
            print(converted_position)
            converted_pontos.append(converted_position)
        return converted_pontos
