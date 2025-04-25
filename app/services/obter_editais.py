import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import date
from sqlalchemy.orm import Session
from app.models.tabela_editais import Model_Edital

def editais_ufu():
    # Obtém o ano atual para comparar com a data dos editais e transforma em String
    data_atual = date.today()
    ano_atual = '{}'.format(data_atual.year)

    # Inicializa variáveis de controle
    id_pag = 0  # Página inicial
    QTD_MAX = 20  # Última página
    continuar = True  # Variável que indica se devemos continuar a busca

    # Lista que vai armazenar todos os dados de editais coletados
    editais_data = []

    # Laço que percorre as páginas de editais enquanto a quantidade de páginas for menor que QTD_MAX e devemos continuar
    while (id_pag < QTD_MAX and continuar):
        # Formata a URL da página de editais com o número da página atual
        url = f"http://www.editais.ufu.br/discente?page={id_pag}&order=field_data_publicacao_value&sort=desc"

        # Faz uma requisição HTTP para obter o conteúdo da página
        response = requests.get(url)

        # Verifica se a requisição foi bem-sucedida (status 200)
        if response.status_code == 200:
            # Analisa o conteúdo da página HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontra todos os blocos de editais (linhas da tabela de editais)
            edital_blocks = soup.find_all('tr')

            # Itera sobre cada edital encontrado na página
            for edital in edital_blocks:
                numero_edital = edital.find('td', class_='views-field-field-nro-value')
                numero_edital = numero_edital.get_text(strip=True) if numero_edital else 'N/A'

                orgao_responsavel = edital.find('td', class_='views-field-field-setor-responsavel-value')
                orgao_responsavel = orgao_responsavel.get_text(strip=True) if orgao_responsavel else 'N/A'

                titulo = edital.find('td', class_='views-field-title')
                titulo_text = titulo.get_text(strip=True) if titulo else 'N/A'

                link_edital = None
                if titulo:
                    a_tag = titulo.find('a', href=True)  # Encontra a tag que contém o link
                    if a_tag:
                        # Cria a URL completa do edital usando urljoin
                        link_edital = urljoin(url, a_tag['href'])

                tipo = edital.find('td', class_='views-field-field-tipo-value')
                tipo = tipo.get_text(strip=True) if tipo else 'N/A'

                data_publicacao = edital.find('td', class_='views-field-field-data-publicacao-value')
                data_publicacao = data_publicacao.get_text(strip=True) if data_publicacao else 'N/A'

                # Extrai o ano da data de publicação
                ano_edital = '{}'.format(data_publicacao[4:9].strip())
                # Se qualquer uma dessas informações estiver disponível, cria um dicionário com os dados do edital
                if numero_edital != 'N/A' or orgao_responsavel != 'N/A' or titulo_text != 'N/A' or tipo != 'N/A' or data_publicacao != 'N/A' or link_edital:
                    edital_info = {
                        'numero_edital': numero_edital,
                        'orgao_responsavel': orgao_responsavel,
                        'titulo': titulo_text,
                        'tipo': tipo,
                        'data_publicacao': data_publicacao,
                        'link': link_edital
                    }
                    if(ano_edital == ano_atual):
                        editais_data.append(edital_info)
            # Se o ano do edital não for o ano atual, interrompe a busca
            if(ano_edital < ano_atual):
                continuar = False

        else:
            # Exibe uma mensagem de erro se a página não for acessada com sucesso
            print(f"Erro ao acessar a página. Status code: {response.status_code}")
            break

        # Incrementa o número da página para acessar a próxima
        id_pag += 1

    return editais_data


def salvar_editais_no_bd(db: Session):
    editais = editais_ufu()

    for edital in editais:
        existente = db.query(Model_Edital).filter_by(link=edital['link']).first()
        if not existente:
            novo_edital = Model_Edital(
                link=edital['link'],
                orgao_responsavel=edital['orgao_responsavel'],
                titulo=edital['titulo'],
                tipo=edital['tipo'],
                data=edital['data_publicacao'],
                num_edital=edital['numero_edital']
            )
            db.add(novo_edital)
    db.commit()

def obter_editais_db(db: Session):
    editais = db.query(Model_Edital).all()
    return [
        {
            "link": edital.link,
            "orgao_responsavel": edital.orgao_responsavel,
            "titulo": edital.titulo,
            "tipo": edital.tipo,
            "data": edital.data,
            "num_edital": edital.num_edital
        } for edital in editais
    ]
