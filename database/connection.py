import mysql.connector

from config import DB_CONFIG

def conectar():
    conexao = mysql.connector.connect(**DB_CONFIG)
    return conexao