---

# Software EPI (Offline Version)

Este projeto é uma versão offline do sistema principal disponível em:
[https://github.com/lucimaraalvesramalho/Software-EPI](https://github.com/lucimaraalvesramalho/Software-EPI)

Sistema web para gerenciamento de EPIs e controle de funcionários, desenvolvido com Flask e SQLite, permitindo execução local sem necessidade de servidor externo.

---

## Visão geral

O sistema permite:

* Cadastro de funcionários
* Cadastro de EPIs
* Registro de entrega e devolução de equipamentos
* Consulta e gerenciamento de registros
* Interface web renderizada pelo Flask

---

## Estrutura do projeto

```
app.py

controller/
└── routes.py

models/
└── tables.py

database.py
script.sql
icon.ico

static/
├── css/
│   ├── global.css
│   ├── dashboard.css
│   ├── cadastro-epi.css
│   ├── cadastro-funcionario.css
│   ├── criar-registro.css
│   ├── atualizar-registros.css
│   └── outros arquivos

├── js/
│   ├── script.js
│   ├── funcionarios.js
│   ├── epis.js
│   └── registros.js

templates/
├── base.html
├── index.html
├── cadastrar-funcionario.html
├── cadastrar-epi.html
├── criar-registro.html
├── funcionarios.html
├── epis.html
├── registros.html
└── components/
    └── header.html
```

---

## Tecnologias utilizadas

* Python 3.10+
* Flask
* SQLite
* HTML5
* CSS3
* JavaScript
* Matplotlib

---

## Como executar o projeto

### 1. Criar ambiente virtual (opcional)

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2. Instalar dependências

```bash
pip install flask matplotlib
```

---

### 3. Executar aplicação

```bash
python app.py
```

Acesse no navegador:

```
http://127.0.0.1:5000
```

---

## Banco de dados

O projeto utiliza SQLite local.

* Arquivo: database.db
* Estrutura pode ser recriada utilizando script.sql

---

## Observações

* As requisições do frontend são feitas via fetch para a API Flask.
* O projeto foi desenvolvido para uso local/offline.
* Certifique-se de que a pasta static e templates estejam no mesmo nível da aplicação.

---

## Extensões recomendadas para VS Code

* Python (Pylance)
* Thunder Client
* SQLite Viewer

---

## Licença

Projeto acadêmico / educacional.

---
