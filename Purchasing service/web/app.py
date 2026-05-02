#!/usr/bin/python3
import json
import os
import secrets

from flask import Flask, redirect, render_template, request, session, url_for

from runtime import is_internal_bot_request, read_flag, render_records_page, send_delegated_request

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

APP_PORT = int(os.environ.get("APP_PORT", "8000"))
BASE_URL = os.environ.get("BASE_URL", f"http://127.0.0.1:{APP_PORT}")

TEAM_ID = "office-ledger"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

AUTH_USERS = {
    "guest": {
        "password": "guest123",
        "role": "member",
        "team_id": TEAM_ID,
        "login_allowed": True,
    },
    "guest1": {
        "password": "guest123",
        "role": "member",
        "team_id": TEAM_ID,
        "login_allowed": True,
    },
    "bot": {
        "password": None,
        "role": "purchase-bot",
        "team_id": TEAM_ID,
        "login_allowed": False,
    },
}


def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


USER_CREDITS = load_json("users.json")
USERS = {
    username: {
        "username": username,
        "balance": account["balance"],
        **AUTH_USERS[username],
    }
    for username, account in USER_CREDITS.items()
}
PRODUCTS = load_json("products.json")

ORDERS = []


def current_user():
    username = session.get("username")
    if not username:
        return None
    return USERS.get(username)


def authenticate(username, password):
    user = USERS.get(username)
    if not user or not user["login_allowed"]:
        return False
    return user["password"] == password


def find_product(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def team_orders(team_id):
    return [order for order in ORDERS if order["team_id"] == team_id]


def buy_product(username, product_id):
    user = USERS.get(username)
    if not user:
        return False, "Unknown user."

    product = find_product(product_id)
    if not product:
        return False, "Unknown product."

    if user["balance"] < product["price"]:
        return False, "Not enough credits."

    user["balance"] -= product["price"]
    gift_code = None
    if product["is_flag"]:
        gift_code = "GIFT-" + secrets.token_hex(8).upper()

    ORDERS.append(
        {
            "team_id": user["team_id"],
            "buyer": username,
            "product_name": product["name"],
            "price": product["price"],
            "gift_code": gift_code,
        }
    )
    return True, f"Purchased {product['name']}."


def redeem_code(username, code):
    user = USERS.get(username)
    if not user:
        return False, "Unknown user."

    for order in team_orders(user["team_id"]):
        if order.get("gift_code") == code:
            return True, read_flag()
    return False, "Invalid code."


@app.route("/")
def index():
    user = current_user()
    orders = team_orders(user["team_id"]) if user else []
    return render_records_page(
        render_template(
            "index.html",
            user=user,
            orders=orders,
            jobs=[],
            message=None,
            redeem_result=None,
        ),
        orders,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if authenticate(username, password):
        session["username"] = username
        return redirect(url_for("index"))

    return render_template("login.html", error="Login failed.")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/shop")
def shop():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    return render_template("shop.html", user=user, products=PRODUCTS, message=None)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        bot_active = request.form.get("bot_active", "false")
        buyer = request.form.get("buyer", user["username"]).strip()
        target_url = request.form.get("target_url", "/").strip()

        if bot_active != "true":
            return render_settings("Delegated purchase bot is inactive.")

        if buyer != "bot":
            return render_settings("Delegated request was queued for manual review.")

        if send_delegated_request(app, BASE_URL, buyer, target_url):
            return render_settings("Delegated request was sent.")

        return render_settings("Delegated request failed.")

    return render_settings()


@app.route("/buy", methods=["POST"])
def buy():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    if user["role"] == "purchase-bot" and not is_internal_bot_request(request.remote_addr):
        return "Bot purchases must originate from the internal purchase service.", 403

    try:
        product_id = int(request.form.get("product_id", "0"))
    except ValueError:
        product_id = 0

    ok, message = buy_product(user["username"], product_id)
    return render_template(
        "shop.html",
        user=current_user(),
        products=PRODUCTS,
        message=message if ok else f"Purchase failed: {message}",
    )


@app.route("/redeem", methods=["POST"])
def redeem():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    code = request.form.get("code", "").strip()
    ok, result = redeem_code(user["username"], code)
    return render_index(None, result if ok else f"Redeem failed: {result}")


def render_index(message=None, redeem_result=None):
    user = current_user()
    orders = team_orders(user["team_id"]) if user else []
    return render_records_page(
        render_template(
            "index.html",
            user=user,
            orders=orders,
            jobs=[],
            message=message,
            redeem_result=redeem_result,
        ),
        orders,
    )


def render_settings(message=None):
    return render_template("settings.html", user=current_user(), users=USERS.values(), message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)
