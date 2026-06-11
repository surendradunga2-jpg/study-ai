from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"


# 🧮 Math detect
def is_math(q):
    return bool(re.search(r'^[0-9\.\s\+\-\*\/\(\)]+$', q))


# 🧮 Safe math solve
def solve_math(q):
    try:
        return str(eval(q))
    except:
        return "Invalid math"


# 🤖 AI answer (for theory)
def ask_ai(q):
    res = requests.post(OLLAMA_URL, json={
        "model": "mistral",
        "prompt": f"""
You are a school STUDY TEACHER AI.

RULES:
- Give SHORT and CORRECT answer only
- No stories
- No extra explanation
- Use simple language

Question: {q}
""",
        "stream": False
    })

    return res.json()["response"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    q = data["question"]

    # 🧮 math first priority
    if is_math(q):
        answer = solve_math(q)
    else:
        answer = ask_ai(q)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)