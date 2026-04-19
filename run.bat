@echo off
echo.
echo  Hermes Runner
echo  =============
echo.
echo  Available workflows:
echo    1. WF-01  Demand Signal Refresh
echo    2. WF-02  Supply Plan Generation
echo    3. WF-03  Protocol Amendment Impact
echo    4. WF-04  Routine Monitoring
echo    5. WF-05  Supply Plan Execution
echo.

set /p "WF=  Enter workflow number (1-5): "
set /p "STUDY=  Enter study ID: "
set /p "DROP=  Enter data drop date (YYYY-MM-DD, or press Enter for latest): "

if "%WF%"=="1" set "WFID=WF-01"
if "%WF%"=="2" set "WFID=WF-02"
if "%WF%"=="3" set "WFID=WF-03"
if "%WF%"=="4" set "WFID=WF-04"
if "%WF%"=="5" set "WFID=WF-05"

if not defined WFID (
    echo.
    echo  ERROR: Invalid workflow number. Enter 1-5.
    pause
    exit /b 1
)

if "%STUDY%"=="" (
    echo.
    echo  ERROR: Study ID is required.
    pause
    exit /b 1
)

echo.
echo  Running %WFID% for study %STUDY%...
echo.

REM Load ANTHROPIC_API_KEY from .env file
for /f "usebackq tokens=* delims=" %%a in (.env) do (
    if not "%%a"=="" (
        setlocal enabledelayedexpansion
        set "line=%%a"
        if "!line:~0,18!"=="ANTHROPIC_API_KEY=" (
            set "ANTHROPIC_API_KEY=!line:~18!"
            set "ANTHROPIC_API_KEY=!ANTHROPIC_API_KEY:"=!"
        )
        endlocal & set "ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY%"
    )
)

if "%DROP%"=="" (
    python runner/runner.py --workflow %WFID% --study %STUDY%
) else (
    python runner/runner.py --workflow %WFID% --study %STUDY% --data-drop %DROP%
)

echo.
pause
