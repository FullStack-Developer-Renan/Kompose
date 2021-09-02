# Kompose

### Adicione aqui os erros e correções aplicadas

---

**Código com erro:** docker-compose.yml

```sh
version: '3.3'
services:
    db:
        image: postgres:latest
        env_file: envs/dev.env
        ports:
            - 5432:5432

    migration:
        build: .
        env_file: envs/dev.env
        command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; python manage.py migrate'

        stdin_open: true
        tty: true

        depends_on:
            - db

    web:
        env_file: envs/dev.env
        command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; python manage.py runserver 0.0.0.0:8000'

        stdin_open: true
        tty: true
        ports:
            - 8000:8001

        depends_on:
            - db
            - migration
```

**Erro:** A versão 3.3 não bate com a última versão do Docker instalado / O db não está com os volumes setados / Código poluído com o migration / Volume não definido no serviço web / A condição para o banco depender do serviço web está definida de maneira errada com base nos critérios anteriores
**O que ele causa:** Trava na hora de realizar a build do docker-compose por não reconhecer a versão associada / Isso impede que os dados fiquem armazenados no banco postgresql / Desorganização no código / Toda e qualquer alteração no código precisaria executar o build do docker-compose (isso não é prático) / Erros na execução do build do docker compose
**Como corrigir:** Trocar a versão para a versão do docker suportada / Adicionar volumes ao db (lembrando que é importante o volume ser definido externalmente já que localmente seria difícil por cada máquina ter definido um diretório distinto para volumes) / Adicionar um healthcheck / Atribuir a dependência do migration à um arquivo chamado entrypoint.sh / Adicionar volumes no serviço web / Adicionar uma condition ao db especificado
**Código corrigido:**

```sh
version: "3.8"
services:
  postgres:
    image: postgres:latest
    env_file: ./envs/dev.env
    ports:
      - 5432:5432
    volumes:
      - simple:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    build: .
    ports:
      - 8000:8000
    command: python manage.py runserver 0.0.0.0:8000
    entrypoint: ./entrypoint.sh
    stdin_open: true
    tty: true
    volumes:
      - .:/code
    env_file: ./envs/dev.env
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  simple:
    external: true
```

---

**Código com erro:** Dockerfile

```sh
FROM python:2.7
```

**Erro:** A versão python:2.7
**O que ele causa:** Possíveis erros de execução no código por incompatibilidade por instalar uma imagem do docker não mais atual.
**Como corrigir:** Trocar a versão para python:3.9
**Código corrigido:**

```sh
FROM python:3.9
```

---

**Código com erro:** envs/devs.env

```sh
DB=kompose
USER=user
PASSWORD=password
```

**Erro:** As variáveis de ambiente foram inseridas de maneira incorreta
**O que ele causa:** Erros de execução no código
**Como corrigir:** Trocar nos nomes das variáveis de ambiente e seus devidos valores.
**Código corrigido:**

```sh
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=songs
```

---

**Código com erro:** kompose/settings.py

```sh
ALLOWED_HOSTS = []
...
if os.getenv("TEST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgres",
            "NAME": os.getenv("DB"),
            "USER": os.getenv("USER"),
            "PASSWORD": os.getenv("PASSWORD"),
            "HOST": "database",
            "PORT": 5432,
        }
    }

```

**Erro:** Permissões para acessar a api não foram fornecidas / Databases escritos de maneira incorreta / Ponte do banco postgresql da app com o banco do heroku não realizada
**O que ele causa:** Acessar a api do heroku ou até mesmo do localhost não será possível / Erros de execução do código / Banco postgresql do heroku não será criado gerando um erro na api
**Como corrigir:** Mudar o código / Gerar a ponte do banco da app com o do heroku
**Código corrigido:**

```sh
import dj_database_url
...
ALLOWED_HOSTS = ["kompose-renan.herokuapp.com", "localhost"]
...
if os.getenv("TEST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": "postgres",
            "PORT": 5432,
        }
    }
...
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    config = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
    DATABASES['default'] = config
    DEBUG = False

```

---
