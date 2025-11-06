@echo off
REM Automatic PowerPoint Conversion Script
REM This will convert the markdown presentation to PowerPoint

echo.
echo ============================================================
echo   Sales Command Center - PowerPoint Conversion
echo ============================================================
echo.

REM Check if Pandoc is installed
pandoc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pandoc is not installed.
    echo.
    echo OPTION 1: Install Pandoc automatically
    echo ------------------------------------------
    echo Download from: https://pandoc.org/installing.html
    echo.
    echo After installing, run this script again.
    echo.
    pause
    start https://pandoc.org/installing.html
    exit /b 1
)

echo ✓ Pandoc found!
echo.

REM Check which presentation to convert
echo Which presentation would you like to convert?
echo.
echo [1] AI Game Changer Presentation (14 slides - Recommended)
echo [2] Original Sales Pitch Presentation (20 slides)
echo [3] Both presentations
echo.
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto convert_game_changer
if "%choice%"=="2" goto convert_sales_pitch
if "%choice%"=="3" goto convert_both
goto invalid_choice

:convert_game_changer
echo.
echo Converting AI Game Changer Presentation...
pandoc AI_GAME_CHANGER_PRESENTATION.md -o SalesCommandCenter_GameChanger.pptx
if %errorlevel% equ 0 (
    echo ✓ Successfully created: SalesCommandCenter_GameChanger.pptx
    echo.
    echo Opening PowerPoint...
    start SalesCommandCenter_GameChanger.pptx
) else (
    echo ✗ Conversion failed
)
goto end

:convert_sales_pitch
echo.
echo Converting Original Sales Pitch Presentation...
pandoc SALES_PITCH_PRESENTATION.md -o SalesCommandCenter_SalesPitch.pptx
if %errorlevel% equ 0 (
    echo ✓ Successfully created: SalesCommandCenter_SalesPitch.pptx
    echo.
    echo Opening PowerPoint...
    start SalesCommandCenter_SalesPitch.pptx
) else (
    echo ✗ Conversion failed
)
goto end

:convert_both
echo.
echo Converting both presentations...
echo.
echo [1/2] Converting AI Game Changer Presentation...
pandoc AI_GAME_CHANGER_PRESENTATION.md -o SalesCommandCenter_GameChanger.pptx
if %errorlevel% equ 0 (
    echo ✓ SalesCommandCenter_GameChanger.pptx created
) else (
    echo ✗ Failed to create GameChanger presentation
)

echo.
echo [2/2] Converting Original Sales Pitch...
pandoc SALES_PITCH_PRESENTATION.md -o SalesCommandCenter_SalesPitch.pptx
if %errorlevel% equ 0 (
    echo ✓ SalesCommandCenter_SalesPitch.pptx created
) else (
    echo ✗ Failed to create SalesPitch presentation
)

echo.
echo Opening both presentations...
start SalesCommandCenter_GameChanger.pptx
timeout /t 2 /nobreak >nul
start SalesCommandCenter_SalesPitch.pptx
goto end

:invalid_choice
echo.
echo Invalid choice. Please run the script again and choose 1, 2, or 3.
goto end

:end
echo.
echo ============================================================
echo   Conversion Complete!
echo ============================================================
echo.
echo NEXT STEPS:
echo 1. Open the generated PowerPoint file(s)
echo 2. Choose a professional theme (Design tab)
echo 3. Add your company logo
echo 4. Customize colors and fonts
echo 5. Add images and charts
echo 6. Review and refine
echo.
echo TIP: See CONVERT_TO_POWERPOINT.md for detailed formatting guide
echo TIP: See POWERPOINT_SLIDE_CONTENT.md for copy-paste content
echo.
pause
