from flask import Flask, request, redirect, url_for
import serial
import os

# Configurare port serial pentru Arduino
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)  # Înlocuiește COM4 cu portul Arduino-ului

app = Flask(__name__)

# Fișierul cu datele de utilizator
USER_FILE = "users.txt"

# Pagina de logare
@app.route('/')
def login():
    return '''
        <!DOCTYPE html>
        <html lang="ro">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Autentificare</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f8ff;
                    text-align: center;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                form {
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    display: inline-block;
                }
                input {
                    display: block;
                    width: 100%;
                    margin: 10px 0;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>Autentificare</h1>
            <form action="/authenticate" method="post">
                <input type="text" name="username" placeholder="Nume utilizator" required>
                <input type="password" name="password" placeholder="Parolă" required>
                <button type="submit">Logare</button>
            </form>
        </body>
        </html>
    '''

# Autentificare utilizator
@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')

    # Verificare username și parolă din fișier
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            for line in file:
                user, passw = line.strip().split(':')
                if user == username and passw == password:
                    return redirect(url_for('control_page'))
    return "<p>Autentificare eșuată! Încercați din nou.</p><a href='/'>Înapoi</a>"

# Pagina principală pentru control
@app.route('/control')
def control_page():
    return '''
        <!DOCTYPE html>
        <html lang="ro">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Control NeoPixel și Servo</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f8ff;
                    text-align: center;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                h2 {
                    color: #007BFF;
                }
                form {
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    display: inline-block;
                    margin-top: 20px;
                }
                button {
                    background-color:rgb(167, 40, 148);
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 10px;
                    cursor: pointer;
                    border-radius: 8px;
                    transition: background-color 0.3s;
                }
                button:hover {
                    background-color:rgb(136, 33, 62);
                }
                a {
                    color: #007BFF;
                    text-decoration: none;
                    font-size: 16px;
                }
                a:hover {
                    text-decoration: underline;
                }
                .command-buttons {
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Control NeoPixel și Servo</h1>
            <div class="command-buttons">
                <form action="/send" method="get">
                    <h2>Controlează LED-urile:</h2>
                    <button name="command" value="red">Roșu</button>
                    <button name="command" value="green">Verde</button>
                    <button name="command" value="blue">Albastru</button>
                </form>
            </div>
        </body>
        </html>
    '''

# Ruta pentru trimiterea comenzilor
@app.route('/send', methods=['GET'])
def send_command():
    command = request.args.get('command')
    if command:
        arduino.write((command + '\n').encode())  # Trimite comanda la Arduino
        return f"<p>Comanda '{command}' trimisă!</p><a href='/control'>Înapoi</a>"
    return "<p>Comandă invalidă!</p><a href='/control'>Înapoi</a>"

# Pornire aplicație
if __name__ == '__main__':
    # Exemplu de fișier cu utilizatori (creat dacă nu există)
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w') as file:
            file.write('admin:1234\n')  # Adaugă un utilizator implicit
    app.run(host='0.0.0.0', port=5000)
