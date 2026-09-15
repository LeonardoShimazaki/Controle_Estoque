from flask import Flask, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import conectar

app = Flask(__name__)

app.config["SECRET_KEY"] = "chave-temporaria-controle-estoque"
def verificar_admin():

    if "usuario_id" not in session:
        return False

    return session.get("perfil") == "ADMIN"

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login = request.form["login"]
        senha = request.form["senha"]

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            SELECT id, nome, login, senha, perfil
            FROM usuario
            WHERE login = %s
        """

        cursor.execute(sql, (login,))

        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario[3], senha):
            session["usuario_id"] = usuario[0]
            session["nome"] = usuario[1]
            session["perfil"] = usuario[4]

            return render_template(
                "dashboard.html",
                nome=session["nome"],
                perfil=session["perfil"]
            )

        return "Login ou senha inválida"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "usuario_id" not in session:
        return "Você precisa fazer login primeiro!"

    return render_template(
        "dashboard.html",
        nome=session["nome"],
        perfil=session["perfil"]
    )

@app.route("/produtos")
def produtos ():

    if "usuario_id" not in session:
        return "Você precisa fazer login primeiro!"

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, descricao, quantidade, estoque_minimo
        FROM produto
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "produtos.html",
        produtos=produtos
    )

@app.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if "usuario_id" not in session:
        return "Você precisa fazer login primeiro!"

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        quantidade_texto = request.form.get("quantidade")
        estoque_minimo_texto = request.form.get("estoque_minimo")

        if not nome:
            return "Erro: o nome do produto é obrigatório!"

        try:
            quantidade = int(quantidade_texto)
            estoque_minimo = int(estoque_minimo_texto)
        except (ValueError, TypeError):
            return "Erro: quantidade e estoque mínimo devem ser números inteiros!"

        if quantidade < 0 or estoque_minimo < 0:
            return "Erro: quantidade e estoque mínimo não podem ser negativos!"

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO produto
            (nome, descricao, quantidade, estoque_minimo)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (nome, descricao, quantidade, estoque_minimo)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            mensagem="Produto cadastrado com sucesso!",
            tipo="produto"
        )

    return render_template("produto_form.html")


@app.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
def editar_produto(id):

    if "usuario_id" not in session:
        return "Você precisa fazer login primeiro!"

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        nome = request.form["nome"]
        descricao = request.form["descricao"]
        quantidade = request.form["quantidade"]
        estoque_minimo = request.form["estoque_minimo"]

        sql = """
            UPDATE produto
            SET nome = %s,
                descricao = %s,
                quantidade = %s,
                estoque_minimo = %s
            WHERE id = %s
        """

        cursor.execute(
            sql,
            (nome, descricao, quantidade, estoque_minimo, id)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        return "Produto atualizado com sucesso!"

    cursor.execute("""
        SELECT id, nome, descricao, quantidade, estoque_minimo
        FROM produto
        WHERE id = %s
    """, (id,))

    produto = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not produto:
        return "Produto não encontrado!"

    return render_template(
        "produto_editar.html",
        produto=produto
    )

@app.route("/movimentacoes", methods=["GET", "POST"])
def movimentacoes():

    if "usuario_id" not in session:
        return "Você precisa fazer login primeiro!"

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        produto_id = request.form.get("produto_id")
        tipo = request.form.get("tipo")
        quantidade_texto = request.form.get("quantidade")

        if not produto_id or not tipo or not quantidade_texto:
            return "Erro: todos os campos são obrigatórios!"

        if tipo not in ["ENTRADA", "SAIDA"]:
            return "Erro: tipo de movimentação inválido!"

        try:
            quantidade = int(quantidade_texto)
        except ValueError:
            return "Erro: a quantidade deve ser um número inteiro!"

        if quantidade <= 0:
            return "Erro: a quantidade deve ser maior que zero!"

        cursor.execute("""
            SELECT quantidade
            FROM produto
            WHERE id = %s
        """, (produto_id,))

        produto = cursor.fetchone()

        if not produto:
            cursor.close()
            conexao.close()
            return "Produto não encontrado!"

        estoque_atual = produto[0]

        if tipo == "SAIDA" and quantidade > estoque_atual:
            cursor.close()
            conexao.close()
            return "Erro: quantidade de saída maior que o estoque disponível!"

        if tipo == "ENTRADA":
            novo_estoque = estoque_atual + quantidade
        else:
            novo_estoque = estoque_atual - quantidade

        cursor.execute("""
            UPDATE produto
            SET quantidade = %s
            WHERE id = %s
        """, (novo_estoque, produto_id))

        cursor.execute("""
            INSERT INTO movimentacao
            (produto_id, usuario_id, tipo, quantidade)
            VALUES (%s, %s, %s, %s)
        """, (
            produto_id,
            session["usuario_id"],
            tipo,
            quantidade
        ))

        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            mensagem="Movimentação registrada com sucesso!",
            tipo="movimentacao"
        )

    cursor.execute("""
        SELECT id, nome, quantidade
        FROM produto
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "movimentacao.html",
        produtos=produtos
    )

@app.route("/historico")
def historico():

    if "usuario_id" not in session:
        return "Você precisa fazer login primeiro!"

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            movimentacao.id,
            produto.nome,
            movimentacao.tipo,
            movimentacao.quantidade,
            usuario.nome,
            movimentacao.data_movimentacao
        FROM movimentacao
        INNER JOIN produto
            ON movimentacao.produto_id = produto.id
        INNER JOIN usuario
            ON movimentacao.usuario_id = usuario.id
        ORDER BY movimentacao.data_movimentacao DESC
    """)

    movimentacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "historico.html",
        movimentacoes=movimentacoes
    )

@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():

    if "usuario_id" not in session:
        return "Você precisa fazer login primeiro!"

    if not verificar_admin():
        return "Acesso negado! Apenas administradores podem acessar esta área."

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        login = request.form.get("login", "").strip()
        senha = request.form.get("senha", "")
        perfil = request.form.get("perfil")

        if not nome or not login or not senha or not perfil:
            return "Erro: todos os campos são obrigatórios!"

        if perfil not in ["ADMIN", "COMUM"]:
            return "Erro: perfil inválido!"

        if len(senha) < 6:
            return "Erro: a senha deve possuir pelo menos 6 caracteres!"

        senha_hash = generate_password_hash(
            senha,
            method="pbkdf2:sha256"
        )

        cursor.execute("""
            INSERT INTO usuario
            (nome, login, senha, perfil)
            VALUES (%s, %s, %s, %s)
        """, (
            nome,
            login,
            senha_hash,
            perfil
        ))

        conexao.commit()

        cursor.close()
        conexao.close()

        return render_template(
            "sucesso.html",
            mensagem="Usuário cadastrado com sucesso!",
            tipo="usuario"
        )

    cursor.execute("""
        SELECT id, nome, login, perfil
        FROM usuario
        ORDER BY nome
    """)

    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )

@app.route("/logout")
def logout():

    session.clear()

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)