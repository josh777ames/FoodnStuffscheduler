from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulating a database with a dictionary, including a role for each user
# Note: Changed 'sha256' to 'pbkdf2:sha256' in generate_password_hash method
users = {
    'admin1@trincoll.edu': {'password': generate_password_hash('415', method='pbkdf2:sha256'), 'role': 'admin'},
    'volunteer1@trincoll.edu': {'password': generate_password_hash('415', method='pbkdf2:sha256'), 'role': 'volunteer'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['login-email']
    password = request.form['login-password']
    user = users.get(email)
    
    if user and check_password_hash(user['password'], password):
        # Login successful
        flash('Login successful!', 'success')
        if user['role'] == 'admin':
            return redirect(url_for('admin_ui'))
        elif user['role'] == 'volunteer':
            return redirect(url_for('volunteer_ui'))
    else:
        # Login failed
        flash('Invalid email or password.', 'danger')
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['signup-email']
    password = request.form['signup-password']
    confirm_password = request.form['signup-confirm-password']

    if email in users:
        flash('Email already exists.', 'danger')
        return redirect(url_for('index'))

    if password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('index'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    users[email] = {'password': hashed_password, 'role': 'volunteer'}  # Default role is volunteer
    flash('Account created successfully, please login.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_ui():
    # Ensure this page has some form of access control in a real application
    return render_template('admin_ui.html')

@app.route('/volunteer')
def volunteer_ui():
    # Ensure this page has some form of access control in a real application
    return render_template('volunteer_ui.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
