from flask import request

from . import main
from ..bot_commands import parse_callback_query, parse_message


@main.route("/", methods=["POST"])
def receive_update():
    print(request.json)
    if request.method == "POST":
        for key, value in request.json.items():
            match key:
                case "callback_query":
                    parse_callback_query(value)
                case "message":
                    parse_message(value)
    return {"ok": True}
