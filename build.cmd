cd Source
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q config-path.egg-info

py -3.5 setup.py sdist bdist_wheel %1 %2 %3 %4
cd ..

dir /s /b Source\dist\*.whl
