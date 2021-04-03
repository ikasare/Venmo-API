import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(error, code=404):
    return json.dumps({"success": False, "error": error}), code

@app.route("/")
@app.route("/api/users/")
def get_users():
    return success_response(DB.get_all_users())

@app.route("/api/users/", methods=["POST"])
def create_venmo():
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance", 0)
    if name is not None and username is not None:
        user_id = DB.insert_venmo_user(name, username, balance)
        return success_response(DB.get_user_by_id(user_id))
    return failure_response("No name or username or both were not entered", 400)
@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    user = DB.get_user_by_id(user_id)
    if user:
        return success_response(user)
    return failure_response("No user found")


@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("No user found")
    DB.delete_user_by_id(user_id)
    return success_response(user)

@app.route("/api/send/", methods=["POST"])
def send():
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    if sender_id is None or receiver_id is None or amount is None:
        return failure_response("You did not enter input right")
    sender_obj = DB.get_user_by_id(sender_id)
    receiver_obj = DB.get_user_by_id(receiver_id)
    if not sender_obj or not receiver_obj:
        return failure_response("either the sender or receiver does not exist")
    sender_balance = sender_obj["balance"]
    if sender_balance >= amount:
        sender_new_balance = sender_balance - amount
        DB.update(sender_id, sender_new_balance)
    else:
        return failure_response("You dont have enough money")
        
    receiver_balance = receiver_obj["balance"]
    receiver_new_balance = receiver_balance + amount
    DB.update(receiver_id, receiver_new_balance)
    return success_response({"sender_id": sender_id, "receiver_id": receiver_id, "amount": amount})
   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
