from flask import Flask, jsonify, request, url_for
import sqlite3
import subprocess
import repository
import json

app = Flask(__name__)

@app.get('/pedido')
def pedido_get():
    return repository.getAllPedidos()

@app.route('/pedido/<numero>', methods=['GET'])
def get_pedido(numero):
    return repository.getPedido(numero)

@app.route('/pedido/', methods=['POST'])
def insert_pedido():
    data = request.get_json()
    response = repository.insertPedido(data)

    return jsonify(success=response)

@app.route('/pedido/<numero>/item', methods=['GET'])
def get_item_pedido(numero):
    return jsonify(repository.get_item_pedido(numero))

@app.route('/pedido/<numero>/item', methods=['POST'])
def insert_item_pedido(numero):
    data = request.get_json()
    for x in data:
        print(x)
        print(data[x])
    
    repository.insertItemPedido(numero, data)
    return ""



app.run()