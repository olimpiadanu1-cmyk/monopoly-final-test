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

# API для сохранения данных
@app.route('/save/<data_type>', methods=['POST'])
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

# Проверка статуса
@app.route('/status', methods=['GET'])
def get_status():
    """Получить статус сервера"""
    return jsonify({'success': True, 'message': 'Сервер сохранения работает'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # берем порт из переменной окружения, по умолчанию 5000
    print(f"Запуск сервера Monopoly на порту {port}...")
    
    # host="0.0.0.0" чтобы сервер был доступен извне
    app.run(host='0.0.0.0', port=port, debug=False)

