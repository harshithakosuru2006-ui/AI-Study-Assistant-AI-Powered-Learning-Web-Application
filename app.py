from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not API_KEY:
    print("Warning: ANTHROPIC_API_KEY is not configured.")

client = anthropic.Anthropic(api_key=API_KEY) if API_KEY else None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()

        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "success": False,
                "error": "Please enter a question."
            }), 400

        if not client:
            return jsonify({
                "success": False,
                "error": "API key is not configured."
            }), 500

        prompt = f"""
You are an AI Study Assistant.

Help the student understand the following question.

Question:
{question}

Instructions:
- Give a clear and accurate explanation.
- Use simple language.
- Provide examples when useful.
- Structure the answer with headings or bullet points when appropriate.
- Keep the explanation suitable for a college student.
"""

        response = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = ""

        for block in response.content:
            if hasattr(block, "text"):
                answer += block.text

        return jsonify({
            "success": True,
            "answer": answer
        })

    except Exception as error:
        print("Error:", error)

        return jsonify({
            "success": False,
            "error": "Something went wrong while generating the answer."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)