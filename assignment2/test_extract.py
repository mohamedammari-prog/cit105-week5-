from extract import parse_response

CLEAN = '[{"title":"Plan network","priority":"high","estimate":45}]'
TASKS = [{"title": "Plan network", "priority": "high", "estimate": 45}]


def test_clean_json_array():
    assert parse_response(CLEAN) == (TASKS, None)


def test_markdown_code_fence():
    text = '```json\n' + CLEAN + '\n```'
    assert parse_response(text) == (TASKS, None)


def test_friendly_sentence_before_json():
    text = "Sure, here you go:\n" + CLEAN
    assert parse_response(text) == (TASKS, None)


def test_no_json_returns_empty_not_exception():
    tasks, message = parse_response("I cannot produce JSON today.")
    assert tasks == []
    assert isinstance(message, str)


def test_truncated_json_returns_empty_not_exception():
    tasks, message = parse_response('[{"title":"Plan network","priority":"high"')
    assert tasks == []
    assert isinstance(message, str)


def test_invalid_priority_is_rejected():
    tasks, message = parse_response('[{"title":"Plan network","priority":"urgent","estimate":45}]')
    assert tasks == []
    assert isinstance(message, str)
