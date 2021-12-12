from typing import List, Tuple, Any
import numpy as np

DEFAULT_FPS = 1.0 / 60.0


# Gera uma instância de partícula. Guarda a posição anterior da partícula, posição atual e um booleano indicando
# se a partícula está fixa ou não, além da massa da partícula.
# Elementos de posição são do tipo numpy.array (facilita operações vetoriais).
class Particle:
    previous_pos = np.array([])
    current_pos = np.array([])
    mass = 0
    is_fixed = False

    def __init__(self, previous_pos, current_pos, mass, is_fixed=False):
        self.previous_pos = previous_pos
        self.current_pos = current_pos
        self.mass = mass
        self.is_fixed = is_fixed

    # Atualiza posição atual da partícula e move posição atual (antiga) para ficar guardada na posição anterior.
    def update_position(self, new_position):
        self.previous_pos = self.current_pos
        self.current_pos = new_position

    def get_current_pos(self):
        return self.current_pos


# A classe Bar representa uma barra conectando quaisquer duas partículas.
# Serve para guardar a distância original entre elas e permitir o relaxamento
# de suas posições na simulação.
class Bar:
    def __init__(self, particle1: Particle, particle2: Particle, length: float):
        self.particle1 = particle1
        self.particle2 = particle2
        self.length = length

    # Aplica o relaxamento das partículas conectadas pela barra.
    def relax(self):
        p1 = self.particle1
        p2 = self.particle2
        direction = np.subtract(p1.get_current_pos(), p2.get_current_pos())
        distance = np.linalg.norm(direction)
        adjust = self.length - distance
        direction /= distance

        if not p1.is_fixed and not p2.is_fixed:
            p1.current_pos += (adjust / 2) * direction
            p2.current_pos += (adjust / 2) * (-direction)
        elif not p1.is_fixed:
            p1.current_pos += adjust * direction
        elif not p2.is_fixed:
            p2.current_pos += adjust * (-direction)


# Gera barras adjacentes e imaginárias (1 passo a mais além da adjacente)
# entre partículas passadas em uma lista no parâmetro "pontos".
def gera_barras(pontos: [Particle], n_adj: int) -> [Bar]:
    barras = []
    for i in range(len(pontos) - 1):
        count = 0
        p1 = pontos[i]
        p2 = pontos[i + 1]
        dist = calcula_dist(p1.get_current_pos(), p2.get_current_pos())
        barra_perto = Bar(p1, p2, dist)
        barras.insert(0, barra_perto)
        count += 1
        # max_lim = len(pontos)
        max_lim = min(len(pontos), i + 1 + n_adj)
        # com max_lim = i+8, cada particula faz a barra adjacente
        # e no até 6 barras imaginárias = 7 barras no total (para particulas que tem
        # 7 partículas depois dela na corda, é claro)
        for j in range(i + 2, max_lim):
            paux = pontos[j]
            aux_dist = calcula_dist(p1.get_current_pos(), paux.get_current_pos())
            aux_bar = Bar(p1, paux, aux_dist)
            barras.append(aux_bar)
            count += 1
    return barras


# Gera partículas e barras a partir de um tamanho de corda, uma distância mínima entre partículas
# e parâmetros h e lista de massas das partículas.
def _gera_pontos_iniciais(dist_minima: float, tam_corda: float, h: float, m: [float], n_adj: int) \
        -> tuple[list[Particle], list[Bar]]:
    particles: [Particle] = []
    distances: [float] = []
    barras: [Bar] = []
    v0 = np.array([0, 0])

    # Criando partículas
    for i in range(int(tam_corda / dist_minima)):
        previous_pos = np.array([dist_minima * i, 10 + tam_corda - dist_minima * i])
        particles.append(Particle(previous_pos, previous_pos, m[i]))
    particles[0].is_fixed = True

    # Gerando barras
    # e dando passo inicial
    barras = gera_barras(particles, n_adj)
    for i in range(len(particles) - 1):
        if not particles[i].is_fixed:
            current_pos = particles[i].previous_pos + h * v0
            particles[i].update_position(current_pos)
    # Dando passo inicial na última partícula
    current_pos = particles[-1].previous_pos + h * v0
    particles[-1].update_position(current_pos)

    for i in range(len(barras)):
        barras[i].relax()

    return particles, barras


# Calcula distância entre duas coordenadas x-y.
def calcula_dist(point1, point2):
    diff = np.subtract(point1, point2)
    return np.linalg.norm(diff)


class CordaSimul:
    def __init__(self,
                 tam_corda: float,
                 tempo_passo: float = DEFAULT_FPS,
                 vento: float = None,
                 delta: float = None,
                 m: [float] = None,
                 h: float = None,
                 dist_minima: float = None,
                 pontos: List[Particle] = None,
                 barras: List[Bar] = None,
                 n_adjacencias_por_particula=7
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
        self.n_adjacencias = n_adjacencias_por_particula
        if dist_minima is not None:
            self.dist_minima = dist_minima
            self.pontos, self.barras = _gera_pontos_iniciais(dist_minima, tam_corda, self.h, self.m, self.n_adjacencias)
        elif pontos is not None and barras is not None:
            self.pontos = pontos
            self.barras = barras
            self.dist_minima = None
        else:
            print("especifique dist_minima ou pontos")
            exit(0)
        print("NUMERO DE PARTICULAS:", len(self.pontos))
        print("NUMERO DE BARRAS (RELAXACOES POR ITERAÇÃO):", len(self.barras))
        return

    def proxima_avaliacao(self):
        delta = self.delta
        m = self.m
        h = self.h
        count = 0
        fg = np.array([0, -9.8])
        for i, p in enumerate(self.pontos):
            if p.is_fixed:
                continue
            previous_pos = p.previous_pos
            current_pos = p.current_pos
            next_pos = p.current_pos + (1 - delta) * (p.current_pos - previous_pos) + ((h * h) / p.mass) * fg
            p.update_position(next_pos)

        for i in range(len(self.barras)):
            self.barras[i].relax()
            count += 1

        return

    def get_pontos(self):
        # Converte posições das partículas de numpy.array para listas e lista de posições atuais/correntes
        # de todas as partículas.
        converted_pontos = []
        for point in self.pontos:
            converted_position = point.get_current_pos().tolist()
            # print(converted_position)
            converted_pontos.append(converted_position)
        return converted_pontos
