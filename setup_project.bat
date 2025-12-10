@echo off
echo ===================================================
echo   SETTING UP FUEL THEFT DETECTION PROJECT STRUCT
echo ===================================================

:: 1. Create Root Directory
mkdir FuelTheftProject
cd FuelTheftProject

:: 2. Create Backend (Python)
echo Creating Backend...
mkdir backend
cd backend
type NUL > server.py
type NUL > requirements.txt
echo flask > requirements.txt
echo flask-cors >> requirements.txt
echo scikit-learn >> requirements.txt
echo pandas >> requirements.txt
echo numpy >> requirements.txt
cd ..

:: 3. Create Hardware (Arduino)
echo Creating Hardware folder...
mkdir hardware
cd hardware
mkdir node_code
cd node_code
type NUL > node_code.ino
cd ..
cd ..

:: 4. Create Frontend Folder (Placeholder)
echo Creating Frontend folder...
mkdir frontend

echo ===================================================
echo   DONE! Folder structure created.
echo   NEXT STEP: Open 'frontend' folder and run:
echo   npx create-react-app fuel-dashboard
echo ===================================================
pause