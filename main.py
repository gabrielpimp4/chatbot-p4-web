
from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("base_conhecimento_chatbot.md", "r", encoding="utf-8") as f:
    knowledge_base = f.read()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def perguntar():
    data = request.get_json()
    pergunta = data.get("pergunta")

    prompt = f"""
Você é um assistente interno da empresa P4. Responda de forma objetiva e baseada na seguinte base de conhecimento:
{knowledge_base}

Pergunta: {pergunta}
Resposta:
"""

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.3
        )
        texto_resposta = resposta.choices[0].message['content'].strip()
        return jsonify({"resposta": texto_resposta})
    except Exception as e:
        return jsonify({"resposta": f"Erro ao consultar a IA: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
