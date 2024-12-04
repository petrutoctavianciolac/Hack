import pyodbc as odbc

driver = "ODBC Driver 11 for SQL Server"
server="DESKTOP-O8H9J1P" + "\\" + "SQLEXPRESS"
db = "Avioane"
username = "octavian"
password = "123456"

cnxn_str = (
        "Driver=" + driver + ";"
        "Server=" + server + ";"
        "Database=" + db + ";"
        "Trusted_Connection=no;"
        "UID=" + username + ";"
        "PWD=" + password + ";"
                    )
conn = odbc.connect(cnxn_str)

cursor = conn.cursor()
cursor.execute("SELECT * FROM dbo.Avioane")
avioane = cursor.fetchall()

for a in avioane:
    print(a)

conn.close()