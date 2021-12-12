from view import Visualizacao
from sim import CordaSimul

def main_teste():

    delta = 0.02
    m = 0.2
    h = 0.05


    tam_corda = 10
    v = Visualizacao(
        tam_corda=tam_corda,
        fps=30.0
    )

    s = CordaSimul(
        tam_corda=2,
        tempo_passo=1.0/60.0,
        delta=delta,
        m=m,
        h=h,
        dist_minima=0.1
    )

    while True:
        s.proxima_avaliacao()
        v.atualizar(s.get_pontos())


if __name__ == "__main__":
    main_teste()
