import sqlite3

def connect():
    conn = sqlite3.connect('database/estoque.db')
    return conn

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_compra REAL,
            preco_venda REAL
        )
    ''')

    # Tabela de movimentações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT, 
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')

    conn.commit()
    conn.close()
