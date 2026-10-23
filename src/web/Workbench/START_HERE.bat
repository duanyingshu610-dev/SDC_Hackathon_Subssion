@echo off
setlocal EnableExtensions
chcp 65001 >nul
title ORBYTE AI Customer Message Workbench v1.4
pushd "%~dp0" >nul 2>nul
if errorlevel 1 goto BADPATH
set "PYEXE="
set "PYARGS="
rem Prefer the user's installed Python 3.14, then fall back to 3.13/3.12.
where py >nul 2>nul
if not errorlevel 1 (
  py -3.14 --version >nul 2>nul
  if not errorlevel 1 (set "PYEXE=py" & set "PYARGS=-3.14")
)
if not defined PYEXE (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3.13 --version >nul 2>nul
    if not errorlevel 1 (set "PYEXE=py" & set "PYARGS=-3.13")
  )
)
if not defined PYEXE (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3.12 --version >nul 2>nul
    if not errorlevel 1 (set "PYEXE=py" & set "PYARGS=-3.12")
  )
)
if not defined PYEXE (
  where python >nul 2>nul
  if not errorlevel 1 (
    python -c "import sys; raise SystemExit(0 if sys.version_info[:2] in ((3,14),(3,13),(3,12)) else 1)" >nul 2>nul
    if not errorlevel 1 (set "PYEXE=python" & set "PYARGS=")
  )
)
if not defined PYEXE goto NOPYTHON
echo [1/3] Detected Python:
%PYEXE% %PYARGS% --version
if errorlevel 1 goto PYERROR
echo.
echo [2/3] Checking pip...
%PYEXE% %PYARGS% -m pip --version
if errorlevel 1 (
  echo pip is unavailable. Trying Python's built-in ensurepip...
  %PYEXE% %PYARGS% -m ensurepip --upgrade
  if errorlevel 1 goto PIPERROR
)
echo.
echo Installing app dependencies. Internet access is required on first run.
%PYEXE% %PYARGS% -m pip install --user --disable-pip-version-check -r "%CD%\requirements.txt"
if errorlevel 1 goto INSTALLERROR
echo.
echo [3/3] Starting the web app...
echo If the browser does not open, visit http://localhost:8501
 echo Keep this window open while using the app. Press Ctrl+C to stop.
%PYEXE% %PYARGS% -m streamlit run "%CD%\app.py"
if errorlevel 1 goto RUNERROR
popd
exit /b 0
:BADPATH
echo ERROR: Cannot open the project folder. Extract the ZIP first.
goto ENDFAIL
:NOPYTHON
echo ERROR: Python 3.12, 3.13, or 3.14 was not found in PATH or the Python launcher.
echo Check that Python 3.14 (64-bit) is installed and available as 'py -3.14' or 'python'.
goto ENDFAIL
:PYERROR
echo ERROR: Python could not run correctly.
goto ENDFAIL
:PIPERROR
echo ERROR: pip could not be initialized. Repair Python 3.14 and enable pip in its installer.
goto ENDFAIL
:INSTALLERROR
echo ERROR: Dependency installation failed. Check internet access and the error above.
goto ENDFAIL
:RUNERROR
echo ERROR: The app did not start. Review the error shown above.
goto ENDFAIL
:ENDFAIL
pause
popd
exit /b 1
