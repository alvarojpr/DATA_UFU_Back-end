import bcrypt

senha_digitada = "1234"
hash_salvo = "$2b$12$.cuKZuqdJhSirLl0WbX49O7kmTQjENUb.vWsbYAZv.0YrGwEhll1a"

print(bcrypt.checkpw(senha_digitada.encode('utf-8'), hash_salvo.encode('utf-8')))


# import requests
# from bs4 import BeautifulSoup

# def obter_horarios_intercampi():
#     url = 'https://www.montecarmelo.mg.gov.br/transporte-publico'
#     response = requests.get(url)
#     html = response.text

#     soup = BeautifulSoup(html, 'html.parser')
#     titulos = soup.find_all('div', class_='linha50')

#     # Exemplo Excel: Horário - Parada
#     pontos_dict = {}

#     for titulo in titulos:
#         linhas = titulo.text.strip().splitlines()
#         for linha in linhas:
#             linha = linha.strip()
#             if '»' in linha:
#                 horario, parada = linha.split(' » ', 1)
#                 parada = parada.strip()
#                 horario = horario.strip()
#                 if parada not in pontos_dict:
#                     pontos_dict[parada] = []
#                 pontos_dict[parada].append(horario)

#     # Deixa no mesmo formato do transporte "municipal"
#     pontos_e_horarios = []
#     for parada, horarios in pontos_dict.items():
#         pontos_e_horarios.append({
#             "ponto": parada,
#             "horarios": horarios
#         })

#     return {
#         "transporte": "intercampi",
#         "Pontos_e_horarios": pontos_e_horarios
#     }

# # 🧪 Testando
# if __name__ == "__main__":
#     resultado = obter_horarios_intercampi()
#     from pprint import pprint
#     pprint(resultado)
