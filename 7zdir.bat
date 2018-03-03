   @echo off
rem   Komprimiert den aktuellen Ordner in ein Zip File
rem
   set prjname=pymframe-1.1
   echo.
   echo BACKUP Verzeichnis
   echo.
   echo es wird ein Archiv mit Namen %prjname%.zip erzeugt
   echo.

   set zip="%cd%\..\..\bin\7zip\7z"
:start
   set function=%prjname%   
   echo.
   echo Funktionen
   echo b: Backup  (ZIP Format)
   echo s: Backup Filenname mit Datum  (ZIP Format)
   echo 7: Backup   (7Zip Format)
   echo r: restore
   echo r7: restore
   echo.
   echo x: beenden
   echo.
   set/P function=Wahl:

   if "%function%" == "b" goto backup
   if "%function%" == "s" goto save
   if "%function%" == "7" goto backup7z
   if "%function%" == "r" goto restore
   if "%function%" == "r7" goto restore7z
   if "%function%" == "x" goto exit

   echo.
   echo ungueltige Eingabe %function%
   goto start

:backup
   %zip% >zip.log a  -r -tzip %prjname%.zip *.* -x!%prjname%.zip -x!distribution/ -x!%prjname%.7z -x!zip.log
   echo "DONE"
   pause
   goto exit

:save
   rem Datum und Uhrzeit zusammenbauen
   set hh=%time:~0,2%
   if "%time:~0,1%"==" " set hh=0%hh:~1,1%

   set datetime=%date:~6,4%-%date:~3,2%-%date:~0,2%_%hh%T%time:~3,2%%

   %zip%  a  -r -tzip %prjname%-%datetime%.zip *.* -x!%prjname%-%datetime%.zip -x!%prjname%.zip
   goto exit


:backup7z
   %zip%  a  -r -t7z %prjname% *.* -x!%prjname%.zip  -x!distribution/ -x!%prjname%.7z
   goto exit

:restore
   %zip% >NUL: -aoa x  %prjname%.zip
   goto exit

:restore7z
   %zip%  x  %prjname%.7z
   goto exit

:exit
