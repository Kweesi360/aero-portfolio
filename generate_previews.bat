@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Set paths
SET "MODEL_DIR=C:\Users\nyame\OneDrive\Desktop\ANDREWS\3RD COMEBACK\Aero Portfolio\models"
SET "PREVIEW_DIR=C:\Users\nyame\OneDrive\Desktop\ANDREWS\3RD COMEBACK\Aero Portfolio\previews"

REM Create previews folder if it doesn't exist
IF NOT EXIST "!PREVIEW_DIR!" mkdir "!PREVIEW_DIR!"

REM List of models
SET MODELS=(
"arm"
"ball_bearing"
"crankshaft"
"drone_2"
"drone_arm"
"drone"
"gate_valve"
"gear_assembly"
"gear"
"gears"
"glider"
"kc_8"
"landing_gear"
"pencil_inspired_aircraft"
"plier"
"predator"
"quadcopter_drone"
"screw_2"
"screw"
"spanner"
"spring"
"top_link"
"torque_wrench"
)

REM Loop through each model
FOR %%M IN %MODELS% DO (
    echo Creating preview for %%M...
    
    REM Input and output paths
    SET "INPUT=!MODEL_DIR!\%%M.mp4"
    SET "OUTPUT=!PREVIEW_DIR!\%%M_preview.mp4"
    
    REM Generate preview: rotate 90° clockwise, first 5 seconds, scale width=320px
    ffmpeg -y -i "!INPUT!" -ss 0 -t 5 -vf "transpose=1,scale=320:trunc(ow/a/2)*2" -b:v 500k -an "!OUTPUT!"
    
    echo Done with %%M
)

echo All previews completed!
pause
