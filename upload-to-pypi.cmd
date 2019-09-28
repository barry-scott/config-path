setlocal
set PY=py -3.7
set TWINE_USERNAME=barryscott

%PY% -m twine check dist\*
if errorlevel 1 goto :eof
%PY% -m twine upload dist\*
endlocal
