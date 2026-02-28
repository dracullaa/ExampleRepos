from flask import Flask
import requests
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World! 🎉"

@app.route('/status')
def status():
    return {"status": "OK", "message": "Application is running"}

if __name__ == '__main__':
    app.run(debug=True)