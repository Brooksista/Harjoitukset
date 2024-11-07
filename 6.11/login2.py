import jwt
import datetime
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from mysql.connector import connect, Error

# Secret key for encoding JWTs (keep this secure in production)
SECRET_KEY = "your_secret_key_here"

class TokenBasedAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Define routes
        routes = {
            "/login": self.login,
            "/logout": self.logout,
            "/": self.home
        }

        try:
            # Handle route
            response = 200
            handler = routes.get(self.path.split('?')[0], self.not_found)
            content = handler()
        except Exception as e:
            response = 500
            content = "Server Error"
            print("Error:", e)

        # Send response
        self.send_response(response)
        self.send_header('Content-type', 'text/html')
        if hasattr(self, "cookie"):
            self.send_header("Set-Cookie", self.cookie)
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def login(self):
        # Parse query parameters
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)
        username = params.get("username", [""])[0]
        password = params.get("password", [""])[0]

        if username and password:
            user = self.check_credentials(username, password)
            if user:
                # Create JWT and set it as HttpOnly cookie
                token = self.create_jwt(user)
                self.cookie = f"token={token}; HttpOnly; Path=/"
                return "Logged in successfully!"
            else:
                return self.login_form("Invalid credentials")
        else:
            return self.login_form("Username and password required")

    def logout(self):
        # Clear the token by setting an empty cookie with expired time
        self.cookie = "token=; HttpOnly; Path=/; Max-Age=0"
        return "Logged out successfully!"

    def home(self):
        # Check JWT token in cookies
        token = self.get_jwt_from_cookie()
        if token and self.verify_jwt(token):
            return "Welcome, you are logged in!"
        else:
            return "Welcome, please <a href='/login'>login</a> to continue."

    def login_form(self, error_message=None):
        error_html = f'<p style="color:red;">{error_message}</p>' if error_message else ""
        return f'''
            <html>
                <body>
                    <h2>Login</h2>
                    {error_html}
                    <form method="get" action="/login">
                        <label for="username">Username:</label><br>
                        <input type="text" id="username" name="username" required><br>
                        <label for="password">Password:</label><br>
                        <input type="password" id="password" name="password" required><br><br>
                        <input type="submit" value="Login">
                    </form>
                </body>
            </html>
        '''

    def create_jwt(self, user):
        # Define JWT payload with expiration time
        payload = {
            "user_id": user["tunnus"],
            "username": user["nimi"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }
        # Encode JWT
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def verify_jwt(self, token):
        try:
            # Decode and verify JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload  # Return payload if successful
        except jwt.ExpiredSignatureError:
            print("JWT has expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid JWT")
            return None

    def get_jwt_from_cookie(self):
        cookies = self.parse_cookies(self.headers.get("Cookie"))
        return cookies.get("token")

    def parse_cookies(self, cookie_list):
        return dict((c.strip().split("=", 1) for c in cookie_list.split(";"))) if cookie_list else {}

    def check_credentials(self, username, password):
        # Check the database for matching credentials
        try:
            with connect(
                host="localhost",
                user="root",
                password="kukkula",
                database="tilavaraus"
            ) as connection:
                query = "SELECT tunnus, nimi FROM kayttajat WHERE nimi = %s AND salasana = %s"
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (username, password))
                    return cursor.fetchone()
        except Error as e:
            print("Database connection error:", e)
            return None

    def not_found(self):
        return "404 Not Found"

# Server setup
address = ('', 8000)
handler = TokenBasedAuthHandler
server = HTTPServer(address, handler)

print("Server running on port 8000...")
server.serve_forever()
