@echo off
cls
set python="..\..\bin\python27\app\python.exe"
if not exist %python% (
   echo.
   echo Kann keine Pythoninterpreter in %python% finden.
   echo Programmabbruch
   echo.
   pause
   goto endofPython
   )
title Interaktive Hilfsroutinen
"%python%" -x  .\tools\skeletor\skeletor.py %1 %2 %3 %4 %5 %6 %7 %8
