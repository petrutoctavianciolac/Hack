import pyodbc
from flask import Flask, flash, jsonify, render_template, request

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
            SELECT [id], [vecin_id], [titlu], [descriere], [status], [data_cerere]
            FROM [general].[dbo].[requests]
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

@app.route('/templates/myrequests')
def cererile_mele():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Execută SQL pentru a prelua cererile
        cursor.execute("""
            SELECT [id], [titlu], [descriere],[status]
            FROM [general].[dbo].[requests]
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

        # Conectare la baza de date
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Interogare SQL pentru a insera cererea în tabelul 'requests'
        cursor.execute("""
            INSERT INTO [dbo].[requests] ([vecin_id], [titlu], [descriere], [status])
            VALUES (?, ?, ?, ?)
        """, (1, titlu, descriere, 'În așteptare'))  # Vecinul are id=1

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
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Interogare SQL pentru a selecta datele din tabelul 'requests'
        cursor.execute("""
            SELECT TOP 5 [id], [vecin_id], [titlu], [descriere], [status], [data_cerere]
            FROM [general].[dbo].[requests]
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


@app.route("/templates/startPage", methods=["GET"])
def toStart():
    if request.method == "GET":
        return render_template('startPage.html')  # Afișează formularul
    
@app.route("/templates/avizier", methods=["GET"])
def toAvizier():
    if request.method == "GET":
        return render_template('avizier.html')  # Afișează formularul


"""
@app.route("/templates/pagina_cerere")
def index():
    return render_template('pagina_cerere.html')
@app.route("/templates/pagina_cerere", methods=["GET"])
def show_request_form():
    return render_template('pagina_cerere.html')  # Afișează formularul

"""

if __name__ == '__main__':
    app.run(debug=True)