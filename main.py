import tkinter as tk
from tkinter import messagebox
from database.db_config import create_tables, connect  

# Tornar entry_busca global
entry_busca = None

def iniciar():
    create_tables()
    messagebox.showinfo("Sucesso", "Banco de dados inicializado com sucesso!")

def cadastrar_produto():
    def salvar_produto():
        nome = entry_nome.get()
        categoria = entry_categoria.get()
        quantidade = entry_quantidade.get()
        preco_compra = entry_preco_compra.get()
        preco_venda = entry_preco_venda.get()

        if nome and categoria and quantidade and preco_compra and preco_venda:
            conn = connect()  
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO produtos (nome, categoria, quantidade, preco_compra, preco_venda)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, categoria, quantidade, preco_compra, preco_venda))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")  
            cadastro_window.destroy()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

    # Janela de cadastro de produto
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastrar Produto")

    tk.Label(cadastro_window, text="Nome do Produto").pack(pady=5)
    entry_nome = tk.Entry(cadastro_window)  
    entry_nome.pack(pady=5)

    tk.Label(cadastro_window, text="Categoria").pack(pady=5)
    entry_categoria = tk.Entry(cadastro_window)
    entry_categoria.pack(pady=5)

    tk.Label(cadastro_window, text="Quantidade").pack(pady=5)
    entry_quantidade = tk.Entry(cadastro_window)
    entry_quantidade.pack(pady=5)

    tk.Label(cadastro_window, text="Preço de Compra").pack(pady=5)
    entry_preco_compra = tk.Entry(cadastro_window)
    entry_preco_compra.pack(pady=5)

    tk.Label(cadastro_window, text="Preço de Venda").pack(pady=5)
    entry_preco_venda = tk.Entry(cadastro_window)
    entry_preco_venda.pack(pady=5)

    tk.Button(cadastro_window, text="Salvar", command=salvar_produto).pack(pady=10)

# Função para visualizar os produtos
def visualizar_produtos():
    # Janela para visualizar produtos
    visualizar_window = tk.Toplevel(root)
    visualizar_window.title("Produtos Cadastrados")

    # Criar a lista de produtos
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, categoria, quantidade, preco_compra, preco_venda FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    # Cabeçalho da tabela
    header = tk.Label(visualizar_window, text="ID | Nome | Categoria | Quantidade | Preço de Compra | Preço de Venda")
    header.pack(pady=10)

    # Exibir os produtos
    for produto in produtos:
        # Frame para cada produto
        produto_frame = tk.Frame(visualizar_window)
        produto_frame.pack(pady=5, fill=tk.X)

        # Exibir dados do produto
        produto_label = tk.Label(produto_frame, text=f"{produto[0]} | {produto[1]} | {produto[2]} | {produto[3]} | {produto[4]} | {produto[5]}")
        produto_label.pack(side=tk.LEFT, padx=5)

        # Botão de editar para o produto atual
        botao_editar = tk.Button(produto_frame, text="Editar", command=lambda id_produto=produto[0]: editar_produto(id_produto))
        botao_editar.pack(side=tk.LEFT, padx=5)

        # Botão de excluir para o produto atual
        botao_deletar = tk.Button(produto_frame, text="Excluir", command=lambda id_produto=produto[0]: deletar_produto(id_produto))
        botao_deletar.pack(side=tk.LEFT, padx=5)

    # Finalizando a janela
    visualizar_window.mainloop()

