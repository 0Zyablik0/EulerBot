import json

import requests
from sqlalchemy import func

from credentials import bot_token
from init import db
from models import User, Topic
from speeches import speeches

TOKEN = bot_token


def send_message(data, method='sendMessage'):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    requests.post(url, data=data)


def parse_callback_query(request):
    data = {"chat_id": request["message"]["chat"]["id"],
            "parse_mode": "Markdown",
            "disable_web_page_preview": "true"}
    topic_name = request["data"]
    topic = Topic.query.filter_by(name=topic_name).first()
    text = f"I want to advise you these materials for learning *{topic_name}*:\n\n"
    if not topic:
        return
    text += "-"*40 + "\n"
    text += "*Books:*\n\n"
    for book in topic.books:
        text += f"[{book.title}]({book.urls}) _by {', '.join(book.authors)}_\n\n"

    text += "*Courses:* _will be available soon..._\n\n"
    text += "-"*40 + '\n'
    text += "PRESS /roadmap to return back\n"
    data["text"] = text
    send_message(data)


def parse_message(request):
    data = {"chat_id": request["chat"]["id"]}
    if "from" in request:
        add_user(request["from"])
    if "text" in request:
        data |= parse_message_text(request)
    send_message(data)


def parse_message_text(request):
    text = request["text"]
    user_id = request["from"]["id"]
    match text:
        case "/start":
            return start_command()
        case "/help":
            return help_command()
        case "/roadmap":
            return roadmap_command(user_id)
        case "/level_up":
            return level_up(user_id)
        case "/level_down":
            return level_down(user_id)
        case "/take_test":
            return test_command()
        case _:
            return {"text": speeches["unknown_command"], "parse_mode": "markdown"}


def start_command():
    result = {"text": speeches["starting_speech"], }
    return result


def level_up(user_id):
    result = {}
    user = User.query.filter_by(id=user_id).first()
    max_level = db.session.query(func.max(Topic.level)).scalar()
    if not max_level or user.level == max_level:
        result["text"] = speeches["level_up_error"]
    else:
        user.level += 1
        db.session.commit()
        result["text"] = speeches["level_up"].format(user.level)
    return result


def level_down(user_id):
    result = {}
    user = User.query.filter_by(id=user_id).first()
    min_level = db.session.query(func.min(Topic.level)).scalar()
    if not min_level or user.level == min_level:
        result["text"] = speeches["level_down_error"]
    else:
        user.level -= 1
        db.session.commit()
        result["text"] = speeches["level_down"].format(user.level)
    return result


def help_command():
    return {"text": speeches["help"]}


def test_command():
    return {"text": "test"}


def roadmap_command(user_id):
    user = User.query.filter_by(id=user_id).first()
    result = Topic.query.filter_by(level=user.level).all()
    keyboard = {"inline_keyboard": []}
    for topic in result:
        key_button = [{"text": topic.name, "callback_data": topic.name}]
        keyboard["inline_keyboard"].append(key_button)
    return {"text": speeches["roadmap"], "reply_markup": json.dumps(keyboard)}


def add_user(user_info):
    user_id = user_info["id"]
    user = User.query.filter_by(id=user_id).first()
    if user:
        return
    first_name = user_info["first_name"]
    last_name = None if "last_name" not in user_info else user_info["last_name"]
    username = None if "username" not in user_info else user_info["username"]
    entry = User(user_id, first_name, last_name, username)
    db.session.add(entry)
    db.session.commit()
