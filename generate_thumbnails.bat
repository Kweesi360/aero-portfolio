@echo off
setlocal enabledelayedexpansion

REM Set paths
set "MODELS_FOLDER=C:\Users\nyame\OneDrive\Desktop\ANDREWS\3RD COMEBACK\Aero Portfolio\models"
set "THUMBNAILS_FOLDER=C:\Users\nyame\OneDrive\Desktop\ANDREWS\3RD COMEBACK\Aero Portfolio\thumbnails"

REM Make sure thumbnails folder exists
if not exist "%THUMBNAILS_FOLDER%" mkdir "%THUMBNAILS_FOLDER%"

REM Loop through video files
for %%F in ("%MODELS_FOLDER%\*.mp4") do (
    set "VIDEO=%%F"
    set "FILENAME=%%~nF"
    set "THUMB_PATH=%THUMBNAILS_FOLDER%\!FILENAME!.jpg"

    REM Check if thumbnail exists
    if exist "!THUMB_PATH!" (
        echo Thumbnail already exists for !FILENAME!, skipping...
    ) else (
        echo Generating thumbnail for !FILENAME!...
        ffmpeg -y -i "!VIDEO!" -ss 00:00:02 -vframes 1 -update 1 "!THUMB_PATH!"
    )
)

echo Done!
pause
