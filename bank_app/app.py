
import os
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secretkey"


# User logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login", message="You have been logged out successfully."))

# Admin logout route
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login", message="You have been logged out successfully."))

# File upload configuration
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fake database (replace later)
users = {
    "user1": {"password": "1234", "locked": False}
}

admin = {
    "christopher98": "986031"
}

# Unlock account route
@app.route("/admin/unlock/<username>", methods=["POST"])
def unlock_account(username):
    if "admin" in session and username in users:
        users[username]["locked"] = False
        users[username]["message"] = "Account unlocked."
    return redirect("/admin/accounts")

# Send message to account route
@app.route("/admin/message/<username>", methods=["POST"])
def send_message(username):
    if "admin" in session and username in users:
        msg = request.form.get("message", "")
        users[username]["message"] = msg
    return redirect("/admin/accounts")
import os
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secretkey"

# File upload configuration
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fake database (replace later)
users = {
    "user1": {"password": "1234", "locked": False}
}

admin = {
    "christopher98": "986031"
}

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/admin/clients")
def admin_clients():
    return render_template("admin_clients.html", users=users)

@app.route("/admin/accounts", methods=["GET", "POST"])
def admin_accounts():
    message = ""
    error = ""
    if request.method == "POST":
        try:
            required_fields = ["username", "email", "password", "fullname", "bank", "account_number", "account_type"]
            for field in required_fields:
                if not request.form.get(field):
                    raise ValueError(f"Missing required field: {field}")

            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            fullname = request.form["fullname"]
            bank = request.form["bank"]
            account_number = request.form["account_number"]
            account_type = request.form["account_type"]

            # Email must be unique
            for u, data in users.items():
                if data.get("email", "").lower() == email.lower():
                    raise ValueError("Email already exists. Please use a different email.")
            if username in users:
                raise ValueError("Username already exists. Please use a different username.")

            # Handle photo upload
            photo = request.files.get("photo")
            filename = ""
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            # Handle bank logo upload
            bank_logo_file = request.files.get("bank_logo")
            bank_logo_filename = ""
            if bank_logo_file and bank_logo_file.filename and allowed_file(bank_logo_file.filename):
                bank_logo_filename = "logo_" + secure_filename(bank_logo_file.filename)
                bank_logo_file.save(os.path.join(app.config["UPLOAD_FOLDER"], bank_logo_filename))

            users[username] = {
                "username": username,
                "email": email,
                "password": password,
                "locked": False,
                "message": "Account created successfully!",
                "fullname": fullname,
                "bank": bank,
                "account_number": account_number,
                "account_type": account_type,
                "photo": filename,
                "bank_logo": bank_logo_filename,
                "balance": 0.0,
                "created_by": session.get("admin", "admin"),
                "transfer_history": []
            }

            # Optional fields
            initial_transfer = request.form.get("initial_transfer")
            if initial_transfer:
                try:
                    amt = float(initial_transfer)
                    users[username]["transfer_history"].append({
                        "type": "initial",
                        "amount": amt,
                        "description": "Initial deposit"
                    })
                    users[username]["balance"] += amt
                except Exception:
                    pass

            start_year = request.form.get("start_year")
            from datetime import datetime
            if start_year:
                try:
                    start_year = int(start_year)
                    current_year = datetime.now().year
                    for year in range(start_year, current_year + 1):
                        users[username]["transfer_history"].append({
                            "type": "yearly",
                            "amount": 0.0,
                            "description": f"Yearly history for {year}",
                            "year": year
                        })
                except Exception:
                    pass
            message = f"Account for {username} created successfully!"
        except Exception as e:
            error = str(e) if str(e).startswith("Missing required field") or str(e).endswith("exists. Please use a different email.") or str(e).endswith("exists. Please use a different username.") else "Invalid input. Please check all fields."
    return render_template("admin_accounts.html", users=users, message=message, error=error)

@app.route("/admin/security")
def admin_security():
    return render_template("admin_security.html")

