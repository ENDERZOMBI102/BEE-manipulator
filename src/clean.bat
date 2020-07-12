@ECHO OFF
rmdir logs /S /Q
rmdir __pycache__ /S /Q
del assets\database.json
del assets\about.html
del config.cfg