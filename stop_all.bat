@echo off
echo ============================================
echo  Stopping all JDM Applications
echo ============================================
echo.

echo Stopping Python processes...
taskkill /F /IM python.exe

if %errorlevel% equ 0 (
    echo.
    echo Success: All applications stopped.
) else (
    echo.
    echo No running applications found.
)

echo.
pause
