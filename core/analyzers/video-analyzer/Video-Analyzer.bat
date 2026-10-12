@echo off
setlocal
title Video End-to-End Analyzer
echo ===================================================
echo           VIDEO END-TO-END ANALYZER (AI)
echo ===================================================
echo.

set SCRIPT_DIR=%~dp0
set TARGET=%~1

if "%TARGET%"=="" (
    echo Drag and drop a video file (.mp4, .mov, .mkv, .webm) here, then press Enter:
    set /p TARGET="Video Path: "
)

if "%TARGET%"=="" (
    echo Error: No video provided. Exiting.
    pause
    exit /b 1
)

echo.
echo Analyzing video: %TARGET%
echo.

where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    uv run --with Pillow --with faster-whisper python "%SCRIPT_DIR%scripts\video_analyzer.py" "%TARGET%"
) else (
    python "%SCRIPT_DIR%scripts\video_analyzer.py" "%TARGET%"
)

echo.
echo ===================================================
echo Video analysis complete. Press any key to exit.
pause >nul