# ================= USER SIDE =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_id = request.form["login_id"]
        password = request.form["password"]

        # Try to find user by username or email
        user = None
        username = None
        for u, data in users.items():
            if data.get("username") == login_id or data.get("email") == login_id:
                user = data
                username = u
                break
        if not user or user["password"] != password:
            return render_template("login.html", error="Invalid username/email or password.")

        # Allow login even if locked
        session["user"] = username
        return redirect("/dashboard")

    # Show logout message if present
    message = request.args.get("message")
    return render_template("login.html", message=message) if message else render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")  # ADS HERE


# ================= ADMIN SIDE =================
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in admin and admin[username] == password:
            session["admin"] = username
            return redirect("/admin/panel")

        return render_template("admin_login.html", error="Incorrect username or password.")

    # Show logout message if present
    message = request.args.get("message")
    return render_template("admin_login.html", message=message) if message else render_template("admin_login.html")


@app.route("/admin/panel", methods=["GET", "POST"])
def admin_panel():
    if "admin" not in session:
        return redirect("/admin")

    message = ""
    if request.method == "POST":
        username = request.form["username"]
        photo = request.files.get("photo")
        filename = ""
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        users[username] = {
            "password": request.form["password"],
            "locked": False,
            "message": "Account created successfully!",
            "fullname": request.form["fullname"],
            "bank": request.form["bank"],
            "account_number": request.form["account_number"],
            "account_type": request.form["account_type"],
            "photo": filename,
            "balance": 0.0,
            "created_by": session["admin"],
            "transfer_history": []
        }
        # Optionally add initial transfer history if provided
        initial_transfer = request.form.get("initial_transfer")
        if initial_transfer:
            users[username]["transfer_history"].append({
                "type": "initial",
                "amount": float(initial_transfer),
                "description": "Initial deposit"
            })
            users[username]["balance"] += float(initial_transfer)
        message = f"Account for {username} created successfully!"
        return redirect("/admin/panel")

    # Show only users created by this admin
    admin_users = {u: d for u, d in users.items() if d.get("created_by") == session["admin"]}
    return render_template("admin_panel.html", users=admin_users, message=message)


@app.route("/admin/lock/<username>")
def lock_user(username):
    if "admin" in session and username in users:
        users[username]["locked"] = True
    return redirect("/admin/panel")



@app.route("/admin/lock/<username>", methods=["POST"])
def lock_account(username):
    if "admin" in session and username in users:
        if users[username]["created_by"] == session["admin"]:
            message = request.form.get("message", "")
            users[username]["locked"] = True
            users[username]["message"] = message
    return redirect("/admin/panel")


@app.route("/transfer", methods=["POST"])
def transfer():
    user = users[session["user"]]

    if user["locked"]:
        return render_template(
            "locked.html",
            message=user.get("message", "Your account is restricted.")
        )

    # Get transfer details from form
    recipient = request.form.get("recipient")
    amount = request.form.get("amount", type=float)

    # Validate recipient and amount
    if not recipient or recipient not in users:
        return "Recipient not found"
    if amount is None or amount <= 0:
        return "Invalid transfer amount"
    if user["balance"] < amount:
        return "Insufficient funds"
    if users[recipient]["locked"]:
        return f"Cannot transfer to {recipient}: Account is locked."

    # Perform transfer
    user["balance"] -= amount
    users[recipient]["balance"] += amount
    # Record transfer history for sender
    if "transfer_history" not in user:
        user["transfer_history"] = []
    user["transfer_history"].append({
        "type": "sent",
        "amount": amount,
        "to": recipient,
        "description": f"Sent to {recipient}"
    })
    # Record transfer history for recipient
    if "transfer_history" not in users[recipient]:
        users[recipient]["transfer_history"] = []
    users[recipient]["transfer_history"].append({
        "type": "received",
        "amount": amount,
        "from": session["user"],
        "description": f"Received from {session['user']}"
    })
    return render_template("transfer.html", message=f"Successfully transferred ${amount:.2f} to {recipient}.")

