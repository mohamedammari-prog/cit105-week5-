# CIT 105 Module 5 — Assignment 2: Structured Prompt Script

## Purpose and schema
The script turns a project description into task cards. Each item must contain exactly:
- `title`: non-empty string
- `priority`: `low`, `medium`, or `high`
- `estimate`: positive integer minutes

## Full prompt
The script's `PROMPT_TEMPLATE` in `extract.py` is the full prompt used. It specifies the exact JSON array shape, allowed priority values, positive integer estimate, and forbids preambles, markdown fences, and explanations.

## Setup
1. `.gitignore` excludes `.env` and Python-generated files. It was committed before the other assignment files.
2. Set the course-approved API key in your environment as `COURSE_AI_API_KEY`. Do not put the key in this repository or paste it into chat.
3. If the course provider uses a different endpoint or model, set `COURSE_AI_API_URL` and `COURSE_AI_MODEL` according to the instructor's documentation.
4. Install dependencies and run tests:
   ```bash
   python -m pip install requests pytest
   python -m pytest -q
   python extract.py
   ```

## Test run
The parser tests were run in the draft environment and passed: `6 passed`. Re-run them in your own environment and replace this note with your actual test output before submission.

## What surprised me
A response can contain valid JSON yet still be unusable if a task has an extra/missing key or a priority outside the allowed set. The parser therefore validates the structure after parsing instead of trusting valid JSON alone.

## AI assistance disclosure
ChatGPT assisted with an initial code draft and test cases. I reviewed the code and will be prepared to explain the prompt, parser, validation rules, and failure handling.
