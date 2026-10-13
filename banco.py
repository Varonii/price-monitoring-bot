import sqlite3

ARQUIVO = "produtos.db"

def conectar():
    return sqlite3.connect(ARQUIVO)

def criar_tabelas():
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                titulo TEXT,
                ultimo_preco REAL,
                UNIQUE(chat_id, url)
            )
        """)

def adicionar_produto(chat_id, url, titulo, preco):
    with conectar() as con:
        try:
            con.execute(
                "INSERT INTO produtos (chat_id, url, titulo, ultimo_preco) VALUES (?, ?, ?, ?)",
                (chat_id, url, titulo, preco),
            )
            return True
        except sqlite3.IntegrityError:
            return False

def listar_produtos(chat_id):
    with conectar() as con:
        return con.execute(
            "SELECT id, titulo, ultimo_preco, url FROM produtos WHERE chat_id = ?",
            (chat_id,),
        ).fetchall()

def listar_todos():
    with conectar() as con:
        return con.execute(
            "SELECT id, chat_id, url, titulo, ultimo_preco FROM produtos"
        ).fetchall()

def atualizar_preco(produto_id, novo_preco):
    with conectar() as con:
        con.execute(
            "UPDATE produtos SET ultimo_preco = ? WHERE id = ?",
            (novo_preco, produto_id),
        )

def remover_produto(chat_id, produto_id):
    with conectar() as con:
        cur = con.execute(
            "DELETE FROM produtos WHERE id = ? AND chat_id = ?",
            (produto_id, chat_id),
        )
        return cur.rowcount > 0

if __name__ == "__main__":
    criar_tabelas()
    adicionar_produto(123, "https://exemplo.com", "Produto teste", 999.90)
    print(listar_produtos(123))