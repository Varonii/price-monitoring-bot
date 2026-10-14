# Telegram Price Tracker Bot

Bot para Telegram que monitora os preços de produtos da Amazon e envia mensagens quando identifica uma queda de preço.

O bot utiliza SQLite para salvar os produtos monitorados e realiza verificações automáticas a cada 6 horas.

**Importante:** o bot funciona apenas enquanto o arquivo `main.py` estiver em execução.

## Funcionalidades

- Adicionar produtos pelo link da Amazon.
- Listar produtos monitorados e seus preços.
- Remover produtos da lista.
- Verificar preços automaticamente e avisar sobre quedas.

## Comandos

| Comando | Descrição |
|---|---|
| `/start` | Mostra as boas-vindas e os comandos disponíveis. |
| `/adicionar <link>` | Adiciona um produto para monitoramento. |
| `/listar` | Mostra os produtos monitorados. |
| `/remover <id>` | Remove um produto pelo ID. |

## Estrutura do projeto

```text
telegram-price-tracker/
├── main.py
├── preco.py
├── banco.py
├── teste_loja.py
├── requirements.txt
└── produtos.db
```

- `main.py`: inicia o bot e gerencia os comandos.
- `preco.py`: extrai o nome e o preço dos produtos.
- `banco.py`: gerencia o banco de dados SQLite.
- `teste_loja.py`: realiza testes de requisições.

## Como executar

**1. Clone o repositório**

```bash
git clone https://github.com/SEU_USUARIO/price-monitoring-bot.git
cd price-monitoring-bot
```

**2. Crie e ative o ambiente virtual**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure o token**

Crie um arquivo `token.env` na raiz do projeto com o token obtido pelo [@BotFather](https://t.me/BotFather).

```env
TELEGRAM_TOKEN=seu_token_aqui
```

**5. Inicie o bot**

```bash
python main.py
```

Pronto! Com o script em execução, você pode acessar o bot pelo Telegram e começar a monitorar produtos.

## Tecnologias

- Python
- SQLite
- Telegram Bot API

