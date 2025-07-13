#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend files
"""

import os
import sys
import http.server
import socketserver
from urllib.parse import urlparse
import json

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        """Override to inject API configuration into JavaScript files"""
        if self.path == '/config.js':
            # Serve configuration as JavaScript
            api_base_url = os.environ.get('API_BASE_URL', 'http://localhost:8000')
            config_js = f"""
// Configuration injected by server
window.API_CONFIG = {{
    BASE_URL: '{api_base_url}'
}};
"""
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.end_headers()
            self.wfile.write(config_js.encode())
            return
        
        # Default behavior for other files
        super().do_GET()

    def guess_type(self, path):
        """Override to handle additional MIME types"""
        mime_type = super().guess_type(path)
        if path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.html'):
            return 'text/html'
        return mime_type

def run_server(port=3001):
    """Run the HTTP server"""
    # Change to the directory containing the frontend files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    handler = CORSHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🚀 Frontend server running at http://localhost:{port}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Try a different port.")
            print(f"   Example: python server.py {port + 1}")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    port = 3001
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default port 3001")
    
    run_server(port) 