import re
import pdfplumber
from sqlalchemy.orm import Session
from app.models.tabela_disciplina import Model_Disciplina 


def is_valid_time(horario):
    return re.match(r"\d{2}h\d{2}-\d{2}h\d{2}", horario) is not None


def is_valid_entry(entry):
    return bool(entry.strip())


def processar_multiplos_dias(dia_semana, horario, nome_disciplina, professor, sala):
    dias = dia_semana.split()
    return [
        {"dia": dia, "horario": horario, "disciplina": nome_disciplina, "professor": professor, "sala": sala}
        for dia in dias
    ]


def extrair_dados_horarios(tables):
    horarios_extraidos = []
    for table in tables:
        if len(table) < 4:
            continue

        headers = table[2]
        ultimo_dia = None

        for row in table[4:]:
            horario = row[0]
            if not is_valid_time(horario):
                continue

            for i, dia_info in enumerate(row[1:], start=1):
                if dia_info and is_valid_entry(dia_info):
                    dia_semana = headers[i] if headers[i] is not None else ultimo_dia
                    if dia_semana:
                        ultimo_dia = dia_semana

                    disciplinas = dia_info.split("\n\n")
                    for disciplina in disciplinas:
                        detalhes = disciplina.split("\n")
                        if len(detalhes) >= 3:
                            nome_disciplina = " ".join(detalhes[:-2])
                            professor = detalhes[-2]
                            sala = detalhes[-1]

                            if "CANCELADA" in sala.upper():
                                continue

                            professor = professor.strip("()").strip()

                            if sala == "(Victor)":
                                sala = professor
                                professor = "Victor"

                            if professor in ["T) (Adriano", "P) (Adriano", "I (P) (Adriano"]:
                                professor = "Adriano"
                                nome_disciplina = "FACOM33403 - Programação para Web I"

                            if professor == "e Sociedade":
                                nome_disciplina = "FACOM33202 - ACE: Informática e Sociedade"
                                professor = "Daniel"
                                sala = "Não Informado"

                            if professor == "Popularização C&T":
                                nome_disciplina = "FACOM33503 - ACE: Popularização C&T"
                                professor = "Daniel"
                                sala = "Não Informado"

                            if " " in dia_semana:
                                horarios_extraidos.extend(
                                    processar_multiplos_dias(dia_semana, horario, nome_disciplina.strip(), professor.strip(), sala.strip())
                                )
                            else:
                                horarios_extraidos.append({
                                    "dia": dia_semana,
                                    "horario": horario,
                                    "disciplina": nome_disciplina.strip(),
                                    "professor": professor.strip(),
                                    "sala": sala.strip()
                                })
    return horarios_extraidos


def salvar_disciplinas_no_bd(db: Session):
    pdf_path = r"app/services/resources/horarios.pdf"
    dados_extraidos = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number in range(1, 9):
            page = pdf.pages[page_number]
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    dados_extraidos.extend(extrair_dados_horarios([table]))

    for dado in dados_extraidos:
        existente = db.query(Model_Disciplina).filter_by(
            nome=dado['disciplina'],
            dia_semana=dado['dia'],
            horario=dado['horario']
        ).first()

        if not existente:
            nova_disciplina = Model_Disciplina(
                dia_semana=dado['dia'],
                nome=dado['disciplina'],
                sala=dado['sala'],
                nome_prof=dado['professor'],
                horario=dado['horario']
            )
            db.add(nova_disciplina)

    db.commit()
    print("Disciplinas salvas no banco de dados com sucesso.")
