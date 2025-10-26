@echo off
REM ==========================================
REM Step 0: Go to your project folder
REM ==========================================
cd /d "D:\Desktop\ANDREWS\3RD COMEBACK\Aero Portfolio"

REM ==========================================
REM Step 1: Make sure temp folder exists
REM ==========================================
if not exist voices\temp mkdir voices\temp

REM ==========================================
REM Step 2: Copy ATC voice to temp folder
REM ==========================================
copy /y "voices\atc\voice_6_ATC_radio.mp3" "voices\temp\voice_6_ATC.wav"

REM ==========================================
REM Step 3: Concatenate using filter_complex
REM This avoids timestamp issues entirely
REM ==========================================
ffmpeg -y ^
-i "voices\temp\static_start_6.wav" ^
-i "voices\temp\voice_6_ATC.wav" ^
-i "voices\temp\static_end_6.wav" ^
-filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]" ^
-map "[out]" -c:a libmp3lame -b:a 192k "voices\temp\voice_6_ATC_final.mp3"

echo.
echo ==========================================
echo All done! Your final MP3 is in voices\temp
echo ==========================================
pause
