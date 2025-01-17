import os
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

UPLOAD_DIR = "/tmp"  # Path to save the uploaded files
MAX_FILE_SIZE_MB = 80  # Maximum file size limit (in MB)
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
ALLOWED_EXTENSIONS = {'.zip', '.xz', '.bin'}  # Allowed file extensions

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handles GET requests and serves the file upload form."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            files = os.listdir(UPLOAD_DIR)
            file_links = "".join(f'<li><a href="/files/{file}">{file}</a></li>' for file in files)
            self.wfile.write(f"""
                <html>
                <head><title>File Upload</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 20px; }}
                        h2 {{ color: #333; }}
                        form {{ margin-bottom: 20px; }}
                    </style>
                </head>
                <body>
                    <h2>Upload a File (Max 80MB)</h2>
                    <form method="POST" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".zip,.xz,.bin" required>
                        <button type="submit">Upload</button>
                    </form>
                    <h2>Available Files</h2>
                    <ul>{file_links}</ul>
                </body>
                </html>
            """.encode("utf-8"))
        elif self.path.startswith("/files/"):
            """Handles file download."""
            file_path = os.path.join(UPLOAD_DIR, self.path[len("/files/"):])
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
                self.send_header("Content-Type", "application/octet-stream")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        """Handles POST requests for file uploads."""
        if self.path == "/":
            # Get the content length and parse the form
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            # Split the data to get the file field
            boundary = self.headers['Content-Type'].split('boundary=')[-1].encode()
            parts = post_data.split(boundary)

            # Get the file part from the data
            for part in parts:
                if b"Content-Disposition" in part and b"filename=" in part:
                    filename_start = part.find(b"filename=") + len(b'filename="')
                    filename_end = part.find(b'"', filename_start)
                    filename = part[filename_start:filename_end].decode()
                    file_data_start = part.find(b'\r\n\r\n') + 4
                    file_data = part[file_data_start:]

                    # Validate file extension
                    if not self.is_valid_extension(filename):
                        self.send_response(415)
                        self.end_headers()
                        self.wfile.write(b"Invalid file type. Please upload .zip, .xz, or .bin files.")
                        return

                    # File size validation
                    if len(file_data) > MAX_FILE_SIZE_BYTES:
                        self.send_response(413)
                        self.end_headers()
                        self.wfile.write(b"File too large. Please upload a file smaller than 80 MB.")
                        return

                    # Save the file with the original filename
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    self.save_file_with_progress(file_data, file_path)

                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(f"File '{filename}' uploaded successfully.".encode())
                    return

            self.send_error(400, "Invalid form submission.")
        else:
            self.send_error(404, "Page not found")

    def is_valid_extension(self, filename):
        """Check if the file extension is allowed."""
        _, ext = os.path.splitext(filename)
        return ext.lower() in ALLOWED_EXTENSIONS

    def save_file_with_progress(self, file_data, file_path):
        """Save the file and show progress."""
        total_size = len(file_data)
        chunk_size = 1024  # 1KB chunks
        num_chunks = total_size // chunk_size

        with open(file_path, "wb") as f:
            for i in range(num_chunks + 1):
                chunk = file_data[i * chunk_size: (i + 1) * chunk_size]
                f.write(chunk)
                progress = (i + 1) * chunk_size
                self.show_progress(progress, total_size)

            # If there is any leftover data less than a chunk
            leftover_data = file_data[num_chunks * chunk_size:]
            if leftover_data:
                f.write(leftover_data)
                self.show_progress(total_size, total_size)

    def show_progress(self, progress, total_size):
        """Print the progress percentage."""
        progress_percentage = (progress / total_size) * 100
        print(f"Uploading... {progress_percentage:.2f}% completed", end="\r")

def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler, port=8080):
    os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the upload directory exists
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
