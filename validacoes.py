from datetime import datetime

def validar_data(data, hora):

    formato = "%Y-%m-%d %H:%M"
    validar_data = datetime.strptime(f"{data} {hora}", formato)
    agora = datetime.now()

    if validar_data < agora:
        return False
    return True
