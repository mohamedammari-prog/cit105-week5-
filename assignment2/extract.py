"""Extract validated task cards from unstructured project text using an AI API."""
import json
import os
import re
import requests

# Set these only to the endpoint/model approved by the course instructor.
API_URL = os.getenv("COURSE_AI_API_URL", "https://api.openai.com/v1/chat/completions")
MODEL = os.getenv("COURSE_AI_MODEL", "gpt-4o-mini")
REQUIRED_KEYS = {"title", "priority", "estimate"}
ALLOWED_PRIORITIES = {"low", "medium", "high"}

PROMPT_TEMPLATE = """Convert the project description into task cards.
Return exactly one JSON array and no other text. Do not include a preamble,
markdown code fences, or explanation. Every array item must be an object with
exactly these keys: "title" (a non-empty string), "priority" (one of "low",
"medium", or "high"), and "estimate" (a positive integer number of minutes).
Do not invent tasks unrelated to the project description.
Project description:
{description}
"""


def extract_json_array(text):
    """Find and parse the first complete JSON array in a model response."""
    if not isinstance(text, str):
        return []
    decoder = json.JSONDecoder()
    for match in re.finditer(r"\\[", text):
        try:
            value, _ = decoder.raw_decode(text[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(value, list):
            return value
    return []


def validate_tasks(value):
    """Return a valid task list, or an empty list if its shape is invalid."""
    if not isinstance(value, list):
        return []
    validated = []
    for item in value:
        if not isinstance(item, dict) or set(item.keys()) != REQUIRED_KEYS:
            return []
        if not isinstance(item["title"], str) or not item["title"].strip():
            return []
        if item["priority"] not in ALLOWED_PRIORITIES:
            return []
        if isinstance(item["estimate"], bool) or not isinstance(item["estimate"], int) or item["estimate"] <= 0:
            return []
        validated.append(item)
    return validated


def parse_response(text):
    """Parse defensively; return an empty result and readable message on failure."""
    try:
        parsed = extract_json_array(text)
        if not parsed:
            return [], "The AI response did not contain a usable JSON task array."
        tasks = validate_tasks(parsed)
        if not tasks:
            return [], "The AI response contained tasks with an invalid structure."
        return tasks, None
    except (ValueError, TypeError, json.JSONDecodeError):
        return [], "The AI response could not be read. Please try again."


def generate_tasks(description, timeout=20):
    """Call the configured API once and return tasks, message, and token usage."""
    key = os.getenv("COURSE_AI_API_KEY")
    if not key:
        return [], "Missing COURSE_AI_API_KEY environment variable.", None
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Return structured task data following the user's schema exactly."},
            {"role": "user", "content": PROMPT_TEMPLATE.format(description=description)},
        ],
        "temperature": 0,
    }
    try:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload,
            timeout=timeout,
        )
        if response.status_code != 200:
            return [], f"The AI service returned HTTP {response.status_code}. Please try again later.", None
        body = response.json()
        text = body["choices"][0]["message"]["content"]
        usage = body.get("usage", {})
        tasks, message = parse_response(text)
        return tasks, message, usage
    except requests.exceptions.Timeout:
        return [], "The AI service took too long to respond. Please try again.", None
    except requests.exceptions.RequestException:
        return [], "Could not reach the AI service. Check your connection and try again.", None
    except (ValueError, KeyError, IndexError, TypeError):
        return [], "The AI service returned an unexpected response format.", None


def main():
    description = input("Paste a project description, then press Enter: ").strip()
    if not description:
        print("Please enter a project description.")
        return
    tasks, message, usage = generate_tasks(description)
    if message:
        print(message)
    if tasks:
        print(json.dumps(tasks, indent=2))
    if usage is not None:
        print(
            "Token usage: "
            f"prompt={usage.get('prompt_tokens', 'unknown')}, "
            f"completion={usage.get('completion_tokens', 'unknown')}, "
            f"total={usage.get('total_tokens', 'unknown')}"
        )


if __name__ == "__main__":
    main()
