"""Tools the twin can call, plus Pushover notifications for the results."""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"


def push(text: str) -> None:
    """Send a Pushover notification. Never raises -- a failed ping must not
    take down the conversation."""
    if not (PUSHOVER_USER and PUSHOVER_TOKEN):
        print(f"[push skipped, credentials missing] {text}", flush=True)
        return

    try:
        response = requests.post(
            PUSHOVER_URL,
            data={
                "token": PUSHOVER_TOKEN,
                "user": PUSHOVER_USER,
                "message": text,
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[push failed] {exc}", flush=True)


def record_user_details(email, name="Not provided", notes="not given"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"


def record_unknown_question(question):
    push(f"Recording question {question} that I couldn't answer")
    return "OK"


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"}
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_unknown_question": record_unknown_question,
    "record_user_details": record_user_details,
}


def handle_tool_calls(tool_calls):
    """Run every tool the model asked for and return one result message each."""
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        print(f"Tool called: {tool_name}", flush=True)

        tool = tool_map.get(tool_name)
        if tool is None:
            result = f"Unknown tool: {tool_name}"
        else:
            try:
                arguments = json.loads(tool_call.function.arguments or "{}")
                result = tool(**arguments)
            except (json.JSONDecodeError, TypeError) as exc:
                result = f"Tool {tool_name} failed: {exc}"

        results.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id,
            }
        )
    return results
