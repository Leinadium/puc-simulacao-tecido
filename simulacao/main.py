from view import Visualizacao
from sim import CordaSimul


def main_teste():
    tam_corda = 4
    delta = 0.02
    dist_minima = 0.1
    m = [0.2 for i in range(int(tam_corda / dist_minima))]
    h = 0.05
    fps = 60

    v = Visualizacao(
        tam_corda=15,
        fps=fps
    )

    s = CordaSimul(
        tam_corda=tam_corda,
        tempo_passo=1 / fps,
        delta=delta,
        m=m,
        h=h,
        dist_minima=dist_minima,
        n_adjacencias_por_particula=7
    )

    while True:
        s.proxima_avaliacao()
        v.atualizar(s.get_pontos())


if __name__ == "__main__":
    main_teste()
