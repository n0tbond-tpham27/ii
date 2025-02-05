import os
import openai
from flask import Flask, jsonify

# Fetch API key from GitHub Secrets (environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_biology_question():
    """Generates an AP Bio/USABO-style multiple-choice question using OpenAI"""
    prompt = """
    Generate a challenging AP Biology or USABO-style multiple-choice question. 
    Include four answer options (A, B, C, D) and specify the correct answer with an explanation. 
    Format it in JSON as follows:

    {
        "question": "What is the primary function of the mitochondria?",
        "options": ["A. DNA replication", "B. Protein synthesis", "C. Energy production", "D. Lipid metabolism"],
        "correct_answer": "C",
        "explanation": "Mitochondria generate ATP, which serves as the primary energy source for cellular functions."
    }
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
        messages=[{"role": "system", "content": prompt}]
    )

    try:
        question_data = response["choices"][0]["message"]["content"]
        return jsonify(question_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/generate-question', methods=['GET'])
def generate_question():
    return generate_biology_question()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
