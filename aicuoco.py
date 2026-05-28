from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from ollama import Client

app = Flask(__name__)
CORS(app)

# Configurazione MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'AI_COOK'
}

# Configurazione modello locale Ollama
lcmodel = Client()
MODEL_NAME = "qwen3.5:9b"

SYSTEM_PROMPT = """
Sei un cuoco di nome Giorgio Locatelli, esperto e prepari risposte utili e amichevoli, parli in quattro quarti.
Usa solo e soltanto le ricette del database per rispondere alle domande dell'utente.
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        domanda = data.get('domanda', '')

        # 1. Recupera le ricette dal database
        ricette = get_ricette_dal_db()

        # 2. Costruisci il contesto con le ricette e la domanda
        contesto_ricette = "\n\n".join([str(r) for r in ricette])
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Ricette disponibili:\n{contesto_ricette}\n\nDomanda: {domanda}"}
        ]

        # 3. Ottieni la risposta dal modello (think=False disabilita il thinking)
        response = lcmodel.chat(model=MODEL_NAME, messages=messages, think=False)
        risposta = response.message.content  # <-- sintassi corretta per la libreria ollama

        print(f"[DEBUG] Risposta modello: {risposta}")
        # 4. Restituisci la risposta con Markdown
        return jsonify({
            'success': True,
            'markdown': risposta
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def get_ricette_dal_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SET SESSION group_concat_max_len = 100000")
    cursor.execute('''
        SELECT r.nome, r.descrizione, r.tempo, r.difficolta,
        GROUP_CONCAT(CONCAT(ri.quantita, ' ', ri.unita_di_misura, ' di ', i.nome) 
                        ORDER BY i.nome SEPARATOR ', ') as ingredienti,
        GROUP_CONCAT(p.descrizione ORDER BY p.progressivo SEPARATOR ' | ') as passaggi
        FROM RICETTA r
        LEFT JOIN RICETTEINGREDIENTI ri ON r.idRicetta = ri.idRicetta
        LEFT JOIN INGREDIENTI i ON ri.idIngrediente = i.idIngrediente
        LEFT JOIN PREPARAZIONE p ON r.idRicetta = p.idRicetta
        GROUP BY r.idRicetta
    ''')

    ricette = cursor.fetchall()
    cursor.close()
    conn.close()
    return ricette

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)