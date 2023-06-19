from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'adminp'
app.config['MYSQL_DB'] = 'complaint_portal'


db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']

)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = 'Pending'  # Set initial status as Pending

        # Insert complaint into the database
        cursor.execute("INSERT INTO complaints (title, description, status) VALUES (%s, %s, %s)",
                       (title, description, status))
        db.commit()

        return redirect('/complaints')

    else:
        # Fetch complaints from the database
        cursor.execute("SELECT * FROM complaints")
        complaints = cursor.fetchall()

        return render_template('complaints.html', complaints=complaints)

if __name__ == '__main__':
    app.run(debug=True)