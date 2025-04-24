import requests
from bs4 import BeautifulSoup
import pandas as pd
from app.models.tabela_fichas import Model_Fichas


def obter_fichas():
    prefixos = ['GSI', 'FAMAT', 'FACOM', 'IEUFU', 'LIBRAS']
    disciplinas_por_periodo = {1: 5, 2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 4, 8: 2}
    dados = []
    contador = 0
    periodo_atual = 1
    resposta = requests.get('https://facom.ufu.br/graduacao/bsi-montecarmelo/fichas-de-disciplinas')
    soup = BeautifulSoup(resposta.text, 'html.parser')
    links = soup.find_all('a', href=True)

    for link in links:
        if contador >= 80:
            break

        codigo = link.get('title', '')
        href = link.get('href', '')

        if not codigo:  #Tratamento especial pra MCC
            codigo = href.split('/')[-1].split('-')[0] if href else ''
            if codigo.lower().startswith('famat'):
                codigo = 'FAMAT33205'

        if codigo and any(codigo.startswith(prefixo) for prefixo in prefixos):
            texto = link.get_text(strip=True)
            disciplina = texto.split('-', 1)[-1].strip() if '-' in texto else texto.strip()

            if periodo_atual <= 8:
                if contador < sum(disciplinas_por_periodo[p] for p in range(1, periodo_atual + 1)):
                    periodo = periodo_atual
                else:
                    periodo_atual += 1
                    periodo = periodo_atual
            else:
                periodo = 'Optativa'

            #Tratamento especial para a primeira disciplina optativa que por alguma razão que eu desconheço é reconhecida como sendo do "9° período" (que obviamente nem existe)
            if periodo == 9:
                periodo = 'Optativa'

            link_completo = f"https://facom.ufu.br{href}" if href.startswith('/') else href

            dados.append([periodo, codigo, disciplina, link_completo])
            contador += 1
    return dados
# df = pd.DataFrame(obter_fichas(), columns=['Período', 'Código', 'Disciplina', 'Link'])
# print(df)
# print(obter_fichas())

def salvar_fichas_no_bd(db: requests.Session):
    fichas = obter_fichas()

    for ficha in fichas:
        periodo, codigo, disciplina, link = ficha
        existente = db.query(Model_Fichas).filter_by(link=link).first()
        if not existente:
            nova_ficha = Model_Fichas(
                link=link,
                periodo=periodo,
                disciplina=disciplina,
                codigo=codigo,
            )
            db.add(nova_ficha)
    
    db.commit()


def obter_fichas_com_cache(db: requests.Session):
    ficha_existe = db.query(Model_Fichas).first()
    if not ficha_existe:
        salvar_fichas_no_bd(db)

    fichas = db.query(Model_Fichas).all()
    return [
        {
            "codigo": ficha.codigo,
            "periodo": ficha.periodo,
            "disciplina": ficha.disciplina,
            "link": ficha.link,
        } for ficha in fichas
    ]
