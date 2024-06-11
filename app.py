import os
from flask import Flask, render_template, request, Blueprint
import datetime
import glob
import shutil
import json
import logging
import os
import sqlite3
from sys import argv
app = Flask(__name__)

def mst(terms):
    database_name = 'CHATGPT_text.db'
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cnt = 0

    # Define the search terms
    search_terms = terms.split(",")  # Split the input string by comma to get individual search terms

    # Construct the WHERE clause for the SQL query to filter rows based on all search terms
    where_conditions = [f"text_content LIKE '%{term}%'" for term in search_terms]
    where_clause = " AND ".join(where_conditions)

    # Execute the SELECT query with the constructed WHERE clause
    query = f"SELECT ROWID, * FROM files WHERE {where_clause}"
    rows = cursor.execute(query)
    DATA = []

    # Iterate over the resulting rows and print the ROWID and user_ChatGPT_PAIR column
    for row in rows:
        cnt += 1
        DATA.append((row[0], row[1], row[4], cnt))

    # Close the connection
    conn.close()
    return DATA

@app.route('/index_', methods=['GET', 'POST'])
def index_():
    if request.method == 'POST':
        terms = request.form.get('terms')
        uploaded_file = request.files.get('file')

        logging.debug(f"Received terms: {terms}")
        logging.debug(f"Received file: {uploaded_file.filename if uploaded_file else 'No file'}")

        if uploaded_file:
            # Save the uploaded file
            file_path = os.path.join('uploads', uploaded_file.filename)
            uploaded_file.save(file_path)
            logging.debug(f"File saved to: {file_path}")

        data = mst(terms)
        logging.debug(f"Processed data: {data}")

        return render_template('index_working.html', data=data)

    return render_template('index_working.html', data=None)



#sqlite3_editor_bp  = Blueprint('sqlite3_editor', __name__, url_prefix='/sqlite3_editor', template_folder='templates')
#, template_folder='templates/exp')
# Configure logging
def logit(logdata):
    timestr = filename = datetime.datetime.now().strftime('%A_%b-%d-%Y')
    with open("testlog2.txt", "a") as log_file:
        log_file.write(f"{timestr}: {logdata} <br/>")
    print("testlog2.txt entry:", logdata)

logit("TEST: 12345 in testlog2.txt\n")

@app.route('/readlog')
def readlog():
    logdata = []
    with open("testlog2.txt", "r") as log_file:
        logdata = log_file.readlines()
    return render_template('read_log.html', log_content=logdata)

# Read functions from app.py file into memory


def read_functions():

    logit("Reading file 'html_py.txt'...")
    #with open('html_py.txt', 'r') as file:
    with open('con_html1.txt', 'r') as file:
        code = file.read()
        #code = code.decode('utf-8')
        functions = code.split('\n\n') # Splitting text into verses based on empty lines
        logit("File successfully read and verses extracted.")
    
    return functions

# Test the function
#verses = read_functions()


functions = read_functions()

@app.route('/')
def index():
    return render_template('index_code.html')


@app.route('/save', methods=['POST'])
def save():
    code = request.form['code']
    logit(f"Received code: {code}")
    suggestions = generate_suggestions(code)
    logit(f"Generated suggestions: {suggestions}")
    return {'suggestions': suggestions}

def generate_suggestions(code):
    logit("Generating suggestions...")
    # Retrieve the last line from the code
    lines = code.split('\n')
    last_line = lines[-1]

    # Split the last line into words and get the last four words
    words = last_line.split()
    last_four_words = ' '.join(words[-2:])
    logit(f"Last four words: {last_four_words}")

    # Search for a matching snippet based on the last four words
    matching_snippets = []
    for i, snippet in enumerate(functions, start=1):
        if last_four_words in snippet:
            # Format the snippet with line numbers and preserve whitespace
            formatted_snippet = f"<pre>{i}: {snippet.strip()}</pre>"
            matching_snippets.append(formatted_snippet)

    logit(f"Matching snippets: {matching_snippets}")

    return matching_snippets
@app.route('/save_code', methods=['POST'])
def save_code():
    # Extract the code from the request body
    code = request.data.decode('utf-8')

    if code:
        # Append the code to the new_app.py file
        with open('new_app.py', 'a') as file:
            file.write(code + '\n')
        
        return 'Code saved successfully', 200
    else:
        return 'No code provided in the request', 400


# Main function to create table and run the app
if __name__ == "__main__":
    #create_table(app.config['DATABASE_'])
    print("port=5500")
    app.run(debug=True,host='0.0.0.0',port=5500)        
 