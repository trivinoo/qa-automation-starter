from http.server import HTTPServer, BaseHTTPRequestHandler
import json

USERS = {
    "student@test.com": {"password": "Password123!", "name": "QA Student"}
}

ITEMS = [
    {"id": 1, "name": "Laptop Pro", "price": 1299.99, "stock": 5},
    {"id": 2, "name": "Wireless Mouse", "price": 29.99, "stock": 20},
    {"id": 3, "name": "Mechanical Keyboard", "price": 89.99, "stock": 12}
]

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>QA Playground & Demo App</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }
    .card { background: #1e293b; padding: 1.5rem; border-radius: 8px; max-width: 480px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    input { width: 100%; box-sizing: border-box; padding: 0.6rem; margin: 0.5rem 0; border-radius: 4px; border: 1px solid #475569; background: #0f172a; color: #fff; }
    button { background: #3b82f6; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; }
    button:hover { background: #2563eb; }
    .success { color: #4ade80; margin-top: 0.5rem; font-weight: bold; }
    .error { color: #f87171; margin-top: 0.5rem; font-weight: bold; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #334155; padding: 8px; text-align: left; }
    th { background: #334155; }
  </style>
</head>
<body>
  <h1>QA Playground - System Under Test (SUT)</h1>
  <p>Local sandbox application for UI, Mobile, and API automated tests.</p>

  <div class="card" id="login-container">
    <h2>Student Login</h2>
    <input type="text" id="username" placeholder="Username / Email" data-testid="username-input" />
    <input type="password" id="password" placeholder="Password" data-testid="password-input" />
    <button id="login-btn" data-testid="login-button" onclick="performLogin()">Log In</button>
    <div id="login-message" data-testid="status-message"></div>
  </div>

  <div class="card" id="catalog-container">
    <h2>Product Catalog (API Driven)</h2>
    <table id="product-table" data-testid="products-table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Price</th><th>Stock</th></tr>
      </thead>
      <tbody id="table-body"></tbody>
    </table>
  </div>

  <script>
    async function performLogin() {
      const u = document.getElementById('username').value;
      const p = document.getElementById('password').value;
      const msg = document.getElementById('login-message');
      
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: u, password: p })
      });
      const data = await res.json();
      if (res.ok) {
        msg.className = 'success';
        msg.innerText = 'Login successful! Welcome, ' + data.user;
      } else {
        msg.className = 'error';
        msg.innerText = data.error || 'Authentication failed.';
      }
    }

    async function loadProducts() {
      const res = await fetch('/api/products');
      const items = await res.json();
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = items.map(i => `<tr><td>${i.id}</td><td>${i.name}</td><td>$${i.price}</td><td>${i.stock}</td></tr>`).join('');
    }
    loadProducts();
  </script>
</body>
</html>
"""

class SimpleQAHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        elif self.path == '/api/health':
            self._send_json(200, {"status": "healthy", "service": "QA Demo Server"})
        elif self.path == '/api/products':
            self._send_json(200, ITEMS)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/login':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
            except Exception:
                self._send_json(400, {"error": "Invalid JSON"})
                return

            email = data.get('email')
            password = data.get('password')
            if email in USERS and USERS[email]["password"] == password:
                self._send_json(200, {"token": "fake-jwt-token-12345", "user": USERS[email]["name"]})
            else:
                self._send_json(401, {"error": "Invalid credentials"})
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleQAHandler)
    print(f"QA Demo Application running at http://127.0.0.1:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")

if __name__ == '__main__':
    run()
