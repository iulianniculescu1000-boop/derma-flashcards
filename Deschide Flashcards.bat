@echo off
cd /d "%~dp0"
echo ================================================
echo   Flashcards Dermatologie
echo ================================================
echo.
echo Pornesc aplicatia... se va deschide in browser.
echo.
echo NU inchide aceasta fereastra cat timp folosesti
echo aplicatia. Cand ai terminat, inchide fereastra.
echo.

rem deschide browserul dupa 2 secunde (timp sa porneasca serverul)
start "" /min cmd /c "timeout /t 2 >nul & start http://localhost:8123"

rem porneste serverul (python 3)
python -m http.server 8123
