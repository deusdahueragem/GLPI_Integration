from flask import Flask, render_template, request, redirect, url_for
import os, requests, json

app = Flask(__name__)

#VERIFICA O LOGIN
@app.route("/", methods=["GET", "POST"])
def check_login():
    session_path = "./static/info/session.json"
    if os.path.isfile(session_path):
        return render_template("index.html")
    else:
        return redirect(url_for("login"))
    
@app.route("/logoff", methods=["GET"])
def logoff():
    app_token = ""
    session_path = "./static/info/session.json"
    app_token_path = "./static/info/app_token"

    if os.path.isfile(session_path) and os.path.isfile(app_token_path):
        with open (app_token_path, "r") as apptkn:
            app_token = apptkn.read()
            apptkn.close

        with open(session_path) as token:
            tkn = json.load(token)
            session_token = tkn['session_token']
            print(session_token)
            print(app_token)
            url = f"http://192.168.0.100/glpi/apirest.php/killSession/?session_token={session_token}&app_token={app_token}"
            payload={}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.status_code)
            token.close
        os.remove(session_path)
        os.remove(app_token_path)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    session_path = "./static/info/session.json"
    app_token_path = "./static/info/app_token"

    if request.method == "POST":
        
        user = request.form['username']
        pwd = request.form['password']
        app_token = request.form['token']
        #FAZ A REQUISICAO DO SESSION TOKEN
        url = f"http://192.168.0.100/glpi/apirest.php/initSession/?app_token={app_token}"
        payload={}
        headers = {
        'Authorization': 'Basic ZWR1YXJkbzozNDAxNDE1NA=='
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        sessiontoken = response.text

        #GUARDA O SESSION TOKEN
        with open(session_path, 'w') as login:
            login.write(sessiontoken)
            login.close
        with open (app_token_path, 'w') as tokenapp:
            tokenapp.write(app_token)
            tokenapp.close
        return render_template("index.html")
    elif request.method == "GET":
        if os.path.isfile(session_path) and os.path.isfile(app_token_path):
            return redirect(url_for("logoff"))
        else:
            return render_template("login.html")

        
#VERIFICA SE O TOKEN EXISTE
#@app.route("/check_config", methods=["GET"])
#def check_config():
#    #CAMINHO DO API TOKEN
#    config_path = "./static/info/api_token"
#    #VERIFICA SE O ARQUIVO EXISTE
#    if os.path.isfile(config_path):
#        return render_template("index.html")
#    #CASO NÃO EXISTA CRIA O ARQUIVO
#    else:
#        return redirect(url_for('create_config'))

#CRIA TOKEN
#@app.route("/config", methods=["GET", "POST"])
#def create_config():
#    if request.method == "POST":
#        config_path = "./static/info/api_token"
#        apitoken = request.form['token']
#        with open(config_path, 'w') as create_config:
#            create_config.write(apitoken)
#            create_config.close
#        return redirect(url_for('check_config'))
#    return render_template("create_config.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)