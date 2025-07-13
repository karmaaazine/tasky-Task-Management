@echo off

echo 🐳 Building and running Tasky Frontend with Docker...

REM Build the Docker image
echo 📦 Building Docker image...
docker build -t tasky-frontend .

REM Run the container
echo 🚀 Starting frontend container...
docker run -d ^
  --name tasky-frontend ^
  --rm ^
  -p 3001:3001 ^
  -e API_BASE_URL=http://localhost:8000 ^
  tasky-frontend

echo.
echo ✅ Frontend is running!
echo 🌐 Frontend URL: http://localhost:3001
echo 📊 Make sure backend is running on: http://localhost:8000
echo.
echo To stop the container:
echo   docker stop tasky-frontend
echo.
echo To view logs:
echo   docker logs -f tasky-frontend

pause 