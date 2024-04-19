from flask import Flask, render_template, request, session, jsonify, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "1234"

DATABASE = 'database.db'    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solicitacao')
def solicitacao():
    return render_template('solicitacao.html')

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
            session['is_admin'] = True
            conn.close()
            return redirect('/home')
        elif usuario:
            session['username'] = username
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
    return redirect('/home')

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
        return redirect('/home')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solicitacoes WHERE id = ?', (id_solicitacao,))
    solicitacao = cursor.fetchone()
    conn.close()
    return render_template('editar_solicitacao.html', solicitacao=solicitacao)

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

criar_tabela()   
if __name__ == '__main__':
    app.run(debug=True)
