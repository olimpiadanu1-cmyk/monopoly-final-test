#!/bin/bash

echo "========================================"
echo "   Monopoly Game - Запуск серверов"
echo "========================================"
echo

echo "[1/2] Запуск API сервера..."
python3 api_server.py &
API_PID=$!

sleep 2

echo "[2/2] Запуск веб-сервера..."
python3 -m http.server 3000 &
WEB_PID=$!

echo
echo "✅ Серверы запущены!"
echo "📖 Откройте в браузере: http://localhost:3000"
echo "💾 Сервер сохранения: http://localhost:5000"
echo
echo "Нажмите Ctrl+C для остановки серверов"

# Функция для остановки серверов
cleanup() {
    echo
    echo "Остановка серверов..."
    kill $API_PID $WEB_PID 2>/dev/null
    echo "Серверы остановлены."
    exit 0
}

# Обработка сигнала прерывания
trap cleanup SIGINT

# Ожидание
wait

