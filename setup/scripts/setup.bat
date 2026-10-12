@echo off
setlocal enabledelayedexpansion
title Universal Multimodal Analysis Suite - Windows Setup
echo ===================================================================
echo     Universal Multimodal Analysis Suite - Windows Setup
echo ===================================================================
echo.

:: Resolve workspace root (two levels up from setup\scripts\)
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%..\.."
set "ROOT_DIR=%CD%"
popd
echo Workspace root: %ROOT_DIR%
echo.

:: ─── Symlink Setup ──────────────────────────────────────────────────────────
echo --- Creating IDE rules symlinks (requires Admin) ---
if not exist "%ROOT_DIR%\.agents\rules" mkdir "%ROOT_DIR%\.agents\rules"
if not exist "%ROOT_DIR%\.cursor\rules" mkdir "%ROOT_DIR%\.cursor\rules"

:: Antigravity / Gemini / Claude rules
for %%F in (AGENTS.md GEMINI.md CLAUDE.md) do (
    if exist "%ROOT_DIR%\setup\rules\%%F" (
        if exist "%ROOT_DIR%\.agents\rules\%%F" del /f "%ROOT_DIR%\.agents\rules\%%F"
        mklink "%ROOT_DIR%\.agents\rules\%%F" "..\..\setup\rules\%%F" >nul 2>&1
        if !ERRORLEVEL! equ 0 (
            echo   [OK] .agents\rules\%%F -- setup\rules\%%F
        ) else (
            copy /y "%ROOT_DIR%\setup\rules\%%F" "%ROOT_DIR%\.agents\rules\%%F" >nul
            echo   [COPY] Copied %%F as fallback.
        )
    )
)

:: Cursor rules
if exist "%ROOT_DIR%\setup\rules\agent-instructions.mdc" (
    if exist "%ROOT_DIR%\.cursor\rules\agent-instructions.mdc" del /f "%ROOT_DIR%\.cursor\rules\agent-instructions.mdc"
    mklink "%ROOT_DIR%\.cursor\rules\agent-instructions.mdc" "..\..\setup\rules\agent-instructions.mdc" >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        echo   [OK] .cursor\rules\agent-instructions.mdc -- setup\rules\agent-instructions.mdc
    ) else (
        copy /y "%ROOT_DIR%\setup\rules\agent-instructions.mdc" "%ROOT_DIR%\.cursor\rules\agent-instructions.mdc" >nul
        echo   [COPY] Copied agent-instructions.mdc as fallback.
    )
)

echo.

:: ─── Skip deps if --symlinks-only ────────────────────────────────────────────
if "%1"=="--symlinks-only" (
    echo ===================================================================
    echo   Symlinks-only mode complete. Skipping dependency installation.
    echo ===================================================================
    pause
    exit /b 0
)

:: ─── Dependency Check ────────────────────────────────────────────────────────
echo --- Checking prerequisite tools ---
echo.

set MISSING=0

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [MISSING] Python ^(install: winget install Python.Python.3.11^)
    set MISSING=1
) else ( echo [OK] Python )

where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [MISSING] Node.js ^(install: winget install OpenJS.NodeJS^)
    set MISSING=1
) else ( echo [OK] Node.js )

where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [MISSING] uv ^(install: winget install astral-sh.uv^)
    set MISSING=1
) else ( echo [OK] uv )

where ffmpeg >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [MISSING] FFmpeg ^(install: winget install Gyan.FFmpeg^)
    set MISSING=1
) else ( echo [OK] FFmpeg )

where tesseract >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [MISSING] Tesseract ^(install: winget install UB-Mannheim.TesseractOCR^)
    set MISSING=1
) else ( echo [OK] Tesseract )

echo.
echo ===================================================================
if %MISSING% neq 0 (
    echo Some tools are missing. Install them with winget (shown above^).
    echo Re-run this script after installation.
) else (
    echo All prerequisites installed! Installing Python dependencies...
    uv pip install Pillow faster-whisper 2>nul || pip install Pillow faster-whisper 2>nul
    echo.
    echo Setup complete! You can now run:
    echo   python core\launchers\analyze.py image  ^<path^>
    echo   python core\launchers\analyze.py video  ^<path^>
    echo   python core\launchers\analyze.py website ^<url^>
    echo   python core\launchers\analyze.py route  "^<your prompt^>"
    echo   python core\launchers\analyze.py doctor
)
echo ===================================================================
pause
