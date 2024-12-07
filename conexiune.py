import pyodbc
from flask import Flask, render_template

# Define the connection string
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-PCH5PUC;"  # Replace with your actual server name if different
    "DATABASE=general;"  # Ensure this is the correct database name
    "Trusted_Connection=yes;"  # This uses Windows Authentication
)

# Function to fetch data from the database
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
def print_requests_table(conn_str):
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

# Apelarea funcției pentru a printa tabelul 'requests'
print_requests_table(conn_str)
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

if __name__ == '__main__':
    app.run(debug=True)
