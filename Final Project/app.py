import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Helper function to normalize costs to monthly
def normalize_to_monthly(cost, billing_cycle):
    """Convert subscription cost to monthly equivalent"""
    if billing_cycle == "Weekly":
        return cost * 52 / 12
    elif billing_cycle == "Quarterly":
        return cost / 3
    elif billing_cycle == "Annually":
        return cost / 12
    else:  # Monthly or default
        return cost


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show dashboard"""
    user_id = session["user_id"]

    # Get user budgets
    user = db.execute("SELECT entertainment_budget, productivity_budget FROM users WHERE id = ?", user_id)[0]
    ent_budget = user["entertainment_budget"]
    prod_budget = user["productivity_budget"]

    # Get subscriptions
    subs = db.execute("SELECT * FROM subscriptions WHERE user_id = ? ORDER BY renewal_date", user_id)

    # Calculate totals and days remaining
    ent_spent = 0
    prod_spent = 0
    
    today = datetime.now().date()

    for sub in subs:
        # Get billing cycle, default to Monthly for older records
        billing_cycle = sub.get("billing_cycle", "Monthly")
        
        # Calculate normalized monthly cost
        monthly_cost = normalize_to_monthly(sub["cost"], billing_cycle)
        sub["monthly_cost"] = monthly_cost  # Add to subscription for display
        
        # Calculate spending using normalized costs
        if sub["category"] == "Entertainment":
            ent_spent += monthly_cost
        elif sub["category"] == "Productivity":
            prod_spent += monthly_cost
        
        # Calculate days remaining
        renewal_date = datetime.strptime(sub["renewal_date"], '%Y-%m-%d').date()
        delta = renewal_date - today
        sub["days_remaining"] = delta.days
        
        # Flag if overdue (though logic implies future dates usually)
        if sub["days_remaining"] < 0:
             sub["days_remaining"] = 0 # Or handle as overdue

    # Calculate percentages
    ent_percent = (ent_spent / ent_budget * 100) if ent_budget > 0 else 0
    prod_percent = (prod_spent / prod_budget * 100) if prod_budget > 0 else 0

    return render_template("index.html", 
                           subs=subs, 
                           ent_budget=ent_budget, prod_budget=prod_budget,
                           ent_spent=ent_spent, prod_spent=prod_spent,
                           ent_percent=ent_percent, prod_percent=prod_percent)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add a new subscription"""
    if request.method == "POST":
        name = request.form.get("name")
        cost = request.form.get("cost")
        category = request.form.get("category")
        renewal_date = request.form.get("renewal_date")
        billing_cycle = request.form.get("billing_cycle", "Monthly")
        cancel_url = request.form.get("cancel_url")

        if not name or not cost or not category or not renewal_date:
            return apology("Missing fields")
        
        # Validate billing cycle
        allowed_cycles = ["Weekly", "Monthly", "Quarterly", "Annually"]
        if billing_cycle not in allowed_cycles:
            return apology("Invalid billing cycle")
        
        try:
            cost = float(cost)
        except ValueError:
            return apology("Invalid cost")

        if cost <= 0:
            return apology("Cost must be positive")

        db.execute("INSERT INTO subscriptions (user_id, name, cost, category, renewal_date, billing_cycle, cancel_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], name, cost, category, renewal_date, billing_cycle, cancel_url)
        
        flash("Subscription Added!")
        return redirect("/")

    return render_template("add.html")


@app.route("/edit/<int:sub_id>", methods=["GET", "POST"])
@login_required
def edit(sub_id):
    """Edit a subscription"""
    # Ensure user owns the subscription
    sub = db.execute("SELECT * FROM subscriptions WHERE id = ? AND user_id = ?", sub_id, session["user_id"])
    if not sub:
        return apology("Subscription not found or access denied")
    sub = sub[0]

    if request.method == "POST":
        name = request.form.get("name")
        cost = request.form.get("cost")
        category = request.form.get("category")
        renewal_date = request.form.get("renewal_date")
        billing_cycle = request.form.get("billing_cycle", "Monthly")
        cancel_url = request.form.get("cancel_url")

        if not name or not cost or not category or not renewal_date:
            return apology("Missing fields")
        
        # Validate billing cycle
        allowed_cycles = ["Weekly", "Monthly", "Quarterly", "Annually"]
        if billing_cycle not in allowed_cycles:
            return apology("Invalid billing cycle")

        try:
            cost = float(cost)
        except ValueError:
            return apology("Invalid cost")

        db.execute("UPDATE subscriptions SET name = ?, cost = ?, category = ?, renewal_date = ?, billing_cycle = ?, cancel_url = ? WHERE id = ?",
                   name, cost, category, renewal_date, billing_cycle, cancel_url, sub_id)
        
        flash("Subscription Updated!")
        return redirect("/")

    return render_template("edit.html", sub=sub)


@app.route("/delete/<int:sub_id>", methods=["POST"])
@login_required
def delete(sub_id):
    """Delete a subscription"""
    # Ensure user owns the subscription
    rows = db.execute("SELECT * FROM subscriptions WHERE id = ? AND user_id = ?", sub_id, session["user_id"])
    if len(rows) != 1:
        return apology("Subscription not found")

    db.execute("DELETE FROM subscriptions WHERE id = ?", sub_id)
    flash("Subscription Deleted!")
    return redirect("/")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Update budgets"""
    if request.method == "POST":
        ent_budget = request.form.get("entertainment_budget")
        prod_budget = request.form.get("productivity_budget")

        if not ent_budget or not prod_budget:
            return apology("Missing fields")

        try:
            ent_budget = float(ent_budget)
            prod_budget = float(prod_budget)
        except ValueError:
            return apology("Invalid budget")

        db.execute("UPDATE users SET entertainment_budget = ?, productivity_budget = ? WHERE id = ?",
                   ent_budget, prod_budget, session["user_id"])
        
        flash("Settings Updated!")
        return redirect("/")

    user = db.execute("SELECT entertainment_budget, productivity_budget FROM users WHERE id = ?", session["user_id"])[0]
    return render_template("settings.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Missing username")
        if not password:
            return apology("Missing password")
        if password != confirmation:
            return apology("Passwords do not match")

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except ValueError:
            return apology("Username already exists")

        return redirect("/login")

    return render_template("register.html")
