from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class Application(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"HEALTHY")
            return

        environment = os.getenv("APP_ENV", "UNKNOWN")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        response = f"""
        Application: Jenkins CI/CD Demo
        Environment: {environment}
        Status: Running
        """

        self.wfile.write(response.encode())


server = HTTPServer(("0.0.0.0", 8000), Application)

print("Application started on port 8000")

server.serve_forever()
