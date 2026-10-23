@echo off
setlocal
chcp 65001 >nul
title SDC Hackathon Submission
cd /d "%~dp0"

:MENU
echo.
echo =============================================
echo   SDC Hackathon Submission - 项目启动菜单
echo =============================================
echo 1. 启动交互式工作台 (Streamlit)
echo 2. 打开 Sample 模拟消息网页 (无需 API)
echo 3. 运行独立后端逻辑演示
echo 4. 打开 Empty 空白网页原型
echo 5. 打开项目说明
echo 0. 退出
set /p choice=请选择 [0-5]: 

if "%choice%"=="1" goto WEB
if "%choice%"=="2" goto SAMPLE
if "%choice%"=="3" goto DEMO
if "%choice%"=="4" goto EMPTY
if "%choice%"=="5" goto README
if "%choice%"=="0" goto END
echo 无效选项，请重新选择。
goto MENU

:WEB
call "%~dp0web\Workbench\START_HERE.bat"
goto MENU

:SAMPLE
start "" "%~dp0web\Sample\index.html"
goto MENU

:DEMO
where py >nul 2>nul
if not errorlevel 1 (py "%~dp0run_demo.py") else (python "%~dp0run_demo.py")
pause
goto MENU

:EMPTY
start "" "%~dp0web\Empty\index.html"
goto MENU

:README
start "" "%~dp0..\README.md"
goto MENU

:END
endlocal
