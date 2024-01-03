@echo off
setlocal enabledelayedexpansion

for /D %%d in (torch-server-starcore-*) do (
    start "Torch Server - %%d" "%%d\torch.server.exe"
)

