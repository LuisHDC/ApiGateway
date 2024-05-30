import os
from flask import Flask, jsonify, request
import repository

app = Flask(__name__)
app.secret_key = 'chave_secreta_api_gateway_123'

repository.create_tables()
repository.populate_tables()

@app.get('/api/v1/pedido')
def pedido_get():
    return repository.getAllPedidos()

@app.route('/api/v1/pedido/<numero>', methods=['GET'])
def get_pedido(numero):
    return repository.getPedido(numero)

@app.route('/api/v1/pedido', methods=['POST'])
def insert_pedido():
    data = request.get_json()
    response = repository.insertPedido(data)

    return jsonify(success="O cliente " + data["cliente"] + " foi adicionado com sucesso!" )

@app.route('/api/v1/pedido/<numero>/item', methods=['GET'])
def get_item_pedido(numero):
    return jsonify(repository.get_item_pedido(numero))

@app.route('/api/v1/pedido/<numero>/item', methods=['POST'])
def insert_item_pedido(numero): 
    data = request.get_json()

    response = repository.insertItemPedido(numero, data)
    
    if "erro" in response:
        return jsonify(failure=response["erro"])
    
    return jsonify(success="O Produto " + data["produto"] + " foi adicionado com sucesso ao pedido de numero " + numero + "!")



app.run(host='0.0.0.0', port=5000)

os.remove('./pedidos.db')