from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.document_loaders import PyPDFLoader

import os
import json
import mysql.connector

PDF_PATH = "vs/data/ricettine.pdf"

db_config = {
    "host": "192.168.15.17",
    "user": "Cuoco",
    "password": "Password",
    "database": "AI_COOK"
}

MAX_CHARS = 30000

if not os.path.exists(PDF_PATH):
    raise Exception(f"PDF non trovato: {PDF_PATH}")

print("Carico modello...")

model = ChatOllama(
    model="qwen2:7b",
    temperature=0,
    num_ctx=32000
)

print("Modello pronto")

# load delpdf

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

doc_text = "\n".join(doc.page_content for doc in docs)

if len(doc_text) > MAX_CHARS:
    print("PDF troppo lungo, taglio in esecuzione...")
    doc_text = doc_text[:MAX_CHARS]

print("Lunghezza testo:", len(doc_text))

system_extract = """
ESTRAI LE RICETTE DAL TESTO.

REGOLE:
- SOLO JSON
- NESSUNA SPIEGAZIONE
- NESSUN MARKDOWN
- OUTPUT VALIDO JSON

FORMATO:

{
  "ricette": [
    {
      "nome": "string",
      "categoria": "Primo|Secondo|Contorno|Dessert",
      "tempo": 0,
      "difficolta": "Non presente|Bassa|Media|Alta",
      "ingredienti": [
        {
          "nome": "string",
          "quantita": "string",
          "unita": "string"
        }
      ],
      "preparazione": [
        "step 1",
        "step 2"
      ]
    }
  ]
}
"""

messages = [
    SystemMessage(content=system_extract),
    HumanMessage(content=doc_text)
]

response = model.invoke(messages)

# PARSE JSON

try:
    content = response.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "")
        content = content.replace("```", "")

    ricette_json = json.loads(content)

    print("Estrazione completata! ")

except Exception as e:
    print("Errore parsing JSON... ")
    print(e)
    print(response.content)
    exit()

# connessione al DB

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    print("----- Connesso al database -----")

except mysql.connector.Error as err:
    print("Errore connessione DB...")
    print(err)
    exit()

categorie = {
    "Primo": 1,
    "Secondo": 2,
    "Contorno": 3,
    "Dessert": 4
}

def to_int(value):
    try:
        return int(value)
    except:
        return None

# INSERT DEI DATI

try:

    for ricetta in ricette_json.get("ricette", []):

        nome_ricetta = ricetta.get("nome", "").strip()

        if not nome_ricetta:
            continue

        print(f"\n>> Inserisco la ricetta: {nome_ricetta}")

        categoria_nome = ricetta.get("categoria", "Primo")
        id_categoria = categorie.get(categoria_nome, 1)

        tempo = to_int(ricetta.get("tempo"))

        difficolta = ricetta.get("difficolta", "Non presente")

        if difficolta not in [
            "Non presente",
            "Bassa",
            "Media",
            "Alta"
        ]:
            difficolta = "Non presente"

        # insert RICETTA

        sql_ricetta = """
        INSERT INTO RICETTA
        (idCategoria, nome, tempo, difficolta)
        VALUES (%s, %s, %s, %s)
        """

        values_ricetta = (
            id_categoria,
            nome_ricetta,
            tempo,
            difficolta
        )

        cursor.execute(sql_ricetta, values_ricetta)

        id_ricetta = cursor.lastrowid

        print(f"- Ricetta inserita ID={id_ricetta}")

        # INGREDIENTI

        ingredienti = ricetta.get("ingredienti", [])

        for ingrediente in ingredienti:

            nome_ing = ingrediente.get("nome", "").strip()

            if not nome_ing:
                continue

            quantita = ingrediente.get("quantita")
            unita = ingrediente.get("unita")

            if not unita:
                unita = "unita"

            # lo cerca nel DB

            cursor.execute(
                """
                SELECT idIngrediente
                FROM INGREDIENTI
                WHERE nome = %s
                """,
                (nome_ing,)
            )

            result = cursor.fetchone()

            # se non lo trova lo inserisce

            if result is None:

                cursor.execute(
                    """
                    INSERT INTO INGREDIENTI (nome)
                    VALUES (%s)
                    """,
                    (nome_ing,)
                )

                id_ingrediente = cursor.lastrowid

                print(f"<< Ingrediente creato: {nome_ing}")

            else:

                id_ingrediente = result[0]

            # insert ricetteingredienti

            sql_rel = """
            INSERT INTO RICETTEINGREDIENTI
            (
                idIngrediente,
                idRicetta,
                quantita,
                unita_di_misura
            )
            VALUES (%s, %s, %s, %s)
            """

            values_rel = (
                id_ingrediente,
                id_ricetta,
                str(quantita) if quantita else None,
                unita
            )

            cursor.execute(sql_rel, values_rel)

        # PREPARAZIONE

        preparazione = ricetta.get("preparazione", [])

        for i, step in enumerate(preparazione, start=1):

            if not step:
                continue

            sql_step = """
            INSERT INTO PREPARAZIONE
            (
                idRicetta,
                progressivo,
                descrizione
            )
            VALUES (%s, %s, %s)
            """

            values_step = (
                id_ricetta,
                i,
                step
            )

            cursor.execute(sql_step, values_step)

        print("Preparazione inserita!\n")

    # commit

    conn.commit()

    print("\n--- IMPORT COMPLETATO ---")

except mysql.connector.Error as err:

    print("\nErrore MYSQL: ")
    print(err)

    conn.rollback()

except Exception as e:

    print("\nErrore: ")
    print(e)

    conn.rollback()

finally:

    if conn.is_connected():
        cursor.close()
        conn.close()

    print("----- Connessione chiusa -----")

