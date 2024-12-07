from flask import Flask, render_template

name = "Iasmina"
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("startPage.html", name = name)  # Rendează pagina HTML

if __name__ == "__main__":
    app.run(debug=True)  # Pornește serverul în modul debug
