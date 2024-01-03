@echo off
setlocal enabledelayedexpansion

rem Set the path to the main directory where all Torch server folders are located
set main_directory=%~dp0

rem Check if the main directory exists
if not exist "%main_directory%" (
    echo Main directory does not exist.
    pause
    exit /b
)

rem Iterate through each server folder and update the submodule
for /d %%d in ("%main_directory%\torch-server-starcore-*") do (
    set server_folder=%%~d
    set submodule_dir=!server_folder!\Instance\Saves\StarcoreMTWorld

    rem Check if the server folder exists
    if not exist "!server_folder!" (
        echo Server folder !server_folder! does not exist.
        continue
    )

    rem Check if the submodule directory exists
    if not exist "!submodule_dir!" (
        echo Submodule directory !submodule_dir! does not exist.
        continue
    )

    echo Updating submodule in !server_folder!
    cd "!submodule_dir!"

    rem Check if the .git directory exists within the submodule directory
    if not exist ".git" (
        echo .git directory not found in !submodule_dir!. Make sure it's a Git submodule.
        cd "%main_directory%"
        continue
    )

    git submodule update --init --recursive
    cd "%main_directory%"
)

pause
