from datetime import datetime, timedelta
from routes import agendar

HORA_INICIO = "08:15"
# ultimo horario aceito: o servico precisa terminar antes das 18h
HORA_FIM = "17:20"
INTERVALO_MINUTOS = 45

ALMOCO_INICIO = "12:00"
ALMOCO_FIM = "13:00"

LIMITE_INICIO = datetime.strptime(HORA_INICIO, "%H:%M").time()
LIMITE_FIM = datetime.strptime(HORA_FIM, "%H:%M").time()
BLOQUEIO_ALMOCO_INICIO = datetime.strptime(ALMOCO_INICIO, "%H:%M").time()
BLOQUEIO_ALMOCO_FIM = datetime.strptime(ALMOCO_FIM, "%H:%M").time()

HORARIOS_PERMITIDOS = []

horario_atual = datetime.strptime(HORA_INICIO, "%H:%M")
horario_limite = datetime.strptime(HORA_FIM, "%H:%M")

while horario_atual <= horario_limite:
    # pula a faixa do almoco, quando a oficina esta fechada
    if BLOQUEIO_ALMOCO_INICIO <= horario_atual.time() < BLOQUEIO_ALMOCO_FIM:
        horario_atual += timedelta(minutes=INTERVALO_MINUTOS)
        continue

    HORARIOS_PERMITIDOS.append(horario_atual.strftime("%H:%M"))
    horario_atual += timedelta(minutes=INTERVALO_MINUTOS)


def validar_agendamento(data_str: str, hora_str: str) -> str | None:
    formatos_hora = ["%H:%M:%S", "%H:%M", "%H"]
    formato_data = "%Y-%m-%d"

    objeto_hora = None
    for fmt in formatos_hora:
        try:
            objeto_hora = datetime.strptime(hora_str, fmt).time()
            break
        except (ValueError, TypeError):
            continue

    if objeto_hora is None:
        return "Horário inválido."

    try:
        objeto_data = datetime.strptime(data_str, formato_data)
    except (ValueError, TypeError):
        return "Data inválida."

    data_hora_agendamento = datetime.combine(objeto_data, objeto_hora)

    if data_hora_agendamento <= datetime.now():
        return "Agendamento fora do prazo."

    if data_hora_agendamento.weekday() >= 5:
        return "Agendamento de segunda a sexta-feira."

    if not (LIMITE_INICIO <= objeto_hora <= LIMITE_FIM):
        return f"A oficina atende das {HORA_INICIO} às {HORA_FIM}."

    if BLOQUEIO_ALMOCO_INICIO <= objeto_hora < BLOQUEIO_ALMOCO_FIM:
        return f"Horário de almoço: das {ALMOCO_INICIO} às {ALMOCO_FIM} não há atendimento."

    return None

