@echo off
setlocal

:: Navigate to your project directory
cd /d D:\internship_hunting_agent

:: Activate virtual environment
call venv\Scripts\activate.bat

set RETRIES=3
set COUNT=0

:retry_loop
set /a COUNT+=1
echo Attempt #%COUNT%

python main.py --auto --query "remote data science & AI & Machine Learning internships and open source"
if %ERRORLEVEL%==0 (
    echo Script executed successfully.
    goto end
) else (
    echo Script failed with error code %ERRORLEVEL%.
    if %COUNT% GEQ %RETRIES% (
        echo Maximum retries reached. Exiting.
        goto end
    ) else (
        echo Retrying in 10 seconds...
        timeout /t 10 /nobreak >nul
        goto retry_loop
    )
)

:end
endlocal
