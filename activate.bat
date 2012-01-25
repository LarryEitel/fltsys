@echo off
set OSGEO4W_ROOT=C:\OSGeo4W
set DJANGO_SETTINGS_MODULE=_flt.settings

PATH=%OSGEO4W_ROOT%\bin;%PATH%

PATH=C:\_envs\flt;C:\_envs\flt;C:\_envs\flt\Lib;C:\_envs\flt\Lib\site-packages;C:\Users\Larry;%PATH%


for %%f in (%OSGEO4W_ROOT%\etc\ini\*.bat) do call %%f

/_envs/flt/Scripts/activate.bat

@echo on

@cmd.exe

