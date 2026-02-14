from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "container_secret_key"


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("bookings.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect("/login")

        except:
            conn.close()
            return "<h3>Username already exists!</h3>"

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("bookings.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "<h3>Invalid username or password</h3>"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- BOOKING (PROTECTED) ----------------
@app.route("/booking", methods=["GET", "POST"])
def booking():

    # 🔒 BLOCK if not logged in
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        truck = request.form["truck"]
        ctype = request.form["type"]
        date = request.form["date"]
        time = request.form["time"]

        # Convert to hourly slot
        hour = time.split(":")[0]
        time_slot = f"{hour}:00"

        conn = sqlite3.connect("bookings.db")
        cursor = conn.cursor()

        # Check capacity (max 3 trucks per slot)
        cursor.execute(
            "SELECT COUNT(*) FROM bookings WHERE date=? AND time=?",
            (date, time_slot)
        )
        count = cursor.fetchone()[0]

        if count >= 3:
            conn.close()
            return "<h2>Slot Full ❌</h2><p>Please choose another time.</p>"

        # Insert booking
        cursor.execute(
            "INSERT INTO bookings (name, truck, container_type, date, time) VALUES (?, ?, ?, ?, ?)",
            (name, truck, ctype, date, time_slot)
        )

        conn.commit()
        conn.close()

        return render_template(
    "success.html",
    name=name,
    truck=truck,
    ctype=ctype,
    date=date,
    time=time_slot
)


    return render_template("booking.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin():

    # must be logged in
    if "user" not in session:
        return redirect("/login")

    # only admin allowed
    if session["user"] != "admin":
        return "<h2>Access Denied ❌</h2><p>You are not authorized to view this page.</p>"

    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()

    conn.close()

    return render_template("admin.html", bookings=data)



# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
