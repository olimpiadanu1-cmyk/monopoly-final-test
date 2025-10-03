@echo off
echo ========================================
echo    Monopoly Game - Запуск серверов
echo ========================================
echo.

echo [1/2] Запуск API сервера...
start "API Server" python api_server.py

echo [2/2] Запуск веб-сервера...
start "Web Server" python -m http.server 3000

echo.
echo ✅ Серверы запущены!
echo 📖 Откройте в браузере: http://localhost:3000
echo 💾 Сервер сохранения: http://localhost:5000
echo.
echo Нажмите любую клавишу для выхода...
pause >nul

