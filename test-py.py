from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
PORT = 3030

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello World from Python!")

server = HTTPServer((HOST, PORT), HelloHandler)

print(f"Server running on http://{HOST}:{PORT}")

server.serve_forever()
