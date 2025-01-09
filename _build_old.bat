@echo off
set version=2.0.9
set BASE_PATH=D:\My files\projects\current\programming\vayl\vaylbot
set EXE_NAME=Vayl
set ZIP_NAME=Vayl %version%.zip

echo Cleaning up previous builds...
if exist "%BASE_PATH%\%EXE_NAME%.exe" del "%BASE_PATH%\%EXE_NAME%.exe"
if exist "%BASE_PATH%\build" @RD /S /Q "%BASE_PATH%\build"
if exist "%BASE_PATH%\dist" @RD /S /Q "%BASE_PATH%\dist"
if exist "%BASE_PATH%\%ZIP_NAME%" del "%BASE_PATH%\%ZIP_NAME%"

echo Compiling Python script...
pushd "%BASE_PATH%"
py -m PyInstaller vayl.py --icon="%BASE_PATH%\_misc\icon.ico" --name="%EXE_NAME%" --onefile
popd

if not exist "%BASE_PATH%\dist\%EXE_NAME%.exe" (
    echo Compilation failed. Exiting...
    exit /b 1
)

echo Packaging files...
7z a "%ZIP_NAME%" "%BASE_PATH%\dist\%EXE_NAME%.exe" "%BASE_PATH%\_blank\configuration" "%BASE_PATH%\_blank\data"

echo Archiving source and ZIP...
xcopy /y "%BASE_PATH%\vayl.py" "%BASE_PATH%\_archive"
pushd "%BASE_PATH%\_archive"
ren "vayl.py" "vayl %version%.py"
popd
xcopy /y "%ZIP_NAME%" "%BASE_PATH%\_zip"
timeout /t 2 /nobreak > nul

echo Starting cleanup process...

REM Delete the Vayl.spec file
if exist "%BASE_PATH%\Vayl.spec" (
    echo Deleting Vayl.spec...
    del "%BASE_PATH%\Vayl.spec"
)

REM Delete the build folder
if exist "%BASE_PATH%\build" (
    echo Removing build folder...
    @RD /S /Q "%BASE_PATH%\build"
)

REM Delete the dist folder
if exist "%BASE_PATH%\dist" (
    echo Removing dist folder...
    @RD /S /Q "%BASE_PATH%\dist"
)

REM Delete any leftover temporary ZIP file
if exist "%BASE_PATH%\Vayl %version%.zip.tmp" (
    echo Deleting temporary ZIP file...
    del "%BASE_PATH%\Vayl %version%.zip.tmp"
)

echo Cleanup complete.


echo Done!
pause
