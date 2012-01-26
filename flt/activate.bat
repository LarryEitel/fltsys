@echo off

set PYTHON_ROOT=C:\Python27
set PYTHONHOME=%PYTHON_ROOT%
set PRJFLT=C:\Users\Larry\__prjs\flt
set DJANGO_SETTINGS_MODULE=flt.settings

set OSGEO4W_ROOT=C:\OSGeo4W
set GEOS_LIBRARY_PATH=%OSGEO4W_ROOT%\bin
set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
set PROJ_LIB=%OSGEO4W_ROOT%\share\proj
set GEOS_LIBRARY_PATH=%OSGEO4W_ROOT%\bin
set PATH=%PATH%;%OSGEO4W_ROOT%\bin

set PYTHONPATH=%PRJFLT%;%PRJFLT%\parts;%PRJFLT%\ve\Lib;%PRJFLT%\ve\Lib\site-packages;C:\Python27;C:\Python27\Lib;C:\Python27\Lib\site-packages;%GEOS_LIBRARY_PATH%

for %%f in (%OSGEO4W_ROOT%\etc\ini\*.bat) do call %%f

/_envs/flt/Scripts/activate.bat
REM python /_envs/flt/Scripts/activate_this.py

@echo on

@cmd.exe

