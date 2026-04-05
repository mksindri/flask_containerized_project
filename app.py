from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
        result = cur.fetchone()

        if result:
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clients")
    data = cur.fetchall()

    return render_template('dashboard.html', clients=data)


# ---------------- ADD CLIENT ----------------
@app.route('/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        details = (
            request.form['name'],
            request.form['mobile'],
            request.form['company'],
            request.form['designation'],
            request.form['address']
        )

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO clients(name, mobile, company, designation, address)
            VALUES(%s,%s,%s,%s,%s)
        """, details)

        mysql.connection.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_client.html')


# ---------------- EDIT CLIENT ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        updated = (
            request.form['name'],
            request.form['mobile'],
            request.form['company'],
            request.form['designation'],
            request.form['address'],
            id
        )

        cur.execute("""
            UPDATE clients
            SET name=%s, mobile=%s, company=%s, designation=%s, address=%s
            WHERE id=%s
        """, updated)

        mysql.connection.commit()
        return redirect(url_for('dashboard'))

    cur.execute("SELECT * FROM clients WHERE id=%s", (id,))
    client = cur.fetchone()

    return render_template('edit_client.html', client=client)


# ---------------- DELETE CLIENT ----------------
@app.route('/delete/<int:id>')
def delete_client(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM clients WHERE id=%s", (id,))
    mysql.connection.commit()

    return redirect(url_for('dashboard'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)