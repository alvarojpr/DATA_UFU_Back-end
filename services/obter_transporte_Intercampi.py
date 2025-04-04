import requests
from bs4 import BeautifulSoup

def obter_horarios_intercampi():
    url = 'https://www.montecarmelo.mg.gov.br/transporte-publico'
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    titulos = soup.find_all('div', class_='linha50')
    
    pontos_dict = {}

    for titulo in titulos:
        linhas = titulo.text.strip().splitlines()
        for linha in linhas:
            linha = linha.strip()
            if '»' in linha:
                horario, parada = linha.split(' » ', 1)
                parada = parada.strip()
                horario = horario.strip()
                if parada not in pontos_dict:
                    pontos_dict[parada] = []
                pontos_dict[parada].append(horario)

    pontos_e_horarios = []
    for parada, horarios in pontos_dict.items():
        pontos_e_horarios.append({
            "ponto": parada,
            "horarios": horarios
        })

    return {
        "transporte": "intercampi",
        "Pontos_e_horarios": pontos_e_horarios
    }
