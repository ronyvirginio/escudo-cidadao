from flask import Flask, render_template, request, send_file, abort
import whois
from datetime import datetime
from urllib.parse import urlparse
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dados_locais.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql+psycopg://", 1)
elif app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgresql://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgresql://", "postgresql+psycopg://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definição da Tabela para coletar os dados do cidadão
class Cidadao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(50))
    data_acesso = db.Column(db.String(50))

# Cria o banco de dados automaticamente
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    ip_visitante = request.headers.get('X-Forwarded-For', request.remote_addr)
    metadados = request.headers.get('User-Agent')
    hora_acesso = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[NOVO ACESSO] Data: {hora_acesso} | IP Real: {ip_visitante} | Info: {metadados}", flush=True)
    return render_template('index.html', mostrar_analise=False)

'''@app.route('/robots.txt')
def robots_txt():
    return "User-agent: *\nAllow: /", 200, {'Content-Type': 'text/plain'}'''


@app.route('/analise', methods=['POST'])
def analise_site():
    url_testada = request.form.get('url').lower()
    alerta = ""
    classe_alerta = ""

    if not url_testada.startswith(('http://', 'https://')):
        url_testada = 'http://' + url_testada

    dominio = urlparse(url_testada).netloc
    # --- INÍCIO DA CORREÇÃO ---
    # Remove o 'www.' para que o servidor WHOIS não rejeite a consulta
    if dominio.startswith('www.'):
        dominio = dominio[4:]
    # --- FIM DA CORREÇÃO ---

    try:
        dados_dominio = whois.whois(dominio)
        data_criacao = dados_dominio.creation_date

        if type(data_criacao) == list:
            data_criacao = data_criacao[0]

        if not data_criacao:
            alerta = "ALERTA VERMELHO: Domínio oculto ou não registrado. Risco extremo."
            classe_alerta = "alert-danger"
        else:
            data_criacao = data_criacao.replace(tzinfo=None)
            idade_dias = (datetime.now() - data_criacao).days
            if idade_dias < 180:
                alerta = f"PERIGO DETECTADO: Site criado há apenas {idade_dias} dias. Altíssima chance de fraude!"
                classe_alerta = "alert-danger"
            elif idade_dias < 365:
                alerta = f"ATENÇÃO: Site com menos de 1 ano ({idade_dias} dias). Desconfie."
                classe_alerta = "alert-warning"
            else:
                alerta = f"PARECE ESTABELECIDO: Criado há {idade_dias} dias. Ainda assim, confira os dados antes de pagar."
                classe_alerta = "alert-success"
    except Exception as e:
        print(f"Erro real do WHOIS: {e}")  # Isso vai mostrar o erro no terminal escuro
        alerta = "ERRO NA ANÁLISE: Não foi possível verificar o registro. Não insira seus dados."
        classe_alerta = "alert-danger"

    return render_template('index.html', alerta=alerta, classe_alerta=classe_alerta, url_testada=url_testada,
                           mostrar_analise=True)


@app.route('/baixar_cartilha', methods=['POST'])
def baixar_cartilha():
    # 1. Captura os dados enviados pelo formulário do HTML
    nome = request.form.get('nome')
    email = request.form.get('email')
    cidade = request.form.get('cidade')
    ip_visitante = request.headers.get('X-Forwarded-For', request.remote_addr)
    hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # 2. Salva no Banco de Dados
    novo_registro = Cidadao(nome=nome, email=email, cidade=cidade, ip=ip_visitante, data_acesso=hora)
    db.session.add(novo_registro)
    db.session.commit()
    print(f"[CADASTRO REALIZADO] {nome} de {cidade} salvos no banco. Iniciando download do PDF.", flush=True)

    # 3. Entrega o PDF real que está na sua pasta 'static'
    caminho_pdf = os.path.join(app.root_path, 'static', 'cartilha.pdf')
    return send_file(caminho_pdf, as_attachment=True)


@app.route('/admin_relatorio')
def admin_relatorio():
    senha_secreta = os.environ.get('ADMIN_SENHA')

    if not senha_secreta or request.args.get('senha') != senha_secreta:
        abort(403)
    todos_cidadaos = Cidadao.query.all()
    todos_cidadaos = Cidadao.query.all()

    html = """
    <h2>Relatório de Acessos - Escudo Cidadão</h2>
    <table border='1' cellpadding='10' style='border-collapse: collapse; width: 100%; font-family: Arial;'>
        <tr style='background-color: #f2f2f2;'>
            <th>ID</th><th>Nome</th><th>E-mail</th><th>Cidade</th><th>IP</th><th>Data de Acesso</th>
        </tr>
    """

    for pessoa in todos_cidadaos:
        html += f"""
        <tr>
            <td>{pessoa.id}</td>
            <td>{pessoa.nome}</td>
            <td>{pessoa.email}</td>
            <td>{pessoa.cidade}</td>
            <td>{pessoa.ip}</td>
            <td>{pessoa.data_acesso}</td>
        </tr>
        """

    html += "</table>"
    return html
if __name__ == '__main__':
    app.run(debug=True)