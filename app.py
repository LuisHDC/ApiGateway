from flask import Flask, jsonify, request, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import sqlite3
import subprocess
import repository
import json

app = Flask(__name__)
app.secret_key = 'chave_secreta_api_gateway_123'

login_manager = LoginManager()
login_manager.init_app(app)

class Usuario(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return Usuario(user_id)

@app.get('/login')
def loginUser():
    user = Usuario(1)
    login_user(user)
    return 'Autenticado com sucesso'

@app.route('/logout')
@login_required
def logoutUser():
    logout_user()
    return 'Deslogado com sucesso'



@app.route('/transformaPayload', methods=['POST'])
def transformacao():
    if request.json:
        novo_payload = transformar(request.json)
        return jsonify(novo_payload)
    else:
        return 'Nenhum payload JSON encontrado', 400

def transformar(payload):
    # Implemente sua lógica de transformação aqui
    return {k.lower(): v for k, v in payload.items()}


@app.get('/pedido')
@login_required
def pedido_get():
    return repository.getAllPedidos()

@app.route('/pedido/<numero>', methods=['GET'])
@login_required
def get_pedido(numero):
    return repository.getPedido(numero)

@app.route('/pedido/', methods=['POST'])
@login_required
def insert_pedido():
    data = request.get_json()
    response = repository.insertPedido(data)

    return jsonify(success=response)

@app.route('/pedido/<numero>/item', methods=['GET'])
@login_required
def get_item_pedido(numero):
    return jsonify(repository.get_item_pedido(numero))

@app.route('/pedido/<numero>/item', methods=['POST'])
@login_required
def insert_item_pedido(numero): 
    data = request.get_json()

    response = repository.insertItemPedido(numero, data)
    
    if "erro" in response:
        return jsonify(failure=response["erro"])
    
    return jsonify(success=True)



app.run()