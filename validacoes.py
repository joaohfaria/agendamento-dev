from datetime import datetime

def data_valida(data, hora):
    try:
        formato = "%Y-%m-%d %H:%M"
        agendando = datetime.strptime(f"{data} {hora}", formato)
        agora = datetime.now()

        if agendando < agora:
            return False
        return True
    except ValueError:
        return False
