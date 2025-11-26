import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

os.chdir('/Users/carsch18/Desktop/VENTI')

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"🚀 VENTI Search Engine running at:")
    print(f"   http://localhost:{PORT}")
    print(f"\n✨ Opening browser...")
    webbrowser.open(f'http://localhost:{PORT}')
    print(f"\n⌨️  Press Ctrl+C to stop the server\n")
    httpd.serve_forever()
