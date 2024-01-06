@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Loop through each subdirectory in the current directory
FOR /D %%D IN (torch-server-*) DO (
    REM Check if Torch.cfg exists in the directory
    IF EXIST "%%D\Torch.cfg" (
        REM Use temporary files for the find and replace operation
        SET TEMP_FILE=%%D\temp.cfg

        REM Replace <Autostart>false</Autostart> with <Autostart>true</Autostart>
        powershell -Command "(Get-Content '%%D\Torch.cfg') -replace '<Autostart>false</Autostart>', '<Autostart>true</Autostart>' | Set-Content '%%TEMP_FILE%'"
        MOVE /Y "%%TEMP_FILE%" "%%D\Torch.cfg"

        REM Replace <NoGui>false</NoGui> with <NoGui>true</NoGui>
        powershell -Command "(Get-Content '%%D\Torch.cfg') -replace '<NoGui>false</NoGui>', '<NoGui>true</NoGui>' | Set-Content '%%TEMP_FILE%'"
        MOVE /Y "%%TEMP_FILE%" "%%D\Torch.cfg"

        ECHO Updated Autostart and NoGui in %%D\Torch.cfg
    ) ELSE (
        ECHO Torch.cfg not found in %%D
    )
)

ENDLOCAL
