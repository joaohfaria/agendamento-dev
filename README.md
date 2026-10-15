# Agendamento Online - Oficina SubSolo

Sistema web para clientes agendarem serviços sem precisar ligar ou ir até a oficina.

## O problema

Hoje o agendamento é feito por telefone e anotado manualmente. O cliente
não sabe quais horários estão livres, e a oficina perde tempo no telefone.

## Status

Em desenvolvimento. Projeto de estudo com uso real previsto.

- [x] Página inicial e formulário de agendamento (HTML)
- [x] Back-end recebendo o formulário (Python + Flask)
- [ ] Banco de dados (SQLite)
- [ ] Painel do funcionário

## Como rodar

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Acesse http://127.0.0.1:5000

## Tecnologias

HTML, CSS, Python, Flask, SQLite