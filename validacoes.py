from datetime import datetime

HORA_INICIO = datetime.strptime("08:15", "%H:%M").time()
# ultimo horario aceito: o servico precisa terminar antes das 18h
HORA_FIM = datetime.strptime("17:20", "%H:%M").time()

def validar_agendamento(data_str: str, hora_str: str) -> str:
    formatos_hora = ["%H:%M:%S", "%H:%M", "%H"]
    formato_data = "%Y-%m-%d" 
    
    objeto_hora = None
    for fmt in formatos_hora:
        try:
            objeto_hora = datetime.strptime(hora_str, fmt).time()
            break
        except ValueError:
            continue

    if not objeto_hora:
        return ("Horario inválido.")

    try:
        objeto_data = datetime.strptime(data_str, formato_data)
    except ValueError:
        return ("Data inválida.")
    data_hora_agendamento = datetime.combine(objeto_data, objeto_hora)

    agora_servidor = datetime.now()
    if data_hora_agendamento <= agora_servidor:
        return ("Agendamento fora do prazo.")

    dia_semana = data_hora_agendamento.weekday()
    if dia_semana >= 5:
        return ("Agendamento de segunda a sexta-feira.")

    if not (HORA_INICIO <= objeto_hora <= HORA_FIM):
        return ("Horário fora do intervalo permitido.")

    

    return None
