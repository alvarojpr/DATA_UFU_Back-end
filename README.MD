# DATAUFU - Backend

Este repositório contém o backend da aplicação **DATAUFU**, desenvolvido em **FastAPI**, como parte da disciplina _Projeto e Desenvolvimento de Sistemas de Informação_ (PDSI) no curso de Sistemas de Informação da UFU.

A proposta do projeto é integrar e disponibilizar **informações úteis para alunos da UFU**, como:

- Horários de ônibus
- Grade horária das disciplinas
- Editais e comunicados

O projeto possui meios para:
- Envio de feedbacks
- Fazer login e autenticação
- Teste automatizados
- Esconder credenciais
- Validação de dados
- Integração com banco de dados relacional

---

## 🔧 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) para ORM
- [PostgreSQL](https://www.postgresql.org/) (ou outro banco relacional)
- [Uvicorn](https://www.uvicorn.org/) como servidor ASGI
- [Pydantic](https://docs.pydantic.dev/) para validação de dados
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) para web scrapping
- [PyPDF2](https://pypdf2.readthedocs.io/en/3.x/) para pdf scrapping

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- Python 3.10+
- Git
- Banco de dados PostgreSQL (ou configurar outro no `.env`)

### Passo a passo:

```bash
# 1. Clone o repositório
git clone https://github.com/alvarojpr/back_end_pdsi2.git
cd back_end_pdsi2

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente (exemplo abaixo)
# Crie um arquivo .env na raiz com o seguinte conteúdo:
# ----------------------------------
# DATABASE_URL=postgresql://usuario:senha@localhost:5432/dataufu
# SECRET_KEY=sua_chave_ultra_secreta
# ----------------------------------

# 5. Execute a aplicação
uvicorn main:app --reload
A API estará disponível em: http://localhost:8000

Documentação automática:
Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc

Estrutura do projeto:
back_end_pdsi2/
├── app/                     # Módulo principal da aplicação
│   ├── models/              # Modelos ORM (tabelas do banco de dados)
│   ├── schemas/             # Schemas do Pydantic (validação de dados)
│   ├── routes/              # Rotas/Endpoints da API
│   ├── services/            # Regras de negócio e lógica da aplicação
│
├── venv/                    # Ambiente virtual com dependências Python
├── .env                     # Variáveis de ambiente (não versionado)
├── .gitignore               # Arquivos/pastas ignoradas pelo Git
├── database.py              # Configuração e conexão com o banco de dados
├── main.py                  # Arquivo principal da aplicação FastAPI
├── requirements.txt         # Lista de dependências do projeto
├── teste.py                 # Script de testes manuais para rotas
└── README.md                # Documentação do projeto


SOBRE:
Projeto acadêmico desenvolvido pelos alunos da Universidade Federal de Uberlândia (UFU) Álvaro José, Edilson Filho, Eduardo Alvim, Gabriel Gama e Waldemar Flores para a disciplina de PDSI. Tem como objetivo centralizar informações relevantes para os estudantes do curso de Sistemas de Informação.
