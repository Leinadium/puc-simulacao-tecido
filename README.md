# Animação de Tecido baseada em Física

Repositório do trabalho final de INF1608 - Análise Numérica, da PUC-Rio.

## Autores
* Daniel Guimarães
* Mariana Barreto
* Mateus Levi

## Setup

É recomendado que se utilize um ambiente virtual para a instalação das bibliotecas em python.

Para isso, é possível utilizar o ```virtualenv / venv``` ou o ```conda``` . Usando o ```venv``` :

```bash
# instalando
python3 -m venv venv    # linux
python -m venv venv     # windows

# ativando
source venv/bin/activate    # linux
venv\Scripts\activate       # windows

# desativando
deactivate  
```

Após ativar o ambiente virtual, instale as bibliotecas necessárias para o projeto:

```bash
pip3 install -r requirements.txt    # linux
python install -r requirements.txt  # windows
```

Para executar o programa, execute o script ```simulacao/main.py```

