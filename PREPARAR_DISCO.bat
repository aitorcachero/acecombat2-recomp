@echo off
title Ace Combat 2 Recompiled - Preparador Universal de Disco
cd /d "%~dp0"
echo ========================================================
echo   Iniciando Preparador de Disco de Ace Combat 2
echo ========================================================
echo.
py -3 "tools\setup_disc.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error preparando el disco.
    pause
) else (
    echo.
    echo Todo listo. Ya puedes hacer doble clic en JUGAR_ACE_COMBAT_2.bat
    pause
)
