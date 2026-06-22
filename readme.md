# Software-EPI

Este aplicativo é uma versão offline do app principal disponivel em:
https://github.com/lucimaraalvesramalho/Software-EPI

Aplicativo para cadastro de funcionários e gerenciamento de EPIs.

## Visão geral

- `app.py`: ponto de entrada do Flask.
- `database.py`: configuração da conexão com o banco de dados.
- `controller/routes.py`: rotas e lógica de CRUD.
- `models/tables.py`: definição das tabelas do banco.
- `static/`: arquivos estáticos (CSS e JavaScript).
- `templates/`: páginas HTML renderizadas pelo Flask.

## Estrutura do projeto

```
app.py
controller/
├── routes.py
models/
├── tables.py
static/
├── css/
│   ├── atualizar-registros.css
│   ├── cadastro-epi.css
│   ├── cadastro-funcionario.css
│   ├── criar-registro.css
│   ├── dashboard.css
│   └── global.css
├── epis.js
├── funcionarios.js
├── registros.js
├── script.js
templates/
└── components/
│   └── header.html
├── base.html
├── cadastrar-epi.html
├── cadastrar-funcionario.html
├── criar-registro.html
├── epis.html
├── funcionarios.html
├── index.html
├── registros.html
database.py
script.sql
icon.ico
```

## Requisitos

- Python 3.10+ (ou compatível)
- Flask
- MySQL Connector/Python

## Instalação

1. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install flask matplotlib
```

## Execução

```bash
python app.py
```

Então acesse `http://127.0.0.1:5000` no navegador.

## Observações

- O formulário de cadastro de funcionário usa JavaScript para enviar os dados via `fetch`.
- Se o JS não carregar, confirme se o caminho do script em `templates/base.html` está correto.
- Ajuste as rotas e a configuração do banco conforme necessário.

## Extensões recomendadas para VS Code

- Thunder Client
- Database Client JDBC
- MySQL
- python (Pylance, Python, Python Debugger e Python Enviroments)
