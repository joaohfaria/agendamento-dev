# Agendamento Online - Oficina SubSolo

Sistema web para clientes agendarem serviços sem precisar ligar ou ir até a oficina.

## O problema

Hoje o agendamento é feito por telefone e anotado manualmente. O cliente não
sabe quais horários estão livres, e a oficina perde tempo ao telefone. Este
sistema permite que o cliente escolha data e horário pelo site, e que a oficina
veja todos os agendamentos numa única lista.

## Funcionalidades

- Formulário de agendamento com nome, e-mail, telefone, placa, serviço, data e hora
- Agendamentos salvos em banco de dados SQLite
- Página de listagem dos agendamentos, ordenada por data e horário

## Páginas

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Página inicial com o formulário de agendamento |
| `/agendar` | POST | Recebe o formulário e grava o agendamento |
| `/agendamentos` | GET | Lista todos os agendamentos |

## Tecnologias

Python, Flask, SQLite, HTML

## Como rodar

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python database.py
python main.py
```

Acesse http://127.0.0.1:5000

O `database.py` cria o arquivo do banco e a tabela. Só precisa ser executado na
primeira vez.

## Status

Em desenvolvimento. Projeto de estudo com uso real previsto na oficina.

- [x] Página inicial e formulário de agendamento
- [x] Back-end recebendo o formulário (Flask)
- [x] Banco de dados (SQLite)
- [ ] Validação: impedir data no passado e horário já ocupado
- [ ] Login do funcionário
- [ ] Deploy

## Ideias futuras

- Lembrete automático para o cliente (e-mail ou WhatsApp) um dia antes do agendamento

## Tecnologias

HTML, CSS, Python, Flask, SQLite