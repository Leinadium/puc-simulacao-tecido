from typing import List
import numpy as np

DEFAULT_FPS = 1.0 / 60.0


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


# class Bar:
#     particle1 = Particle(0, 0)
#     particle2 = Particle(1, 1)
#     length = 0
#
#     def __init__(self, particle1, particle2, length):
#         self.particle1 = particle1
#         self.particle2 = particle2
#         self.length = length
#
#     def relax(self, particle1, particle2):
#         pass

# def gera_barras(self):
#     barras = []
#     for i in range(len(self.pontos) - 2):
#         dist_perto = 1
#         dist_longe = 2
#         barra_perto = Bar(self.pontos[i], self.pontos[i + 1], dist_perto)
#         barra_longe = Bar(self.pontos[i], self.pontos[i + 2], dist_longe)
#         barras.append(barra_perto)
#         barras.append(barra_longe)
#     ultima_barra = Bar(self.pontos[-2], self.pontos[-1], 1)
#     barras.append(ultima_barra)
#     return barras

def _gera_pontos_iniciais(dist_minima: float, tam_corda: float) -> List[List[float]]:
    return [[0, tam_corda - dist_minima * i] for i in range(int(tam_corda / dist_minima))]


def _gera_pontos_iniciais2(dist_minima: float, tam_corda: float) -> List[Particle]:
    v0 = np.array([0.5, 0.5])
    particles: [Particle] = []
    for i in range(int(tam_corda / dist_minima)):
        previous_pos = np.array([0, tam_corda - dist_minima * i])
        current_pos = previous_pos + v0
        particles.append(Particle(previous_pos, current_pos))
    particles[0].is_fixed = True
    for p in particles:
        print(p.get_current_pos())
    return particles


def calcula_dist(point1, point2):
    return np.linalg.norm(point1 - point2)


def relax(point1: Particle, point2: Particle, close_flag):
    # close indica se é uma barra entre dois pontos a 1 barra de distancia (True) ou
    # se é uma barra "tracejada" (2 pontos de distância, valor de close = False)
    if close_flag:
        length = 1
    else:
        length = 2
    direction = np.subtract(point1.current_pos, point2.current_pos)
    distance = np.linalg.norm(direction)
    adjust = length - distance
    direction /= distance

    if not point1.is_fixed and not point2.is_fixed:
        point1.current_pos += (adjust/2) * direction
        point2.current_pos += (adjust/2) * (-direction)
    elif point1.is_fixed:
        point2.current_pos += adjust * direction
    elif point2.is_fixed:
        point1.current_pos += adjust * (-direction)


class CordaSimul:
    def __init__(self,
                 tam_corda: float,
                 tempo_passo: float = DEFAULT_FPS,
                 vento: float = None,
                 delta: float = None,
                 m: float = None, 
                 h: float = None,
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
        self.delta = delta
        self.m = m
        self.h = h
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
        delta = self.delta
        m = self.m
        h = self.h
        # TODO: implementar relaxação
        fg = np.array([0, -9.8])
        for i, p in enumerate(self.pontos):
            if p.is_fixed:
                continue
            previous_pos = p.previous_pos
            current_pos = p.current_pos
            next_pos = p.current_pos + (1 - delta) * (p.current_pos - previous_pos) + ((h * h) / m) * fg
            p.update_position(next_pos)

        for i in range(len(self.pontos) - 2):
            first = self.pontos[i]
            second = self.pontos[i + 1]
            third = self.pontos[i + 2]

            relax(first, second, True)
            relax(first, third, False)
        relax(self.pontos[-2], self.pontos[-1], True)
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
