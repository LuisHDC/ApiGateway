import sqlite3


def getAllPedidos():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()

    cursor.execute("""
            SELECT * FROM Pedido
    """)

    colunas = [descricao[0] for descricao in cursor.description]

    resultado = []
    for linha in cursor.fetchall():
        linha_dict = {}
        for i, coluna in enumerate(colunas):
            linha_dict[coluna] = linha[i]
        resultado.append(linha_dict)

    conn.close()

    return resultado

def getPedido(numero):
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()

    cursor.execute("""
            SELECT * FROM Pedido
            WHERE numero = ?
    """, (numero))

    colunas = [descricao[0] for descricao in cursor.description]

    resultado = []
    for linha in cursor.fetchall():
        linha_dict = {}
        for i, coluna in enumerate(colunas):
            linha_dict[coluna] = linha[i]
        resultado.append(linha_dict)

    conn.close()

    return resultado

def insertPedido(pedido):
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()


    try:
        next_numero = get_next_numero_pedido()

        cursor.execute("""
                INSERT INTO Pedido
                VALUES(?, ?, ?)        
        """, (next_numero, next_numero, pedido['cliente']))

        conn.commit()

        conn.close()

        return True
    except():
        conn.rollback()
        return False

def get_next_numero_pedido():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()

    cursor.execute("""
            SELECT MAX(Numero)
            FROM Pedido
    """)
    
    max = cursor.fetchone()

    conn.close()

    return max[0]+1

def get_next_itemPedido_id():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()

    cursor.execute("""
            SELECT MAX(Id)
            FROM ItemPedido
    """)
    
    max = cursor.fetchone()

    conn.close()

    return max[0]+1

def get_item_pedido(numero):
    data = getPedido(numero)

    if data:
        conn = sqlite3.connect('pedidos.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM ItemPedido
            WHERE numero = ?
        """, (numero))
        colunas = [descricao[0] for descricao in cursor.description]

        resultado = []
        for linha in cursor.fetchall():
            linha_dict = {}
            for i, coluna in enumerate(colunas):
                linha_dict[coluna] = linha[i]
            resultado.append(linha_dict)

        return resultado
    else:
        return {"erro": "O numero de pedido {numero} nao existe!"}
    
def insertItemPedido(numero, itemPedido):
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()
    
    data = getPedido(numero)

    if (validateJson(itemPedido.keys()) is not True):
        return {"erro":"É necessário adicionar todos os atributos: CodigoSKU, Produto, Preco e Quantidade."}

    if data:
        nextId = get_next_itemPedido_id()
        cursor.execute("""
            INSERT INTO ItemPedido (Id, Numero, Indice, CodigoSKU, Produto, Preco, Quantidade)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (nextId, numero, nextId, itemPedido["codigosku"], itemPedido["produto"], itemPedido["preco"], itemPedido["quantidade"]))

        conn.commit()

        conn.close()

        return {}
    else:
        conn.close()
        return {"erro": "O numero de pedido {numero} nao existe!"}

def validateJson(jsonKeys):
    if "produto" in jsonKeys and "codigosku" in jsonKeys and "preco" in jsonKeys and "quantidade" in jsonKeys:
        return True
    return False

def create_tables():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ItemPedido(
                        Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        Numero INTEGER,
                        Indice INTEGER,
                        CodigoSKU INTEGER,
                        Produto VARCHAR(200),
                        Preco FLOAT,
                        Quantidade INTEGER,
                        
                        FOREIGN KEY (Numero) REFERENCES Pedido(Numero)
                    );
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pedido(
                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Numero INTEGER,
                Cliente VARCHAR(200),
                   
                UNIQUE (Numero)
            );
    """)

    conn.close()

def populate_tables():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()

    cursor.execute("""
            INSERT OR IGNORE INTO Pedido 
            VALUES (1, 1, 'Marcos'),
                   (2, 2, 'Carlos'),
                   (3, 3, 'Maria'),
                   (4, 4, 'Ricardo'),
                   (5, 5, 'Fernanda');
    """)

    cursor.execute("""
            INSERT OR IGNORE INTO ItemPedido 
            VALUES (1, 1, 1, 1000, 'Biscoito', 5.10, 2),
                   (2, 1, 2, 1295, 'Leite', 3.90, 1),
                   (3, 1, 3, 1470, 'Chocolate', 6.70, 1),
                   (4, 2, 4, 1040, 'Queijo', 29.00, 1),
                   (5, 2, 5, 1654, 'Sabão em pó', 17.60, 1),
                   (6, 3, 6, 1000, 'Biscoito', 5.10, 4),
                   (7, 4, 7, 1765, 'Feijão', 9.80, 1),
                   (8, 4, 8, 1233, 'Arroz', 15.40, 1),
                   (9, 4, 9, 1723, 'Bandeja de ovos', 30.00, 1),
                   (10, 5, 9, 1233, 'Arroz', 15.40, 2),
                   (11, 5, 10, 1765, 'Feijão', 9.80, 1),
                   (12, 5, 11, 1723, 'Bandeja de ovos', 30.00, 1),
                   (13, 5, 12, 1295, 'Leite', 3.90, 3);
    """)
    conn.commit()

    conn.close()