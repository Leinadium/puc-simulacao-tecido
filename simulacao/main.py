from view import Visualizacao
from sim import CordaSimul


def main_teste():
    tam_corda = 10
    v = Visualizacao(
        tam_corda=tam_corda,
        fps=1.0
    )

    s = CordaSimul(
        tam_corda=1,
        tempo_passo=1.0/60.0,
        dist_minima=0.1
    )

    while True:
        s.proxima_avaliacao()
        v.atualizar(s.get_pontos())


if __name__ == "__main__":
    main_teste()
