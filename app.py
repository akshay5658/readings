from flask import Flask, request, jsonify,send_file, render_template
import sqlite3
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'sampletext'



conn = sqlite3.connect('Readings.db', check_same_thread=False)

# Create table
# cursor= conn.cursor()
@app.route('/Update', methods=['POST'])
def update():
    cursor= conn.cursor()
    sqlite_insert_with_param = """INSERT INTO Reading
                          (Name, Fasting, Time, Ir, Red) 
                          VALUES (?, ?, ?, ?, ?);"""

    request_data = request.get_json()
    data_tuple = (request_data["Name"],request_data["Fasting"],request_data["Time"],request_data["Ir"],request_data["Red"])
    # print(data_tuple)
    try:
        cursor.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        # conn.close()
        return '''Recent data Updated sucessfully'''
    except:
        return '''Recent data Not-updated Recheck !!!!!'''


@app.route('/getresult', methods=['POST'])
def getresult():
    cursor= conn.cursor()
    request_data = request.get_json()
    query = request_data["query"]
    cursor.execute(query)
    data = cursor.fetchall()
    # print(data)
    return jsonify({"data":data})

@app.route('/download')
def download_file():
    path = "Readings.db"
    return send_file(path, as_attachment=True)


@app.route('/download_database')
def upload_form():
    return render_template('download.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/createtable', methods=['POST'])
def createtable():
    cursor= conn.cursor()
    request_data = request.get_json()
    query = request_data["query"]
    cursor.execute(query)
    conn.commit()
    return '''table created'''

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)    
    #app.run(debug=True)
