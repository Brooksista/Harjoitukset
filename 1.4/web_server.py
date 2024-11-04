from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import json
from urllib.parse import parse_qs
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
        self.end_headers()
    
    def do_GET(self):
        # Example: /view?table=varaukset
        if self.path.startswith('/view'):
            query_components = parse_qs(self.path[6:])  # Extract parameters
            table = query_components.get('table', [None])[0]

            if table:
                data = self.view_table(table)
                self._set_headers()
                self.wfile.write(json.dumps(data).encode())
            else:
                self.send_error(400, "Table parameter missing in the request.")
        
    def do_POST(self):
        # Example: /add?table=varaukset&field1=value1&field2=value2
        if self.path.startswith('/add'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = parse_qs(post_data.decode())

            table = params.get('table', [None])[0]
            fields = {key: value[0] for key, value in params.items() if key != 'table'}

            if table and fields:
                success = self.add_record(table, fields)
                self._set_headers()
                response = {'success': success}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(400, "Table or fields missing in the request.")
    
    def do_DELETE(self):
        # Example: /delete?table=varaukset&id=1
        if self.path.startswith('/delete'):
            query_components = parse_qs(self.path[8:])  # Extract parameters
            table = query_components.get('table', [None])[0]
            record_id = query_components.get('id', [None])[0]

            if table and record_id:
                success = self.delete_record(table, record_id)
                self._set_headers()
                response = {'success': success}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(400, "Table or ID parameter missing in the request.")

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
                        row[key] = value.isoformat()  # Converts to "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS" format

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

class MyRequestHandler(BaseHTTPRequestHandler):
    
    # Other methods...

    def do_GET(self):
        if self.path.startswith('/view'):
            query_components = parse_qs(self.path[6:])
            table = query_components.get('table', [None])[0]

            if table:
                data = self.view_table(table)  # Fetch data from the database
                self._set_headers()

                # Build HTML dynamically
                html_content = "<html><head><title>Database Records</title></head><body>"
                html_content += f"<h1>Records from {table} table</h1><table border='1'><tr>"

                # Header row
                if data['success'] and data['data']:
                    for key in data['data'][0].keys():
                        html_content += f"<th>{key}</th>"
                    html_content += "</tr>"

                    # Data rows
                    for row in data['data']:
                        html_content += "<tr>"
                        for value in row.values():
                            html_content += f"<td>{value}</td>"
                        html_content += "</tr>"
                else:
                    html_content += "<tr><td colspan='100%'>No data available or error fetching data.</td></tr>"

                html_content += "</table></body></html>"
                self.wfile.write(html_content.encode())
            else:
                self.send_error(400, "Table parameter missing in the request.")


# Run the server
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
