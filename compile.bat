rmdir /S /Q dist
mkdir dist
robocopy ./fonts/ ./dist/fonts/ /s /e
robocopy ./images/ ./dist/images/ /s /e
robocopy ./levels/ ./dist/levels/ /s /e
python setup.py py2exe
pause