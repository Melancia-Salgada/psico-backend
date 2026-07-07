# EasyPsi 
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
> A aplicação permite login, busca de dados de Pokémon e endereço via APIs, cadastro e listagem no backend FastAPI, com opções de editar e excluir, e usa cache para reduzir requisições repetidas.

## 🚀 Instalando a EasyPsi

Para instalar o back-end da EasyPsi, siga estas etapas:

1. Após clonar os arquivos em sua máquina, abra o terminal.
2. Utilize os seguintes comandos para baixar as dependências.

```bash
pip install -r requirements.txt
python -m venv fastapi_env
install fastapi uvicorn
```
> [!NOTE]
> É possível utilizar outro nome ao invés de "fastapi_env".

3. Instale a extensão do MongoDB no vscode

## ☕ Inicializando o back

1. Abra um terminal específico para cada serviço do sistema (2 no total)

2. Em cada terminal aberto inicialize o fastapi

```bash
fastapi_env\Scripts\activate
```
> [!WARNING]
> Caso tenha mudado o nome da pasta ao baixar as depêndencias utilize o novo nome ao invés de "fastapi_env".

3. Digite cada comando a seguir num terminal diferente.

```bash
uvicorn routes.{Nome da rota}:app --reload --port {Numero da porta}

```

### Inicializando o front

1. Abra um terminal na pasta "front":

2. Instale as depêndencias usando:"

```bash
npm install
```

3. Inicialize utilizando:
```bash
npm start
```

### Inicializando o Banco

1. Para o banco de dados inicie o MongoDB na seginte porta:

```bash
mongodb://localhost:27017
```
2. Crie um banco chamando "easypsi".
3. Dentro do banco, crie as collections.

