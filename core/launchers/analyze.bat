@echo off
setlocal EnableDelayedExpansion
title Multimodal End-to-End Analyzer
echo ===================================================================
echo             UNIVERSAL MULTIMODAL END-TO-END ANALYZER
echo ===================================================================
echo.
echo Select an action:
echo   [1] Analyze Image or Document (PNG, JPG, WebP, PDF)
echo   [2] Analyze Video or Screencast (.mp4, .mov, .webm)
echo   [3] Analyze Website or Web App (localhost or live URL)
echo   [4] Run System Doctor (Verify Installed Binaries)
echo   [5] Exit
echo.
set /p CHOICE="Enter choice (1-5): "

if "%CHOICE%"=="1" (
    echo.
    echo Drag and drop an image file here, then press Enter:
    set /p IMG="Image Path: "
    python "%~dp0analyze.py" image "!IMG!"
    goto DONE
)

if "%CHOICE%"=="2" (
    echo.
    echo Drag and drop a video file here, then press Enter:
    set /p VID="Video Path: "
    python "%~dp0analyze.py" video "!VID!"
    goto DONE
)

if "%CHOICE%"=="3" (
    echo.
    echo Enter website URL (e.g. http://localhost:5173 or https://example.com):
    set /p URL="Website URL: "
    python "%~dp0analyze.py" website "!URL!"
    goto DONE
)

if "%CHOICE%"=="4" (
    python "%~dp0analyze.py" doctor
    goto DONE
)

if "%CHOICE%"=="5" (
    exit /b 0
)

:DONE
echo.
echo ===================================================================
pause
