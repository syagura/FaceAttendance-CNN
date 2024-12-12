from flask import Flask, render_template

app = Flask(__name__)

app.secret_key = 'secretkeyhere'

@app.route('/')
def login():
    return render_template('auth/login.html', title='Login')

if __name__ == '__main__':
    app.run(debug=True)