@echo off
set "DIR=%~dp0..\.."
python "%DIR%\master-skiller\scripts\router.py" %*
