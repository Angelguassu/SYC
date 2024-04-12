from flask import Flask, render_template, request, session, jsonify, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

# Configurações do banco de dados
DATABASE = 'database.db'

# Função para criar a tabela de usuários
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
    conn.commit()
    conn.close()

# Rota padrão
@app.route('/')
def index():
    return render_template('index.html')

# Rota solicitação
@app.route('/solicitacao')
def solicitacao():
    return render_template('solicitacao.html')

# Rota para a página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Rota para a página home após o login
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        is_admin = session.get('is_admin', False)
        return render_template('home.html', username=username, is_admin=is_admin)
    else:
        return redirect('/fazer_login')

# Rota para a página do administrador
@app.route('/adm')
def admin_page():
    if 'username' in session and session.get('is_admin', False):
        return render_template('adm.html', username=session['username'])
    else:
        return redirect('/fazer_login')

# Rota para o cadastro de um novo usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    criar_tabela()
    username = request.form['username']
    email = request.form['email']
    telefone = request.form['telefone']
    senha = request.form['senha']
    confirma_senha = request.form['confirma_senha']

    # Verifica se os campos estão preenchidos
    if not username or not email or not telefone or not senha or not confirma_senha:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    # Verifica se as senhas coincidem
    if senha != confirma_senha:
        return jsonify({'error': 'As senhas não coincidem'}), 400

    # Verifica se o usuário já existe no banco de dados
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (username,))
    usuario_existente = cursor.fetchone()
    if usuario_existente:
        conn.close()
        return jsonify({'error': 'Usuário já cadastrado'}), 400

    # Adiciona o novo usuário ao banco de dados
    cursor.execute('INSERT INTO usuarios (nome, email, telefone, senha) VALUES (?, ?, ?, ?)', (username, email, telefone, senha))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Cadastro realizado com sucesso!'}), 201

# Rota para o login
@app.route('/fazer_login', methods=['POST'])
def fazer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        chave_acesso = request.form['chave_acesso']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Verifica se o usuário existe no banco de dados
        cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?', (username, password))
        usuario = cursor.fetchone()
        
        # Verifica se é um ADM
        if usuario and chave_acesso == "1234":
            session['username'] = username
            session['is_admin'] = True
            conn.close()
            return redirect('/adm')  # Redirecionamento para a página ADM
        elif usuario:
            session['username'] = username
            session['is_admin'] = False
            conn.close()
            return redirect('/home')  # Redirecionamento para a página home
        else:
            error = "Acesso negado."
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")

# Rota para o dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        is_admin = session.get('is_admin', False)
        if is_admin:
            return redirect('/adm')
        else:
            return f"<h1>Bem-vindo, {username}!</h1>"
    else:
        return redirect('/fazer_login')

# Rota para redirecionar para a página principal
@app.route('/redirect_main')
def redirect_main():
    return redirect('/')

# Rota para excluir um cadastro
@app.route('/excluir/<int:id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/adm')

# Rota para retornar os usuários cadastrados
@app.route('/usuarios')
def listar_usuarios():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, telefone FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return jsonify({'usuarios': usuarios})

if __name__ == '__main__':
    app.run(debug=True)
    # Redirecionar para a página principal ao iniciar o servidor
    app.add_url_rule('/redirect_main', 'redirect_main', redirect_main)
