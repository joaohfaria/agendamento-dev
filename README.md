# Agendamento SubSolo

Sistema web de agendamento para oficina mecânica. O cliente escolhe o horário pelo celular, sem telefonar; o funcionário acompanha a agenda e atualiza o status de cada serviço.

**Site no ar:** https://agendamento-subsolo.onrender.com

> Hospedado em planos gratuitos: o serviço web dorme depois de um tempo sem acesso e o banco de dados hiberna quando ocioso. A primeira visita depois de um período parado pode levar cerca de um minuto para carregar.

---

## Telas

| Agendamento (cliente) | Painel (funcionário) |
| --- | --- |
| ![Formulário de agendamento](docs/tela-agendamento.png) | ![Painel de agendamentos](docs/tela-painel.png) |

---

## Funcionalidades

- Formulário público de agendamento com nome, e-mail, telefone, placa, data, horário e serviço
- Horários gerados automaticamente em intervalos de 45 minutos, das 08:15 às 17:20
- Agendamento recusado quando a data já passou, cai em fim de semana ou no horário de almoço (12:00 às 13:00)
- Horário já ocupado não pode ser marcado por outro cliente
- Serviço precisa existir no cadastro do banco
- Em caso de erro, a mensagem aparece na própria página e os dados digitados são preservados
- Confirmação via POST/Redirect/GET: atualizar a página não duplica o agendamento
- Área do funcionário protegida por login, com senha armazenada em hash
- Painel com a lista de agendamentos ordenada por data e hora
- Atualização do status de cada serviço: Aguardando, Em andamento, Pronto
- Status validado no servidor, não apenas no formulário
- Layout responsivo, pensado para o celular

---

## Tecnologias

- **Python 3** e **Flask** — rotas, sessão e renderização
- **Jinja2** — templates com herança a partir de um `base.html`
- **PostgreSQL** (hospedado no **Neon**) — banco de dados, acessado via **psycopg** com consultas parametrizadas
- **Werkzeug** — hash de senha (`generate_password_hash` / `check_password_hash`)
- **pytest** — testes automatizados
- **python-dotenv** — variáveis de ambiente em desenvolvimento
- **Gunicorn** e **Render** — servidor de produção e hospedagem

Ambientes separados: desenvolvimento e testes usam uma branch `dev` do banco; produção usa a branch `production`. O código é idêntico nos dois — só o valor de `DATABASE_URL` muda.

---

## Estrutura do projeto

```
main.py          cria e configura a aplicação Flask
routes.py        as rotas do site
conexao.py       único ponto de contato com o banco de dados
validacoes.py    regras de negócio (horários, datas, status) — não conhece web nem banco
database.py      criação das tabelas e cadastro inicial de serviços
admin.py         criação do usuário administrador a partir das variáveis de ambiente
conftest.py      fixtures do pytest (usuário e agendamento de teste)
test_client.py   testes automatizados
templates/       páginas HTML
static/          folha de estilo
```

---

## Como rodar localmente

```bash
git clone https://github.com/joaohfaria/agendamento-dev.git
cd agendamento-dev
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

O projeto precisa de um banco PostgreSQL. Qualquer instância serve — local ou hospedada. Com a connection string em mãos, crie um arquivo `.env` na raiz (este arquivo não vai para o repositório):

```
DATABASE_URL=postgresql://usuario:senha@host/banco
SECRET_KEY=uma-chave-longa-e-aleatoria
ADMIN_USUARIO=nome-do-usuario-administrador
ADMIN_SENHA=senha-do-administrador
FLASK_DEBUG=1
```

A aplicação não sobe sem `SECRET_KEY` nem sem `DATABASE_URL` — ela falha na inicialização com uma mensagem explícita, de propósito, para não rodar com sessão insegura ou sem banco.

Crie as tabelas e o cadastro inicial de serviços:

```bash
python database.py
```

Rode:

```bash
python main.py
```

O site fica em `http://127.0.0.1:5000`. O usuário administrador é criado automaticamente na primeira execução, a partir das variáveis de ambiente.

---

## Testes

```bash
pytest
```

São 7 testes automatizados, que verificam:

- a página inicial responde e traz os campos do formulário
- a lista de agendamentos redireciona quem não está logado
- a lista de agendamentos abre para quem está logado
- o login funciona com credenciais válidas
- o login é recusado com senha errada
- um agendamento válido é criado e confirmado
- um status fora da lista permitida é recusado com HTTP 400

Os dados usados nos testes são criados e removidos por fixtures do pytest, então nenhuma senha real aparece no código e o banco fica limpo depois da execução. Os testes rodam contra a branch de desenvolvimento, nunca contra produção.

---

## Segurança

- Senhas gravadas apenas como hash, nunca em texto
- Todas as consultas SQL usam parâmetros, nunca concatenação de texto
- Segredos em variáveis de ambiente, com valores diferentes em desenvolvimento e produção
- `.env` fora do controle de versão
- Rotas da área do funcionário verificam a sessão antes de qualquer operação
- Dados vindos do formulário são validados no servidor, independentemente do que o HTML oferece
- Conexões com o banco são fechadas em `finally`, inclusive quando a requisição termina em erro

---

## Limitações conhecidas

- **Não existe tela para trocar a senha.** A senha do administrador só muda pela variável de ambiente.
- **Não há confirmação por e-mail nem lembrete automático** para o cliente.
- **Os horários ocupados continuam aparecendo na lista** do formulário; o cliente só descobre que o horário está tomado depois de enviar.
- **A primeira requisição depois de um período ocioso é lenta**, porque tanto o serviço web quanto o banco hibernam nos planos gratuitos.

---

## Próximos passos

- Esconder da tela os horários já ocupados, usando JavaScript
- Tela de troca de senha
- Organizar as rotas em Blueprints
- Lembrete automático por e-mail para o cliente

---

Projeto desenvolvido por [João Henrique Faria](https://github.com/joaohfaria) como estudo prático de desenvolvimento web com Python.
