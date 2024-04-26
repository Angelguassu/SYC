from flask import Flask, render_template, request, session, jsonify, redirect
import sqlite3


app = Flask(__name__)
app.secret_key = "1234"

DATABASE = 'database.db'    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gestao')
def gestao():
    return render_template('gestao.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        is_admin = session.get('is_admin', False)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM solicitacoes')
        solicitacoes = cursor.fetchall()
        conn.close()
        return render_template('home.html', username=username, is_admin=is_admin, solicitacoes=solicitacoes)
    else:
        return redirect('/fazer_login')


@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    criar_tabela()
    username = request.form['username']
    email = request.form['email']
    telefone = request.form['telefone']
    senha = request.form['senha']
    confirma_senha = request.form['confirma_senha']

    if not username or not email or not telefone or not senha or not confirma_senha:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    if senha != confirma_senha:
        return jsonify({'error': 'As senhas não coincidem'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (username,))
    usuario_existente = cursor.fetchone()
    if usuario_existente:
        conn.close()
        return jsonify({'error': 'Usuário já cadastrado'}), 400

    cursor.execute('INSERT INTO usuarios (nome, email, telefone, senha) VALUES (?, ?, ?, ?)', (username, email, telefone, senha))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Cadastro realizado com sucesso!'}), 201

@app.route('/fazer_login', methods=['POST'])
def fazer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        chave_acesso = request.form['chave_acesso']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?', (username, password))
        usuario = cursor.fetchone()
        
        if usuario and chave_acesso == "1234":
            session['username'] = username
            session['email'] = usuario[2]  # armazene o email na sessão
            session['is_admin'] = True
            conn.close()
            return redirect('/adm')
        elif usuario:
            session['username'] = username
            session['email'] = usuario[2]  # armazene o email na sessão
            session['is_admin'] = False
            conn.close()
            return redirect('/home')
        else:
            error = "Acesso negado."
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")

@app.route('/redirect_main')
def redirect_main():
    return redirect('/')

@app.route('/excluir/<int:id_solicitacao>', methods=['GET', 'POST'])
def excluir_solicitacao(id_solicitacao):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM solicitacoes WHERE id = ?', (id_solicitacao,))
    conn.commit()
    conn.close()
    return redirect('/adm')

@app.route('/responder/<int:id_solicitacao>', methods=['POST'])
def responder_solicitacao(id_solicitacao):
    if request.method == 'POST':
        comentario = request.form['comentario']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''UPDATE solicitacoes 
                     SET comentario=?
                     WHERE id=?''',
                  (comentario, id_solicitacao))
        conn.commit()
        conn.close()
        return redirect('/home')
    
@app.route('/responder/<int:id_solicitacao>', methods=['GET', 'POST'])
def responder_editar_solicitacao(id_solicitacao):
    if request.method == 'POST':
        username = request.form['username']
        telefone = request.form['telefone']
        email = request.form['email']
        setor = request.form['setor']
        assunto = request.form['assunto']
        detalhes = request.form['detalhes']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''UPDATE solicitacoes 
                     SET username=?, telefone=?, email=?, setor=?, assunto=?, detalhes=?
                     WHERE id=?''',
                  (username, telefone, email, setor, assunto, detalhes, id_solicitacao))
        conn.commit()
        conn.close()
        return redirect('/home')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solicitacoes WHERE id = ?', (id_solicitacao,))
    solicitacao = cursor.fetchone()
    conn.close()
    return render_template('responder.html', solicitacao=solicitacao)

@app.route('/editar/<int:id_solicitacao>', methods=['GET', 'POST'])
def editar_solicitacao(id_solicitacao):
    if request.method == 'POST':
        username = request.form['username']
        telefone = request.form['telefone']
        email = request.form['email']
        setor = request.form['setor']
        assunto = request.form['assunto']
        detalhes = request.form['detalhes']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''UPDATE solicitacoes 
                     SET username=?, telefone=?, email=?, setor=?, assunto=?, detalhes=?
                     WHERE id=?''',
                  (username, telefone, email, setor, assunto, detalhes, id_solicitacao))
        conn.commit()
        conn.close()
        return redirect('/adm')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solicitacoes WHERE id = ?', (id_solicitacao,))
    solicitacao = cursor.fetchone()
    conn.close()
    return render_template('editar.html', solicitacao=solicitacao)

@app.route('/usuarios')
def listar_usuarios():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, telefone FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return jsonify({'usuarios': usuarios})

@app.route('/cadastrar_solicitacao', methods=['POST'])
def cadastrar_solicitacao():
    if request.method == 'POST':
        username = request.form['username']
        telefone = request.form['telefone']
        email = request.form['email']
        setor = request.form['setor']
        assunto = request.form['assunto']
        detalhes = request.form['requisitos']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO solicitacoes (username, telefone, email, setor, assunto, detalhes) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, telefone, email, setor, assunto, detalhes))
        conn.commit()
        conn.close()
        return render_template('home.html', username=username, telefone=telefone, email=email, setor=setor, assunto=assunto, detalhes=detalhes)
    
def criar_tabela():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL,
            setor TEXT NOT NULL,
            assunto TEXT NOT NULL,
            detalhes TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    
@app.route('/solicitacao')
def solicitacao():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT email, telefone FROM usuarios WHERE nome = ?', (username,))
        user_info = cursor.fetchone()
        conn.close()
        if user_info:
            email, telefone = user_info
            return render_template('solicitacao.html', username=username, email=email, telefone=telefone)
        else:
            # Se não encontrar informações do usuário, redirecione para o login
            return redirect('/fazer_login')
    else:
        # Se o usuário não estiver logado, redirecione para o login
        return redirect('/fazer_login')
    


# Adicione esta rota para lidar com a página de administração
@app.route('/adm')
def adm():
    if 'username' in session and session.get('is_admin', False):
        # Se o usuário estiver logado como admin
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM solicitacoes')
        solicitacoes = cursor.fetchall()
        conn.close()
        return render_template('adm.html', solicitacoes=solicitacoes)
    else:
        # Se não for um admin, redirecione para a página de login
        return redirect('/fazer_login')


@app.route('/my_solicitacoes')
def my_solicitacoes():
    if 'username' in session:
        email = session['email']  # Mudança aqui para usar o email em vez do nome
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM solicitacoes WHERE email = ?', (email,))
        solicitacoes = cursor.fetchall()
        conn.close()
        return render_template('my_soli.html', solicitacoes=solicitacoes)
    else:
        # Se o usuário não estiver logado, redirecione para o login
        return redirect('/fazer_login')



criar_tabela()   
if __name__ == '__main__':
    app.run(debug=True)
