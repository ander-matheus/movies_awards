## README - Golden Raspberry Awards API

### Para que serve esse repositório?

- API RESTful para possibilitar a leitura da lista de indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards.
- Version: 1.0.0

### Pré-requisitos

- Python 3.13 ou superior.
- pip (gerenciador de pacotes).
- (Recomendado) virtualenv para isolamento do ambiente.

### Como rodar o projeto

1. Clone o repositório
   > git clone https://github.com/ander-matheus/movies_awards.git
1. Crie o ambiente virtual (recomendado)
   > python -m venv venv
1. Ative o ambiente virtual (recomendado)
   > No windows: venv\Scripts\activate ou MacOS/Linux: source venv/bin/activate
1. Instale as dependências do projeto
   > pip install -r requirements.txt
1. Rode as migrações
   > python manage.py migrate
1. Rode os testes (recomendado):
   > python manage.py test
1. Inicie o projeto
   > python manage.py runserver
1. Acesse o projeto em [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
1. Se você ver a tela abaixo, está tudo certo! :)

<img src="https://github.com/ander-matheus/movies_awards/blob/main/Golden-Raspberry-Awards-API.png" alt="home print">
