from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
import pyodbc

loggedId = None
name = "Iasmina"

app = Flask(__name__)

app.secret_key = 'secret_key'

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



@app.route("/home")
def home():
    if loggedId is None:
        flash('Te rog să te loghezi!', 'error')
        return redirect(url_for('login'))

    try:
        user_query = "SELECT nume FROM dbo.neighbors WHERE id = ?"
        cursor.execute(user_query, (loggedId,))
        user = cursor.fetchone()

        if user:
            user_name = user[0]
            print(f"Logged user: {user_name}")
            return render_template("startPage.html", name=user_name)
        else:
            flash('User not found în baza de date!', 'error')
            return redirect(url_for('login'))

    except Exception as e:
        print(f"Database error: {str(e)}")
        return redirect(url_for('login'))



@app.route('/templates/myrequests')
def cererile_mele():
    try:
        conn = pyodbc.connect(cnxn_str)
        cursor = conn.cursor()

        # Execută SQL pentru a prelua cererile
        cursor.execute("""
            SELECT id, titlu, descriere, status
            FROM dbo.requests
        """)

        # Preia rezultatele
        rows = cursor.fetchall()

        if not rows:
            return "Nu există cereri disponibile."

        # Redirecționează către template cu datele
        return render_template('myrequests.html', rows=rows)

    except pyodbc.Error as e:
        return f"Error: {e}"

    finally:
        if conn:
            conn.close()

@app.route("/templates/pagina_cerere", methods=["GET", "POST"])
def submit_request():
    if request.method == "GET":
        return render_template('pagina_cerere.html')  # Afișează formularul
    
    try:
        # Obține datele din formularul POST (nu JSON)
        titlu = request.form['titlu']
        descriere = request.form['descriere']

        print(titlu)
        print(descriere)
        # Conectare la baza de date
        conn = pyodbc.connect(cnxn_str)
        cursor = conn.cursor()

        # Interogare SQL pentru a insera cererea în tabelul 'requests'
        cursor.execute("""
            INSERT INTO dbo.requests (vecin_id, titlu, descriere, status)
            VALUES (?, ?, ?, ?)
        """, (18, titlu, descriere, 'În așteptare'))  # Vecinul are id=1

        # Commit modificările în baza de date
        conn.commit()

        # Răspuns de succes
        #return jsonify({"success": True})
        
        return render_template('pagina_cerere.html')

    except pyodbc.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)})

    finally:
        if conn:
            conn.close()

@app.route("/templates/avizier", methods=["GET"])
def avizier():
    try:
        # Conectare la baza de date
        conn = pyodbc.connect(cnxn_str)
        cursor = conn.cursor()

        # Interogare SQL pentru a selecta datele din tabelul 'requests'
        cursor.execute("""
            SELECT TOP 5 id, vecin_id, titlu, descriere, status, data_cerere
            FROM dbo.requests
        """)

        # Obține toate cererile din baza de date
        requests = cursor.fetchall()

        # Închide conexiunea la baza de date
        conn.close()

        # Transmite cererile către template-ul HTML
        return render_template('avizier.html', requests=requests)

    except pyodbc.Error as e:
        print(f"Error: {e}")
        return render_template('error.html', error=str(e))


@app.route("/templates/score", methods=["GET"])
def scoreboard():
    try:
        conn = pyodbc.connect(cnxn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nume, puncte, avatar FROM dbo.neighbors ORDER BY puncte DESC")
        scores = cursor.fetchall()
        formatted_scores = []
        for score in scores:
            formatted_scores.append({
                'nume': score[1],
                'puncte': score[2],
                'avatar': score[3]
            })
        conn.close()
        return render_template('score.html', scores=formatted_scores)
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return render_template('error.html', error=str(e))

@app.route("/templates/avizier", methods=["GET"])
def toAvizier():
    if request.method == "GET":
        return render_template('avizier.html')  # Afișează formularul
    
@app.route("/update_score", methods=["POST"])
def update_score():
    try:
        # Obține datele trimise de la client
        data = request.get_json()
        vecin_id = data.get('vecin_id')  # Vecinul care acceptă
        puncte = data.get('puncte')  # Punctele de adăugat (100 în acest caz)

        # Conectare la baza de date
        conn = pyodbc.connect(cnxn_str)
        cursor = conn.cursor()

        # Actualizează punctele vecinului în tabela 'neighbors'
        cursor.execute("""
            UPDATE dbo.neighbors
            SET puncte = puncte + ?
            WHERE id = ?
        """, (puncte, vecin_id))

        # Comite modificările în baza de date
        conn.commit()

        # Închide conexiunea la baza de date
        conn.close()

        # Răspunde cu succes
        return jsonify({"success": True})

    except pyodbc.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)})


@app.route('/login', methods=['GET', 'POST'])
def login():
    global loggedId
    if request.method == 'POST':
        password = request.form.get('password')
        name = request.form.get('username')
        print(name)

        try:
            cursor = cnxn.cursor()

            # Caută utilizatorul în baza de date din tabelul 'neighbors'
            query = "SELECT id, nume FROM dbo.neighbors WHERE nume = ?"
            cursor.execute(query, (name,))
            
            user = cursor.fetchone()

            if user:
                user_id = user[0]  # Obține ID-ul (cheia primară)
                print(f"User ID: {user_id}")

                # Verifică parola din tabelul 'passwords'
                query = "SELECT * FROM dbo.passwords WHERE vecin_id = ? AND parola_hash = ?"
                cursor.execute(query, (user_id, password))

                valid = cursor.fetchone()

                if valid:
                    loggedId = user_id
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid password.', 'danger')

            else:
                flash('Username not found.', 'danger')

        except Exception as e:
            flash(f'Database Error: {str(e)}', 'danger')

    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)  # Pornește serverul în modul debug
