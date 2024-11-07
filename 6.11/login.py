from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.parse import unquote
from mysql.connector import connect, Error
from random import randint

# Session storage
sessions = {}

class SessionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Route mapping
        routes = {
            "/login": self.login,
            "/logout": self.logout,
            "/": self.home
        }
        
        # Reset cookie
        self.cookie = None
        try:
            # Check cookies for session
            response = 200
            cookies = self.parse_cookies(self.headers.get("Cookie"))
            if "sid" in cookies:
                self.user = sessions.get(cookies["sid"], False)
            else:
                self.user = False
            
            # Find the correct route, default to 404 if route not found
            handler = routes.get(self.path.split('?')[0], self.not_found)
            content = handler()
        except Exception as e:
            response = 404
            content = "Not Found"
        
        # Send response
        self.send_response(response)
        self.send_header('Content-type', 'text/html')
        if self.cookie:
            self.send_header('Set-Cookie', self.cookie)
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def home(self):
        return f"Welcome, {self.user['nimi']}!" if self.user else "Welcome Stranger!"

    def login(self):
        # Parse query parameters for login
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)
        
        # Decode the URL-encoded parameters
        username = unquote(params.get("username", [""])[0])
        password = unquote(params.get("password", [""])[0])

        # Check credentials
        if username and password:
            user = self.check_credentials(username, password)
            if user:
                sid = self.generate_sid()
                self.cookie = f"sid={sid}"
                sessions[sid] = user  # Store user session
                return f"Logged In as {user['nimi']}"
            else:
                return "Invalid credentials"
        else:
            return "Username and password required"


    def logout(self):
        if not self.user:
            return "Can't Log Out: No User Logged In"
        self.cookie = "sid="
        del sessions[self.user]
        return "Logged Out"

    def generate_sid(self):
        return "".join(str(randint(1, 9)) for _ in range(100))

    def parse_cookies(self, cookie_list):
        return dict((c.strip().split("=", 1) for c in cookie_list.split(";"))) if cookie_list else {}

    def check_credentials(self, username, password):
        try:
            with connect(
                host="localhost",
                user="root",
                password="kukkula",
                database="tilavaraus"
            ) as connection:
                # Using `nimi` as the username and `salasana` for the password
                query = "SELECT tunnus, nimi FROM kayttajat WHERE nimi = %s AND salasana = %s"
                
                # Debugging output to verify parameters
                print("Checking credentials for:", username, password)

                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (username, password))
                    user = cursor.fetchone()
                    print("Queried user:", user)  # Debugging line
                    return user  # Returns the user record if found
        except Error as e:
            print("Database connection error:", e)
            return None



    def not_found(self):
        return "404 Not Found"

# Server setup
address = ('', 8000)
handler = SessionHandler
server = HTTPServer(address, handler)

print("Server running on port 8000...")
server.serve_forever()
