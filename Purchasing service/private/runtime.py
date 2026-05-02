import os
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

FLAG_PATH = os.environ.get("FLAG_PATH", "./flag.txt")


def read_flag():
    try:
        with open(FLAG_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "2026HL{...}"


def render_records_page(html, records):
    comments = []
    for record in records:
        if record.get("gift_code"):
            comments.append(
                f"<!-- ledger gift_code buyer={record['buyer']} value={record['gift_code']} -->"
            )
    if comments:
        html += "\n" + "\n".join(comments)
    return html


def is_internal_leader_request(remote_addr):
    return remote_addr in ("127.0.0.1", "::1")


def send_delegated_request(flask_app, base_url, username, target_path):
    if not target_path.startswith("/"):
        return False

    serializer = flask_app.session_interface.get_signing_serializer(flask_app)
    session_cookie = serializer.dumps({"username": username})
    parsed = urlparse(target_path)
    target = urljoin(base_url, parsed.path)
    form = parse_qs(parsed.query)
    headers = {"Cookie": f"session={session_cookie}"}
    data = None
    method = "GET"

    if parsed.path == "/buy":
        product_id = form.get("product_id", form.get("id", ["0"]))[0]
        data = urlencode({"product_id": product_id}).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        method = "POST"

    delegated_request = Request(target, data=data, headers=headers, method=method)

    try:
        with urlopen(delegated_request, timeout=3) as response:
            response.read(1024)
        return True
    except Exception:
        return False
