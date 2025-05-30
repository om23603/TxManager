from flask import Flask, request, render_template, redirect, url_for

app =Flask("Transaction Operations")

transactions = [
    # {'id': 1, 'date': '2024-07-01', 'amount': 100},
    # {'id': 2, 'date': '2024-07-02', 'amount': -200},
    # {'id': 3, 'date': '2024-07-03', 'amount': 300},
    # {'id': 4, 'date': '2024-07-04', 'amount': 500}
]

# Read operation
@app.route('/')
def get_transactions():
    # Total balance
    total_balance = sum(transaction["amount"] for transaction in transactions)
    return render_template("transactions.html", transactions=transactions, total_balance=total_balance)

# Create operation
@app.route('/add', methods=["GET","POST"])
def add_transaction():
    if request.method == "POST":
        transaction = {
            "id": len(transactions) + 1,
            "date": request.form["date"],
            "amount": float(request.form["amount"])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))
    return render_template("form.html")

# Update operation
@app.route('/edit/<int:transaction_id>', methods=["GET","POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        date = request.form["date"]
        amount = float(request.form["amount"])

        for transaction in transactions:
            if transaction_id == transaction["id"]:
                transaction["date"] = date
                transaction["amount"] = amount
                break
        return redirect(url_for("get_transactions"))
    
    for transaction in transactions:
        if transaction_id == transaction["id"]:
            return render_template("edit.html", transaction=transaction)
    return {"message": "Transaction not found"}, 404

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction_id == transaction["id"]:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

# Search Operation
@app.route('/search', methods=["GET", "POST"])
def search_transaction():
    if request.method == "POST":
        filtered_transactions = []
        min_amount = float(request.form["min_amount"])
        max_amount = float(request.form["max_amount"])
        total_filtered = 0
        for transaction in transactions:
            if min_amount <= transaction["amount"] <= max_amount:
                filtered_transactions.append(transaction)
                total_filtered += transaction["amount"]
        return render_template("transactions.html", transactions=filtered_transactions, total_balance=total_filtered)
    return render_template("search.html")

# Run the Flask app
if __name__ == "__main__":
    app.run()