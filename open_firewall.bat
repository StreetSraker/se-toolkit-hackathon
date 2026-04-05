@echo off
echo ============================================
echo  Opening firewall ports for JDM Apps
echo ============================================
echo.
echo This script needs administrator rights!
echo.
pause

echo Opening port 5000 (Client)...
netsh advfirewall firewall add rule name="JDM Client Port 5000" dir=in action=allow protocol=TCP localport=5000
netsh advfirewall firewall add rule name="JDM Client Port 5000" dir=out action=allow protocol=TCP localport=5000

echo.
echo Opening port 5001 (Service Center)...
netsh advfirewall firewall add rule name="JDM Admin Port 5001" dir=in action=allow protocol=TCP localport=5001
netsh advfirewall firewall add rule name="JDM Admin Port 5001" dir=out action=allow protocol=TCP localport=5001

echo.
echo ============================================
echo  Done! Ports 5000 and 5001 are now open.
echo ============================================
echo.
echo Your IP address is: 
ipconfig | findstr /i "IPv4"
echo.
echo Client access: http://YOUR_IP:5000
echo Service Center access: http://YOUR_IP:5001
echo.
pause
