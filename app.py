from flask import Flask, render_template, request, send_file
import whois
from datetime import datetime
from urllib.parse import urlparse
import os

app = Flask(__name__)


@app.route('/')
def index():
    ip_visitante = request.headers.get('X-Forwarded-For', request.remote_addr)
    metadados = request.headers.get('User-Agent')
    hora_acesso = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[NOVO ACESSO] Data: {hora_acesso} | IP Real: {ip_visitante} | Info: {metadados}", flush=True)
    return render_template('index.html', mostrar_analise=False)


@app.route('/analise', methods=['POST'])
def analise_site():
    url_testada = request.form.get('url').lower()
    alerta = ""
    classe_alerta = ""

    if not url_testada.startswith(('http://', 'https://')):
        url_testada = 'http://' + url_testada

    dominio = urlparse(url_testada).netloc
    from flask import Flask, render_template, request, send_file
    import whois
    from datetime import datetime
    from urllib.parse import urlparse
    import os
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)

    #  Banco de Dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dados_locais.db')
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://",
                                                                                              "postgresql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)

    # Tabela do Banco
    class Cidadao(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(150), nullable=False)
        email = db.Column(db.String(150), nullable=False)
        cidade = db.Column(db.String(100), nullable=False)
        ip = db.Column(db.String(50))
        data_acesso = db.Column(db.String(50))

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        ip_visitante = request.headers.get('X-Forwarded-For', request.remote_addr)
        metadados = request.headers.get('User-Agent')
        hora_acesso = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"[NOVO ACESSO] Data: {hora_acesso} | IP Real: {ip_visitante} | Info: {metadados}", flush=True)
        return render_template('index.html', mostrar_analise=False)

    @app.route('/analise', methods=['POST'])
    def analise_site():
        url_testada = request.form.get('url').lower()
        alerta = ""
        classe_alerta = ""

        if not url_testada.startswith(('http://', 'https://')):
            url_testada = 'http://' + url_testada

        dominio = urlparse(url_testada).netloc
        if dominio.startswith('www.'):
            dominio = dominio[4:]

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
                    alerta = f"PARECE ESTABELECIDO: Criado há {idade_dias} dias. Ainda assim, confira os dados."
                    classe_alerta = "alert-success"
        except Exception as e:
            print(f"Erro real do WHOIS: {e}")
            alerta = "ERRO NA ANÁLISE: Não foi possível verificar o registro."
            classe_alerta = "alert-danger"

        return render_template('index.html', alerta=alerta, classe_alerta=classe_alerta, url_testada=url_testada,
                               mostrar_analise=True)

    # Salva no Banco e entrega o PDF
    @app.route('/baixar_cartilha', methods=['POST'])
    def baixar_cartilha():
        nome = request.form.get('nome')
        email = request.form.get('email')
        cidade = request.form.get('cidade')
        ip_visitante = request.headers.get('X-Forwarded-For', request.remote_addr)
        hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Salva na tabela
        novo_registro = Cidadao(nome=nome, email=email, cidade=cidade, ip=ip_visitante, data_acesso=hora)
        db.session.add(novo_registro)
        db.session.commit()
        print(f"[DADOS SALVOS] {nome} de {cidade} baixou a cartilha em PDF.", flush=True)

        # Envia o PDF real
        caminho_pdf = os.path.join(app.root_path, 'static', 'cartilha.pdf')
        return send_file(caminho_pdf, as_attachment=True)

    if __name__ == '__main__':
        app.run(debug=True)