from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

ADMIN_PASSWORD = "admin123"


def init_db():
    conn = sqlite3.connect("apartment.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS apartments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_number TEXT NOT NULL,
        monthly_rent REAL NOT NULL,
        status TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tenants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        contact TEXT NOT NULL,
        unit TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_name TEXT NOT NULL,
        unit_number TEXT NOT NULL,
        amount_paid REAL NOT NULL,
        payment_date TEXT NOT NULL,
        month_paid TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html", active="home")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form["password"]

        if password == ADMIN_PASSWORD:
            return redirect("/add_apartment")
        else:
            return render_template("admin_error.html", active="admin")

    return render_template("admin.html", active="admin")


@app.route("/add_apartment", methods=["GET", "POST"])
def add_apartment():
    if request.method == "POST":
        unit_number = request.form["unit_number"]
        monthly_rent = request.form["monthly_rent"]
        status = request.form["status"]

        conn = sqlite3.connect("apartment.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO apartments (unit_number, monthly_rent, status)
        VALUES (?, ?, ?)
        """, (unit_number, monthly_rent, status))

        conn.commit()
        conn.close()

        return redirect("/apartments")

    return render_template("add_apartment.html", active="admin")


@app.route("/apartments")
def apartments():
    conn = sqlite3.connect("apartment.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM apartments")
    apartments = cursor.fetchall()

    conn.close()

    return render_template("apartments.html", apartments=apartments, active="apartments")


@app.route("/add_tenant", methods=["GET", "POST"])
def add_tenant():
    if request.method == "POST":
        fullname = request.form["fullname"]
        contact = request.form["contact"]
        unit = request.form["unit"]

        conn = sqlite3.connect("apartment.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tenants (fullname, contact, unit)
        VALUES (?, ?, ?)
        """, (fullname, contact, unit))

        conn.commit()
        conn.close()

        return redirect("/tenants")

    return render_template("add_tenant.html", active="add_tenant")


@app.route("/tenants")
def tenants():
    conn = sqlite3.connect("apartment.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tenants")
    tenants = cursor.fetchall()

    conn.close()

    return render_template("tenants.html", tenants=tenants, active="tenants")


@app.route("/add_payment", methods=["GET", "POST"])
def add_payment():
    if request.method == "POST":
        tenant_name = request.form["tenant_name"]
        unit_number = request.form["unit_number"]
        amount_paid = request.form["amount_paid"]
        payment_date = request.form["payment_date"]
        month_paid = request.form["month_paid"]

        conn = sqlite3.connect("apartment.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO payments (tenant_name, unit_number, amount_paid, payment_date, month_paid)
        VALUES (?, ?, ?, ?, ?)
        """, (tenant_name, unit_number, amount_paid, payment_date, month_paid))

        conn.commit()
        conn.close()

        return redirect("/payments")

    return render_template("add_payment.html", active="add_payment")


@app.route("/payments")
def payments():
    conn = sqlite3.connect("apartment.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM payments")
    payments = cursor.fetchall()

    conn.close()

    return render_template("payments.html", payments=payments, active="payments")


init_db()

if __name__ == "__main__":
    app.run(debug=True)