from view import Visualizacao
from sim import CordaSimul


def main_teste():
    tam_corda = 4
    delta = 0.02
    dist_minima = 0.1
    m = [0.2 for i in range(int(tam_corda / dist_minima))]
    h = 0.05

    v = Visualizacao(
        tam_corda=20,
        fps=30.0
    )

    s = CordaSimul(
        tam_corda=tam_corda,
        tempo_passo=1.0 / 60.0,
        delta=delta,
        m=m,
        h=h,
        dist_minima=dist_minima
    )

    while True:
        s.proxima_avaliacao()
        v.atualizar(s.get_pontos())


if __name__ == "__main__":
    main_teste()
