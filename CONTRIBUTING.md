# Contribuindo com o DRESScode

Obrigada pelo interesse em contribuir! Este guia explica como configurar o ambiente e submeter contribuições.

---

## Índice

- [Contribuindo com o DRESScode](#contribuindo-com-o-dresscode)
  - [Índice](#índice)
  - [Pré-requisitos](#pré-requisitos)
  - [Configuração do Ambiente Local](#configuração-do-ambiente-local)
  - [Variáveis de Ambiente](#variáveis-de-ambiente)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Fluxo de Contribuição](#fluxo-de-contribuição)
  - [Padrões de Código](#padrões-de-código)
  - [Testes](#testes)
  - [Licença](#licença)

---

## Pré-requisitos

- Python 3.12+
- pip
- Git

---

## Configuração do Ambiente Local

```bash
# 1. Fork e clone o repositório
git clone https://github.com/<seu-usuario>/DRESScode.git
cd DRESScode

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente (veja a seção abaixo)
cp .env.example .env
# Edite o .env com seus valores

# 5. Aplique as migrations e suba o servidor
python manage.py migrate
python manage.py runserver
```

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True

# Banco de dados (opcional em dev — sem isso, usa SQLite)
DATABASE_URL=postgres://usuario:senha@host:5432/dresscode

# Cloudinary (necessário para upload de imagens)
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

# E-mail (opcional em dev — sem isso, exibe no console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@dresscode.com
```

> Em desenvolvimento, `DATABASE_URL` pode ser omitido — o projeto usa SQLite automaticamente.
> Para `CLOUDINARY_URL`, crie uma conta gratuita em [cloudinary.com](https://cloudinary.com).

---

## Estrutura do Projeto

```
DRESScode/
├── core/               # Configurações do Django (settings, urls, wsgi)
├── wardrobe/           # App principal
│   ├── models.py       # Modelos: Piece e Outfit
│   ├── views.py        # Views de peças, outfits e conta
│   ├── urls.py         # Rotas do app
│   └── tests.py        # Testes
├── templates/          # Templates HTML
├── static/             # CSS e JS
├── requirements.txt
└── build.sh            # Script de build para deploy
```

**Modelos principais:**

- `Piece` — peça de roupa com categoria (`shirt`, `pants`, `shoes`) e imagem no Cloudinary
- `Outfit` — combinação de peças com nome, imagem gerada e tags separadas por vírgula

---

## Fluxo de Contribuição

1. Crie uma branch a partir de `main`:
   ```bash
   git checkout -b feat/nome-da-feature
   # ou
   git checkout -b fix/nome-do-bug
   ```

2. Faça suas alterações e commit:
   ```bash
   git add arquivo.py
   git commit -m "feat: descrição curta da mudança"
   ```

3. Abra um Pull Request para a branch `main` do repositório original.

**Tipos de branch sugeridos:** `feat/`, `fix/`, `refactor/`, `docs/`

---

## Padrões de Código

- Python: siga o [PEP 8](https://peps.python.org/pep-0008/)
- Templates: indentação de 4 espaços, sem lógica complexa inline
- JavaScript: vanilla JS, sem frameworks externos
- Não commite `.env`, `db.sqlite3`, `media/` ou `staticfiles/`

---

## Testes

```bash
python manage.py test
```

Ao adicionar features, inclua testes em `wardrobe/tests.py` usando `django.test.TestCase`.

---

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [GNU GPL v3.0](LICENSE), a mesma licença do projeto.
