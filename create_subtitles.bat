@echo off
REM === Delete old subtitle file if it exists ===
del subtitles.vtt 2>nul

REM === Start creating the new VTT file ===
(
echo WEBVTT
echo.

echo 00:00:00.000 --> 00:00:04.000
echo ^<c.pilot^>Pilot^:^</c^> Bird strike^^! Bird strike^^! Both engines gone^^!
echo.

echo 00:00:04.000 --> 00:00:08.000
echo ^<c.copilot^>Co-Pilot^:^</c^> Oh no^^! We're losing control^^!
echo.

echo 00:00:08.000 --> 00:00:12.000
echo ^<c.pilot^>Pilot^:^</c^> Relax^^! Focus on your instruments. We can handle this.
echo.

echo 00:00:12.000 --> 00:00:16.000
echo ^<c.copilot^>Co-Pilot^:^</c^> Okay, okay okay. I'm trying to stabilize the plane.
echo.

echo 00:00:16.000 --> 00:00:19.000
echo ^<c.pilot^>Pilot^:^</c^> Contact ATC immediately. Declare emergency^^!
echo.

echo 00:00:19.000 --> 00:00:25.000
echo ^<c.copilot^>Co-Pilot^:^</c^> Mayday^^! Mayday^^! Mayday^^! We have lost both engines. We are currently gliding and heading towards Kwesi Andrews Airport. Is runway R3 available^^?
echo.

echo 00:00:25.000 --> 00:00:29.800
echo ^<c.atc^>ATC^:^</c^> Roger that. Flight Quebec Alpha one two three, runway Zero Niner Romeo is clear for immediate landing.
echo.

echo 00:00:29.800 --> 00:00:32.800
echo ^<c.pilot^>Pilot^:^</c^> Attention cabin crew, this is your captain. Brace for impact^^!
echo.

echo 00:00:32.800 --> 00:00:37.800
echo ^<c.cabin^>Cabin Crew^:^</c^> Fasten your seatbelt^^! Brace for impact^^! Brace^^! Brace^^! Brace^^! Brace^^!
echo.

echo 00:00:37.800 --> 00:00:39.800
echo ^<c.pilot^>Pilot^:^</c^> Initiating Flight Bot.
echo.

echo 00:00:39.800 --> 00:00:42.800
echo ^<c.bot^>Flight Bot^:^</c^> Flight Bot activated. Running system diagnostics for 2 seconds.
echo.

echo 00:00:42.800 --> 00:00:47.800
echo ^<c.bot^>Flight Bot^:^</c^> Engines offline. Initiate emergency glide procedure. Maintain heading 180 degrees.
echo.

echo 00:00:47.800 --> 00:00:52.800
echo ^<c.bot^>Flight Bot^:^</c^> Prepare checklist for dual engine failure. Monitor altitude, airspeed, and heading.
echo.

echo 00:00:52.800 --> 00:00:56.800
echo ^<c.bot^>Flight Bot^:^</c^> Communicate with ATC, declare emergency, and request closest landing site.
echo.

echo 00:00:56.800 --> 00:00:59.800
echo ^<c.pilot^>Pilot^:^</c^> Following Flight Bot instructions.
echo.

echo 00:00:59.800 --> 00:01:04.800
echo ^<c.bot^>Flight Bot^:^</c^> Approaching landing zone. Configure flaps and landing gear. Maintain stabilized approach.
echo.

echo 00:01:04.800 --> 00:01:08.800
echo ^<c.bot^>Flight Bot^:^</c^> Touchdown in progress. Reduce throttle and engage braking procedures.
echo.

echo 00:01:08.800 --> 00:01:11.800
echo ^<c.pilot^>Pilot^:^</c^> We have landed successfully. Excellent job.
) > subtitles.vtt

echo ✅ subtitles.vtt created successfully!
start notepad subtitles.vtt
pause
