@echo off
title "TWINKU core & UI Launcher"
cd /d "c:\Users\ADMIN\Downloads\AI-Desktop-Assistant-Open-Any-App-with-Voice-Text-Python-PowerShell-CMD--main\AI-Desktop-Assistant-Open-Any-App-with-Voice-Text-Python-PowerShell-CMD--main\jarvis-ui"
start cmd /k "npm run dev"
ping 127.0.0.1 -n 6 > nul
cd /d "c:\Users\ADMIN\Downloads\AI-Desktop-Assistant-Open-Any-App-with-Voice-Text-Python-PowerShell-CMD--main\AI-Desktop-Assistant-Open-Any-App-with-Voice-Text-Python-PowerShell-CMD--main\ai0\ai0"
set PYTHONIOENCODING=utf-8
python main.py --startup
