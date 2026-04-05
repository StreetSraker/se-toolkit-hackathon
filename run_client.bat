@echo off
echo ============================================
echo  JDM Client Website
echo ============================================
echo.
echo Starting client application...
echo Website will be available at: http://localhost:5000
echo.
cd /d %~dp0web
C:\Users\kim84\AppData\Local\Programs\Python\Python313\python.exe client_app.py
pause
