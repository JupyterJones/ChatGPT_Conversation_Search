import sqlite3
import os
import hashlib

# Connect to SQLite database (creates a new database if it doesn't exist)
db_path = 'CHATGPT_text.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table to store file information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        content BLOB NOT NULL,
        text_content TEXT NOT NULL,
        hash_value TEXT NOT NULL,
        format TEXT NOT NULL
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

# Function to calculate SHA-256 hash of a file
def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):  # Read in 8KB chunks
            sha256.update(chunk)
    return sha256.hexdigest()

# Function to insert a file into the database
def insert_file(filename, content, text_content, hash_value, file_format):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO files (filename, content, text_content, hash_value, format) VALUES (?, ?, ?, ?, ?)',
                   (filename, content, text_content, hash_value, file_format))
    conn.commit()
    conn.close()

# Function to insert HTML files recursively
def insert_text_files(directory):
    for filename in os.listdir(directory):  # Corrected variable name
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)  # Construct full file path
            with open(file_path, 'rb') as file:
                print(file_path)
                file_content = file.read()
                
            text_content = file_content.decode('utf-8', errors='ignore')  # Convert bytes to string
            hash_value = calculate_hash(file_path)
            insert_file(filename, file_content, text_content, hash_value, 'txt')  # Corrected insertion
            print(f"Inserted: {filename}")

# Example: Insert HTML files recursively from the specified directory
input_folder = 'CHATGPT/TEXT'
insert_text_files(input_folder)

print('Insertion process completed.')
