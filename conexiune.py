import pyodbc
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
loggedId = None

# Define the connection string
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-PCH5PUC;"  # Replace with your actual server name if different
    "DATABASE=general;"  # Ensure this is the correct database name
    "Trusted_Connection=yes;"  # This uses Windows Authentication
)

# check in console part
def fetch_data_from_db(conn_str, query):
    try:
        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        return rows

    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if conn:
            conn.close()
def print_requests_table(conn_str): #print cererile mele
    try:
        # Conectează-te la baza de date
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Execută interogarea SQL pentru a prelua datele din tabelul 'requests'
        cursor.execute("""
            SELECT *
            FROM [general].[dbo].[scoreboard]
        """)

        # Preia toate rândurile
        rows = cursor.fetchall()

        if not rows:
            print("Nu sunt cereri în tabelul 'requests'.")
        else:
            # Afișează datele
            print("Requests Table Data:")
            for row in rows:
                print(f"id: {row.id}, "
                      f"vecin_id: {row.vecin_id}, "
                      f"titlu: {row.titlu}, "
                      f"descriere: {row.descriere}, "
                      f"status: {row.status}, "
                      f"data_cerere: {row.data_cerere}")

    except pyodbc.Error as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()



# Apelarea funcției pentru a printa tabelul 'requests' print_requests_table(conn_str)

# Flask app setup
app = Flask(__name__)
CORS(app)
app.secret_key = 'secret_key'


@app.route("/templates/pagina_cerere", methods=["GET", "POST"])
def submit_request():
    if request.method == "GET":
        return render_template('pagina_cerere.html')  # Afișează formularul
    
    try:
        # Obține datele din formularul POST (nu JSON)
        titlu = request.form['titlu']
        descriere = request.form['descriere']
        categorie = request.form['categorie']

        # Conectare la baza de date
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Interogare SQL pentru a insera cererea în tabelul 'requests'
        cursor.execute("""
            INSERT INTO [dbo].[requests] ([vecin_id], [titlu], [descriere], [tag], [status])
            VALUES (?, ?, ?, ?, ?)
        """, (loggedId, titlu, descriere, categorie, 'Pending'))  # Vecinul are id=1

        # Commit modificările în baza de date
        conn.commit()

        # Răspuns de succes
        return render_template('pagina_cerere.html')

    except pyodbc.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)})

    finally:
        if conn:
            conn.close()



@app.route("/templates/score", methods=["GET"])
def scoreboard():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nume, puncte, avatar FROM [general].[dbo].[neighbors] ORDER BY puncte DESC")
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


@app.route("/templates/startPage", methods=["GET"])
def toStart():
    if request.method == "GET":
        return render_template('startPage.html')  # Afișează formularul
    
@app.route("/templates/avizier", methods=["GET"])
def avizier():
    try:
        # ID-ul vecinului curent
        vecin_id = loggedId

        # Conectare la baza de date
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # 1. Obține abilitatea/tag-ul vecinului curent
        cursor.execute("SELECT abilitati FROM [general].[dbo].[neighbors] WHERE id = ?", vecin_id)
        abilitate = cursor.fetchone()[0]  # Presupunem că abilitatea este un singur string (ex: "Reparatii")
        print(f'Abilitate vecin: {abilitate}')  # Afișează abilitatea în consolă pentru debug

        # 2. Obține cererile care au același tag ca abilitatea vecinului
        cursor.execute("""
            SELECT titlu, descriere, tag FROM [general].[dbo].[requests]
            WHERE [tag] = ? AND [status] = 'Pending'
        """, abilitate)
        cereri_tag = cursor.fetchall()
        print(cereri_tag)
        # 3. Obține restul cererilor
        cursor.execute("""
            SELECT titlu, descriere, tag FROM [general].[dbo].[requests]
            WHERE [tag] != ? AND [status] = 'Pending'
        """, abilitate)
        alte_cereri = cursor.fetchall()
        print(alte_cereri)
        # Combină cererile: cererile cu tag-ul potrivit vor apărea primele
        cereri = cereri_tag + alte_cereri

        # Returnează cererile către șablon
        return render_template("avizier.html", requests=cereri)

    except pyodbc.Error as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)})

    except Exception as e:
        # Capturăm orice altă eroare posibilă
        print(f"Unexpected error: {e}")
        return jsonify({"success": False, "error": str(e)})

    finally:
        if conn:
            conn.close()

@app.route('/accept_request', methods=['POST'])
def accept_request():
    try:
        # Debug: Printează întregul formular pentru a vedea ce date sunt primite
        print("Form Data:", request.form)

        # Obținem ID-ul cererii din formular
        ticket_id = request.form.get('ticket_id', None)
        print("tichetul este: ", ticket_id)

        if ticket_id is None:
            return "Ticket ID nu a fost trimis corespunzător.", 400

        # Conectare la baza de date
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Actualizare status cerere DUPA TITLU
        cursor.execute("""
            UPDATE [general].[dbo].[requests]
            SET [status] = 'Acceptata'
            WHERE [titlu] = ?
        """, (ticket_id,))

        cursor.execute("""
            UPDATE [general].[dbo].[neighbors]
            SET [puncte] = [puncte] + 100
            WHERE [id] =?
        """, (loggedId))



        # Salvează modificările în baza de date
        conn.commit()

        # Poți adăuga aici logica de redirecționare sau renderizare
        return render_template("startPage.html")

    except pyodbc.Error as e:
        print(f"Error: {e}")
        return "A apărut o eroare la procesarea cererii.", 500

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "A apărut o eroare.", 500

    finally:
        if conn:
            conn.close()


