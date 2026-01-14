@echo off
echo Testing Chat REST API
echo.

echo 1. Testing health endpoint...
curl -s http://localhost:8001/health
echo.
echo.

echo 2. Listing conversas (should be empty initially)...
curl -s "http://localhost:8001/api/chat/conversas?user_id=vendedor-1&tipo=vendedor"
echo.
echo.

echo 3. Testing static file (chat.html)...
curl -s -I http://localhost:8001/static/chat.html | findstr "200\|404"
echo.

echo.
echo ===================================
echo Open browser to test WebSocket:
echo http://localhost:8001/static/chat.html
echo ===================================
