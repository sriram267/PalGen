@echo off
setlocal
title Image End-to-End Analyzer
echo ===================================================
echo           IMAGE END-TO-END ANALYZER (AI)
echo ===================================================
echo.

set SCRIPT_DIR=%~dp0
set TARGET=%~1

if "%TARGET%"=="" (
    echo Drag and drop an image file into this window, then press Enter:
    set /p TARGET="Image Path: "
)

if "%TARGET%"=="" (
    echo Error: No image provided. Exiting.
    pause
    exit /b 1
)

echo.
echo Analyzing: %TARGET%
echo.

where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    uv run --with Pillow python "%SCRIPT_DIR%scripts\image_analyzer.py" "%TARGET%"
) else (
    python "%SCRIPT_DIR%scripts\image_analyzer.py" "%TARGET%"
)

echo.
echo ===================================================
echo Analysis complete. Press any key to exit.
pause >nul
