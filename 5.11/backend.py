from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import json
from urllib.parse import parse_qs, urlparse
from datetime import date, datetime

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'kukkula',
    'database': 'tilavaraus'
}

class MyRequestHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # CORS header
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')  # Allowed methods
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Allowed headers
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) == 1:
            table = path_parts[0]
            if table in ['tilat', 'varaajat', 'varaukset']:
                data = self.view_table(table)
                self._set_headers()
                self.wfile.write(json.dumps(data).encode())
            else:
                self.send_error(404, "Table not found")
        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) == 1:
            table = path_parts[0]
            if table in ['tilat', 'varaajat', 'varaukset']:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                params = parse_qs(post_data.decode())

                fields = {key: value[0] for key, value in params.items()}

                success = self.add_record(table, fields)
                self._set_headers()
                response = {'success': success}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(404, "Table not found")

    def do_DELETE(self):
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) == 2:
            table = path_parts[0]
            record_id = path_parts[1]

            if table in ['tilat', 'varaajat', 'varaukset'] and record_id.isdigit():
                success = self.delete_record(table, record_id)
                self._set_headers()
                response = {'success': success}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(400, "Invalid table or ID")
        else:
            self.send_error(404, "Endpoint not found")

    def view_table(self, table):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            # Convert any date or datetime objects to strings
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, (date, datetime)):
                        row[key] = value.isoformat()

            return {'success': True, 'data': rows}
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return {'success': False, 'error': str(err)}
        finally:
            cursor.close()
            conn.close()

    def add_record(self, table, fields):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            columns = ', '.join(fields.keys())
            values = ', '.join(['%s'] * len(fields))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(sql, tuple(fields.values()))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_record(self, table, record_id):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            sql = f"DELETE FROM {table} WHERE id = %s"
            cursor.execute(sql, (record_id,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

# Run the server
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
