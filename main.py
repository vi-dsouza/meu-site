from calendar import c
from django.shortcuts import redirect
from flask import Flask, render_template, request, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from grpc import server
from py import log
from tkinter import messagebox

#Carregando as variaveis de ambiente do arquivo .env
load_dotenv()

# __name__ representa o arquivo atual (aplicacap da web)
app = Flask(__name__)
# representa a pagina padrao

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/servico")
def servico():
    return render_template("servico.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/menssagem_sucesso")
def sucesso_menssagem():
    return render_template("menssagem_sucesso.html")

@app.route("/submit", methods=['POST'])
def submit():
    #pego as informações do formulario
    nome = request.form['nome']
    email = request.form['email']
    titulo = request.form['titulo']
    mensagem = request.form['mensagem']

    corpo_email = f"Nome: {nome}\n\nEmail: {email}\n\nTitulo: {titulo}\n\nMensagem: {mensagem}"

    
    #Acessando as variaveis de ambiente
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')

    if not email_user or not email_password:
        return "Erro: As credenciais de email não foram configuradas corretamente."

    msg = MIMEMultipart()
    msg['Subject'] = "Contato do site"
    msg['From'] = email
    msg['To'] = email_user

    msg.attach(MIMEText(corpo_email, 'plain'))

    try:
        #Configurando o servidor de email
        server = smtplib.SMTP('smtp.gmail.com',  587)
        server.starttls()

        #logando no servidor
        server.login(email_user, email_password)

        #enviando o email
        server.sendmail(email, [msg['To']], msg.as_string())

        #encerrando a conexao com o servidor
        server.quit()

        return sucesso_menssagem()

    except smtplib.SMTPAuthenticationError:
        return "Falha na autenticação. Verifique as credenciais ou a configuração da conta."
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"
    

# ao executar o script o python atribui o nome __main__ ao script quando ele e executado
# se importamos outro script, a instrucao if evitara que outros scripts sejam executados

if __name__ == "__main__":
    #executara a aplicaçao, permite que os erros aparecam na pagina web, ajudando a identificar os erros
    app.run(debug=True)