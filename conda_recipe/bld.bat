set MENU_DIR=%PREFIX%\Menu
mkdir %MENU_DIR%

copy %RECIPE_DIR%\openQCM.ico %MENU_DIR%
if errorlevel 1 exit 1

copy %RECIPE_DIR%\menu-windows.json %MENU_DIR%\openqcm.json
if errorlevel 1 exit 1

%PYTHON% -m pip install . --no-deps --ignore-installed -vv 
if errorlevel 1 exit 1
