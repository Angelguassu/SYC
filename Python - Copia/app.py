from flask import Flask, render_template, request, session, jsonify, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

# Configurações do banco de dados
DATABASE = 'database.db'


# Rota padrão
@app.route('/')
def index():
    return render_template('index.html')

# Rota solicitação
@app.route('/solicitacao')
def solicitacao():
    return render_template('solicitacao.html')

# Rota Gestão
@app.route('/gestao')
def gestao():
    return render_template('gestao.html')

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
        # Busca as solicitações cadastradas no banco de dados
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM solicitacoes')
        solicitacoes = cursor.fetchall()
        conn.close()
        # Renderiza o template 'home.html' passando as solicitações como contexto
        return render_template('home.html', username=username, is_admin=is_admin, solicitacoes=solicitacoes)
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
            return redirect('/home')  # Redirecionamento para a página ADM
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
    return redirect('/gestao')

# Rota para retornar os usuários cadastrados
@app.route('/usuarios')
def listar_usuarios():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, telefone FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return jsonify({'usuarios': usuarios})

# Rota para cadastrar o formulário
@app.route('/cadastrar_solicitacao', methods=['POST'])
def cadastrar_solicitacao():
    if request.method == 'POST':
        username = request.form['username']
        telefone = request.form['telefone']
        email = request.form['email']
        setor = request.form['setor']
        assunto = request.form['assunto']
        detalhes = request.form['requisitos']
        # Aqui você inseriria esses dados no banco de dados
        # Exemplo usando SQLite
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO solicitacoes (username, telefone, email, setor, assunto, detalhes) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, telefone, email, setor, assunto, detalhes))
        conn.commit()
        conn.close()
        return render_template('home.html', username=username, telefone=telefone, email=email, setor=setor, assunto=assunto, detalhes=detalhes)
    


# Função para criar a tabela de usuários e a tabela de solicitações
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

# Chamada da função para criar as tabelas
criar_tabela()   
if __name__ == '__main__':
    app.run(debug=True)