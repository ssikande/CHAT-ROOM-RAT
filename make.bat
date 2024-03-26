@echo off

start cmd.exe /k "python server.py 127.0.0.1 44444"

for /L %%a in (1,1,2) do (
  start cmd.exe /k "python client.py 127.0.0.1 44444"
)
pause
