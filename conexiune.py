import pyodbc
from flask import Flask, flash, jsonify, render_template, request
from flask_cors import CORS

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
        """, (1, titlu, descriere, categorie, 'În așteptare'))  # Vecinul are id=1

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
        vecin_id = 1

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
            WHERE [id] = 1
        """)



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
            WHERE status = 'Acceptata'
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


if __name__ == '__main__':
    app.run(debug=True)