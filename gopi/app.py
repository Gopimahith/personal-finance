from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Path to transactions file
DATA_FILE = "data/transaction.csv/tra.css"  # Update this path

# Ensure data directory and file exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write("Date,Description,Amount\n")  # CSV header

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/tracker", methods=["GET", "POST"])
def tracker():
    transactions = []

    if request.method == "POST":
        # Add a new transaction
        date = request.form.get("date")
        description = request.form.get("description")
        amount = request.form.get("amount")

        if date and description and amount:
            with open(DATA_FILE, "a", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([date, description, amount])
            return redirect(url_for("tracker"))

    # Read transactions
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            transactions = list(reader)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")

    return render_template("tracker.html", transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)