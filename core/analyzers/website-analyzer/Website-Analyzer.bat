@echo off
setlocal
title Website End-to-End Analyzer
echo ===================================================
echo          WEBSITE END-TO-END ANALYZER (AI)
echo ===================================================
echo.

set SCRIPT_DIR=%~dp0
set TARGET=%~1

if "%TARGET%"=="" (
    echo Enter website URL to audit (e.g. http://localhost:5173 or https://example.com):
    set /p TARGET="Website URL: "
)

if "%TARGET%"=="" (
    echo Error: No URL provided. Exiting.
    pause
    exit /b 1
)

echo.
echo Auditing website: %TARGET%
echo.

node "%SCRIPT_DIR%scripts\website_analyzer.mjs" "%TARGET%"

echo.
echo ===================================================
echo Website audit complete. Press any key to exit.
pause >nul
