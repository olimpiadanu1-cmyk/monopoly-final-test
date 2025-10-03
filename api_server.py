#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Папка для хранения данных
DATA_DIR = 'data'

# Файлы для хранения данных
DATA_FILES = {
    'users': 'users.json',
    'applications': 'applications.json',
    'purchase_requests': 'purchase_requests.json',
    'task_submissions': 'task_submissions.json',
    'reward_history': 'reward_history.json',
    'leaderboard': 'leaderboard.json',
    'cell_tasks': 'cell_tasks.json',
    'game_states': 'game_states.json',
    'shop_items': 'shop_items.json',
    'shopping_carts': 'shopping_carts.json'
}

def load_data(data_type):
    """Загрузить данные из JSON файла"""
    if data_type not in DATA_FILES:
        return None
        
    file_path = os.path.join(DATA_DIR, DATA_FILES[data_type])
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Возвращаем пустые данные по умолчанию
            if data_type in ['users', 'applications', 'purchase_requests', 'task_submissions', 'reward_history', 'leaderboard', 'cell_tasks', 'shop_items']:
                return []
            else:  # game_states, shopping_carts
                return {}
    except Exception as e:
        print(f"Ошибка загрузки {data_type}: {e}")
        return [] if data_type != 'game_states' and data_type != 'shopping_carts' else {}

def save_data(data_type, data):
    """Сохранить данные в JSON файл"""
    if data_type not in DATA_FILES:
        return False
        
    file_path = os.path.join(DATA_DIR, DATA_FILES[data_type])
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено: {data_type} -> {file_path}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения {data_type}: {e}")
        return False

# API для получения данных
@app.route('/api/data/<data_type>', methods=['GET'])
def get_data(data_type):
    """Получить данные определенного типа"""
    try:
        data = load_data(data_type)
        if data is not None:
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': False, 'error': 'Неизвестный тип данных'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API для сохранения данных
@app.route('/api/data/<data_type>', methods=['POST'])
def save_data_endpoint(data_type):
    """Сохранить данные определенного типа"""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'success': False, 'error': 'Нет данных'}), 400
        
        success = save_data(data_type, data)
        if success:
            return jsonify({'success': True, 'message': f'Данные {data_type} сохранены'})
        else:
            return jsonify({'success': False, 'error': 'Ошибка сохранения'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API для получения всех данных сразу
@app.route('/api/all-data', methods=['GET'])
def get_all_data():
    """Получить все данные игры"""
    try:
        all_data = {}
        for data_type in DATA_FILES.keys():
            all_data[data_type] = load_data(data_type)
        
        return jsonify({'success': True, 'data': all_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Проверка статуса
@app.route('/api/status', methods=['GET'])
def get_status():
    """Получить статус сервера"""
    return jsonify({'success': True, 'message': 'API сервер работает'})

if __name__ == '__main__':
    print("Запуск API сервера Monopoly Game...")
    print("Папка для данных:", DATA_DIR)
    print("Файлы данных:", list(DATA_FILES.keys()))
    print("Сервер доступен по адресу: http://localhost:5000")
    print("API документация: http://localhost:5000/api/status")
    
    app.run(host='127.0.0.1', port=5000, debug=False)
