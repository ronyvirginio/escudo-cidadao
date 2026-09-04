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
    print(f"[NOVO ACESSO] Data: {hora_acesso} | IP Real: {ip_visitante} | Info: {metadados}", flush=True)-
    return render_template('index.html', mostrar_analise=False)


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


@app.route('/baixar_cartilha')
def baixar_cartilha():
    caminho_arquivo = 'cartilha_seguranca.txt'
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write("=== CARTILHA DE PROTEÇÃO DIGITAL - ESCUDO CIDADÃO ===\n\n")
        f.write("1. O BANCO NÃO LIGA PEDINDO SENHA OU INSTALAÇÃO DE APP.\n")
        f.write("2. DESCONFIE DA URGÊNCIA: Golpistas criam pânico para você não pensar.\n")
        f.write("3. IDADE DO SITE: Desconfie de 'órgãos públicos' em sites recém-criados.\n")
        f.write("4. REGISTRO PERFEITO DE OCORRÊNCIA:\n")
        f.write("   - Tire prints de todas as conversas.\n")
        f.write("   - Salve comprovantes de PIX.\n")
        f.write("   - Anote a URL exata do site falso.\n")
        f.write("   - Não apague nada antes de procurar a delegacia.\n")
    return send_file(caminho_arquivo, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)