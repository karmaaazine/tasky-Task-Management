#!/usr/bin/env python3
"""
Script to start both backend and frontend servers
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting backend server...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"
    ])
    return backend_process

def start_frontend():
    """Start the frontend server"""
    print("🌐 Starting frontend server...")
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return None
    
    frontend_process = subprocess.Popen([
        sys.executable, "server.py"
    ], cwd=frontend_dir)
    return frontend_process

def main():
    """Main function to start both servers"""
    processes = []
    
    try:
        # Start backend
        backend_process = start_backend()
        processes.append(backend_process)
        
        # Wait a bit for backend to start
        time.sleep(2)
        
        # Start frontend
        frontend_process = start_frontend()
        if frontend_process:
            processes.append(frontend_process)
        
        print("\n" + "="*60)
        print("✅ Both servers are running!")
        print("📊 Backend API: http://localhost:8000")
        print("🌐 Frontend Dashboard: http://localhost:3001")
        print("📈 Grafana (if running): http://localhost:3000")
        print("="*60)
        print("\nPress Ctrl+C to stop all servers")
        
        # Wait for processes
        for process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        
        # Terminate all processes
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        print("👋 All servers stopped")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Cleanup processes
        for process in processes:
            try:
                process.terminate()
            except:
                pass
        
        sys.exit(1)

if __name__ == "__main__":
    main() 