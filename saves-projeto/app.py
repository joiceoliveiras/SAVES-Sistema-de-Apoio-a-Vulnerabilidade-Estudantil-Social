# Importa o Flask
# e o render_template, que serve para carregar os arquivos HTML
from flask import Flask, render_template

# Importa o sqlite3 para conectar com o banco de dados SQLite
import sqlite3

# Cria a aplicação Flask
app = Flask(__name__)

# Caminho do banco de dados (fica fora da pasta saves-projeto)
DATABASE = '../saves.db'

# Função responsável por abrir a conexão com o banco
def get_db_connection():
    conn = sqlite3.connect('../saves.db')

    # Faz com que os resultados das consultas possam ser acessados por nome
    # Ex: aluno["nome"] em vez de aluno[0]
    conn.row_factory = sqlite3.Row

    # Retorna a conexão aberta
    return conn

# Rota inicial do sistema (página de login)
@app.route('/')
def login():

    # Renderiza o arquivo login.html
    return render_template('login.html')


@app.route('/aluno')
def aluno():
    return render_template('aluno.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

# Rota responsável por mostrar o ranking de vulnerabilidade
@app.route('/ranking')
def ranking():
    conn = get_db_connection()

     # Consulta que busca os alunos e suas pontuações,
    # juntando a tabela aluno com a socioeconomico
    alunos = conn.execute("""
        SELECT 
            aluno.nome,
            aluno.matricula,
            socioeconomico.pontuacao_vulnerabilidade
        FROM socioeconomico
        JOIN aluno ON socioeconomico.aluno_id = aluno.id_aluno
        ORDER BY socioeconomico.pontuacao_vulnerabilidade DESC
    """).fetchall()
    conn.close()

     # Envia os dados para o HTML ranking.html
    return render_template('ranking.html', alunos=alunos)

# Esse bloco garante que o Flask só vai rodar
# quando esse arquivo for executado diretamente
if __name__ == '__main__':

     # Inicia o servidor Flask em modo debug
    # O debug facilita os testes e mostra erros no navegador
    app.run(debug=True)
