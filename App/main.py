from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

name = "Iasmina"

app = Flask(__name__)
app.secret_key = 'secret_key'  # Necesar pentru flash messages

# Configurarea conexiunii la baza de date SQL Server
driver = "ODBC Driver 11 for SQL Server"
server = "DESKTOP-O8H9J1P\\SQLEXPRESS"
db = "Hack2"

# Conectare la baza de date
cnxn_str = (
    f"Driver={{{driver}}};"
    f"Server={server};"
    f"Database={db};"
    "Trusted_Connection=yes;"
)
cnxn = pyodbc.connect(cnxn_str)
cursor = cnxn.cursor()

# Rutele Flask
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Preluarea datelor din formular
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        bloc = request.form.get('bloc')
        strada = request.form.get('strada')
        varsta = request.form.get('varsta')
        telefon = request.form.get('telefon')
        apartament = request.form.get('apartament')
        detalii = request.form.get('detalii')

        cursor.execute("SELECT nume FROM dbo.neighbors WHERE nume = ?", (name,))
        exista = cursor.fetchall()

        # Compară parolele
        if password != confirm_password:
            flash('Parolele nu se potrivesc!', 'error')
            return redirect(url_for('create_account'))
        
        if exista:
            flash('Vecinul este deja inregistrat!', 'error')
            return redirect(url_for('create_account'))

        try:
            # Inserarea datelor în baza de date
            cursor.execute(
                """INSERT INTO dbo.neighbors (nume, email, bloc, varsta, strada, telefon, apartament, abilitati)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, email, bloc, varsta, strada, telefon, apartament, detalii)
            )

            cnxn.commit()  # Confirmă salvarea în baza de date

            cursor.execute("SELECT id FROM dbo.neighbors WHERE nume = ?", (name,))
            vecin_id = cursor.fetchone()

            if vecin_id:
                # Adaugă parola în tabela `dbo.passwords`
                cursor.execute("INSERT INTO dbo.passwords (vecin_id, parola_hash) VALUES (?, ?)", (vecin_id[0], password))
                cnxn.commit()  # Confirmă salvarea parolei în baza de date


            flash('Contul a fost creat cu succes!', 'success')
            return redirect(url_for('create_account'))

        except Exception as e:
            flash(f'Eroare la crearea contului: {str(e)}', 'error')
            return redirect(url_for('create_account'))

    return render_template("createAccount.html")



@app.route("/")
def home():
    return render_template("startPage.html", name = name)  # Rendează pagina HTML

@app.route("/login")
def login():

    return render_template('startPage.html')

if __name__ == "__main__":
    app.run(debug=True)  # Pornește serverul în modul debug
