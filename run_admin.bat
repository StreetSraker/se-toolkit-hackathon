@echo off
echo ============================================
echo  JDM Service Center Website
echo ============================================
echo.
echo Starting admin application...
echo Website will be available at: http://localhost:5001
echo.
cd /d %~dp0web
C:\Users\kim84\AppData\Local\Programs\Python\Python313\python.exe admin_app.py
pause