"""
@app.route("/templates/pagina_cerere")
def index():
    return render_template('pagina_cerere.html')
@app.route("/templates/pagina_cerere", methods=["GET"])
def show_request_form():
    return render_template('pagina_cerere.html')  # Afișează formularul
@app.route("/templates/avizier", methods=["GET"])
def toAvizier():
    if request.method == "GET":
        return render_template('avizier.html')  # Afișează formularul

"""
@app.route('/templates/myrequests')
def cererile_mele():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Execută SQL pentru a prelua cererile
        cursor.execute("""
            SELECT [id], [titlu], [descriere],[status]
            FROM [general].[dbo].[requests]
            WHERE status = 'Acceptata' AND vecin_id = ?
        """, (loggedId))

        # Preia rezultatele
        rows = cursor.fetchall()

        if not rows:
            return render_template('myrequests.html')

        # Redirecționează către template cu datele
        return render_template('myrequests.html', rows=rows)

    except pyodbc.Error as e:
        return f"Error: {e}"

    finally:
        if conn:
            conn.close()

@app.route("/templates/pagina_event", methods=["GET"])
def toEvent():
    return render_template('pagina_event.html')  # Afișează formularul
#--------------------------EVENIMENTE----------------------------------------
@app.route("/templates/viewEvents", methods=["GET"])
def toViewEvent():
    try:
        # Conectare la baza de date
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Execută interogarea pentru a obține toate evenimentele din baza de date
        cursor.execute("SELECT nume, descriere, data, locatie FROM [dbo].[evenimente]")

        # Preluăm toate rândurile din baza de date
        events = cursor.fetchall()

        # Trimitem evenimentele către template pentru afișare
        return render_template('viewEvents.html', events=events)

    except pyodbc.Error as e:
        print(f"Eroare SQL: {e}")
        return "A apărut o eroare la preluarea evenimentelor.", 500

    finally:
        # Închidem conexiunea la baza de date
        if conn:
            conn.close()

@app.route("/adauga_eveniment", methods=["POST"])
def adauga_eveniment():
    try:
        # Obține datele din formular
        titlu = request.form['titlu']
        descriere = request.form['descriere']
        data = request.form['data']
        locatie = request.form['locatie']

        # Conectare la baza de date
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Interogare SQL pentru a insera evenimentul în tabelul "evenimente"
        cursor.execute("""
            INSERT INTO [dbo].[evenimente] ([nume], [descriere], [data], [locatie])
            VALUES (?, ?, ?, ?)
        """, (titlu, descriere, data, locatie))

        # Confirmăm modificările
        conn.commit()

        # Redirecționează la pagina evenimentelor după succes
        return redirect('/templates/pagina_event')

    except pyodbc.Error as e:
        print(f"Eroare SQL: {e}")
        return jsonify({"success": False, "error": str(e)})

    finally:
        if conn:
            conn.close()

#---------------------------------LOG IN--------------------------------------------------------
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

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
                """INSERT INTO dbo.neighbors (nume, email, bloc, varsta, strada, telefon, apartament, abilitati,puncte)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, email, bloc, varsta, strada, telefon, apartament, detalii,0)
            )

            conn.commit()  # Confirmă salvarea în baza de date

            cursor.execute("SELECT id FROM dbo.neighbors WHERE nume = ?", (name,))
            vecin_id = cursor.fetchone()

            if vecin_id:
                # Adaugă parola în tabela `dbo.passwords`
                cursor.execute("INSERT INTO dbo.passwords (vecin_id, parola_hash) VALUES (?, ?)", (vecin_id[0], password))
                conn.commit()  # Confirmă salvarea parolei în baza de date


            flash('Contul a fost creat cu succes!', 'success')
            return redirect(url_for('create_account'))

        except Exception as e:
            flash(f'Eroare la crearea contului: {str(e)}', 'error')
            return redirect(url_for('create_account'))

    return render_template("createAccount.html")

@app.route("/home")
def home():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    global loggedId
    if request.method == 'POST':
        password = request.form.get('password')
        name = request.form.get('username')
        print(name)

        try:
            cursor = conn.cursor()

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

#--------------------EVENIMENTE-----------------------------
@app.route('/evenimente', methods=['GET'])
def evenimente():
    try:
        # Conectează-te la baza de date
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Preia toate evenimentele din baza de date
        cursor.execute("SELECT nume, descriere, data, locatie FROM evenimente") 
        events = cursor.fetchall()  # Se preiau evenimentele

        # Închide conexiunea la baza de date
        conn.close()

        # Transmite datele către template
        return render_template('evenimente.html', events=events)
    
    except Exception as e:
        print(f"Error: {e}")
        return "A apărut o eroare la încărcarea evenimentelor.", 500



if __name__ == '__main__':
    app.run(debug=True)