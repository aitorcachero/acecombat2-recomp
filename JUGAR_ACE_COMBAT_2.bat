@echo off
cd /d "%~dp0"

:: 1. Lanzar el ejecutable nativo silencioso si existe
if exist "AceCombat2.exe" (
    start "" "AceCombat2.exe"
    exit /b
)
if exist "build-release\AceCombat2.exe" (
    start "" "build-release\AceCombat2.exe"
    exit /b
)

:: 2. Si se ejecuta desde el hub raíz
if exist "ace-combat-2-recomp\AceCombat2.exe" (
    cd /d "%~dp0ace-combat-2-recomp"
    start "" "AceCombat2.exe"
    exit /b
)

:: 3. Lanzar runtime directo si aplica
set PSX_RENDER_THREAD=1
set PSX_PRESENT_THREAD=1
set PSX_FRAME_GEN=0
set PSX_FRAME_INTERPOLATION=0
set PSX_VSYNC=0
set PSX_FPS_TELEMETRY=0
set PSX_WS_FORCE_FULLSCREEN=1
set PSX_WS_FORCE_3D=1
set PSX_WS_FORCE_2D=0
set PSX_ASPECT_RATIO=16:9
set PSX_INTERNAL_SCALE=8
if exist "Ace_Combat_2_Recompiled.exe" (
    start "" "Ace_Combat_2_Recompiled.exe"
) else if exist "build-release\Ace_Combat_2_Recompiled.exe" (
    cd /d "%~dp0build-release"
    start "" "Ace_Combat_2_Recompiled.exe"
)
exit /b