# Função para editar os produtos
def editar_produto(id_produto):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, categoria, quantidade, preco_compra, preco_venda FROM produtos WHERE id=?", (id_produto,))
    produto = cursor.fetchone()
    conn.close()
    
    # Janela para editar o produto
    editar_window = tk.Toplevel(root)
    editar_window.title("Editar Produto")

    # Labels e campos para editar as informações
    tk.Label(editar_window, text="Nome do Produto").pack(pady=5)
    entry_nome = tk.Entry(editar_window)
    entry_nome.insert(0, produto[0])
    entry_nome.pack(pady=5)

    tk.Label(editar_window, text="Categoria").pack(pady=5)
    entry_categoria = tk.Entry(editar_window)
    entry_categoria.insert(0, produto[1])
    entry_categoria.pack(pady=5)

    tk.Label(editar_window, text="Quantidade").pack(pady=5)
    entry_quantidade = tk.Entry(editar_window)
    entry_quantidade.insert(0, produto[2])
    entry_quantidade.pack(pady=5)

    tk.Label(editar_window, text="Preço de Compra").pack(pady=5)
    entry_preco_compra = tk.Entry(editar_window)
    entry_preco_compra.insert(0, produto[3])
    entry_preco_compra.pack(pady=5)

    tk.Label(editar_window, text="Preço de Venda").pack(pady=5)
    entry_preco_venda = tk.Entry(editar_window)
    entry_preco_venda.insert(0, produto[4])
    entry_preco_venda.pack(pady=5)

    def salvar_edicao():
        nome = entry_nome.get()
        categoria = entry_categoria.get()
        quantidade = entry_quantidade.get()
        preco_compra = entry_preco_compra.get()
        preco_venda = entry_preco_venda.get()

        if nome and categoria and quantidade and preco_compra and preco_venda:
            # Atualizar o banco de dados com os novos valores
            conn = connect()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE produtos
                SET nome = ?, categoria = ?, quantidade = ?, preco_compra = ?, preco_venda = ?
                WHERE id = ?
            ''', (nome, categoria, quantidade, preco_compra, preco_venda, id_produto))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
            editar_window.destroy()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

    tk.Button(editar_window, text="Salvar", command=salvar_edicao).pack(pady=10)

# Deletar Produtos
def deletar_produto(id_produto):
    resposta = messagebox.askyesno("Confirmar Exclusão", "Tem Certeza que deseja excluir este produto?")
    if resposta:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
        visualizar_produtos() # Atualiza a janela para refletir a exclusão

# Buscar Produtos
def buscar_produtos():
    # Agora entry_busca está corretamente associada a um campo de entrada
    termo_busca = entry_busca.get()

    # Janela para visualizar produtos
    visualizar_window = tk.Toplevel(root)
    visualizar_window.title("Produtos Cadastrados")

    # Criar a lista de produtos com base na pesquisa
    conn = connect()
    cursor = conn.cursor()

    # Consulta SQL para buscar produtos pelo nome ou categoria 
    cursor.execute('''
        SELECT id, nome, categoria, quantidade, preco_compra, preco_venda
        FROM produtos
        WHERE nome LIKE ? OR categoria LIKE ?
    ''', (f"%{termo_busca}%", f"%{termo_busca}%"))
    produtos = cursor.fetchall()
    conn.close()

    # Cabeçalho da tabela 
    tk.Label(visualizar_window, text="ID | Nome | Categoria | Quantidade | Preço de Compra | Preço de Venda").pack(pady=10)

    # Exibir os produtos
    if produtos:
        for produto in produtos:
            tk.Label(visualizar_window, text=f"{produto[0]} | {produto[1]} | {produto[2]} | {produto[3]} | {produto[4]} | {produto[5]}").pack(pady=5)
            # Botão de editar para o produto atual
            botao_editar = tk.Button(visualizar_window, text="Editar", command=lambda id_produto=produto[0]: editar_produto(id_produto))
            botao_editar.pack(pady=5)
            # Botão de deletar para o produto atual
            botao_deletar = tk.Button(visualizar_window, text="Deletar", command=lambda id_produto=produto[0]: deletar_produto(id_produto))
            botao_deletar.pack(pady=5)
    else:
        tk.Label(visualizar_window, text="Nenhum produto encontrado.").pack(pady=10)

    visualizar_window.mainloop()

# Barra de busca
def adicionar_barra_busca():
    global entry_busca  # Tornando entry_busca global
    tk.Label(root, text="Buscar Produto:").pack(pady=5)
    entry_busca = tk.Entry(root)
    entry_busca.pack(pady=5)

    botao_buscar = tk.Button(root, text="Buscar", command=buscar_produtos)
    botao_buscar.pack(pady=5)

# Criação da janela principal
root = tk.Tk()
root.title("Sistema de Estoque")

# Adicionando um botão para inicializar o banco de dados
botao_iniciar = tk.Button(root, text="Iniciar Banco de Dados", command=iniciar)
botao_iniciar.pack(pady=20)

# Adicionando um botão para abrir o cadastro de produto
botao_cadastrar_produto = tk.Button(root, text="Cadastrar Produto", command=cadastrar_produto)
botao_cadastrar_produto.pack(pady=20)

# Adicionando um botão para visualizar os produtos cadastrados
botao_visualizar_produtos = tk.Button(root, text="Visualizar Produtos", command=visualizar_produtos)
botao_visualizar_produtos.pack(pady=20)

# Adicionando a barra de busca
adicionar_barra_busca()

# Executando a interface
root.mainloop()
