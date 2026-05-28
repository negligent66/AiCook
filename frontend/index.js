const domInput = document.getElementById('domandaInput');
const btnInserisci = document.getElementById('btnInserisci');
const chat = document.getElementById('chat');
const status = document.getElementById('status');

const API_BASE = 'http://localhost:9000';

// Eventi
btnInserisci.addEventListener('click', sendQuestion);
domInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') sendQuestion();
});

// UI messaggi
function appendMessage(text, who) {
    const div = document.createElement('div');
    div.className = `messaggio ${who}`;

    const span = document.createElement('span');

    if (who === 'ai') {
        // Renderizza il Markdown come HTML
        span.innerHTML = marked.parse(text);
    } else {
        span.textContent = text;
    }

    div.appendChild(span);
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// INVIO
async function sendQuestion() {
    const domanda = domInput.value.trim();
    if (!domanda) return;

    appendMessage(domanda, 'user');
    domInput.value = '';
    status.textContent = "Sto pensando...";

    try {
        const resp = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ domanda })
        });

        const data = await resp.json();

        let testo = '';

        if (!data.success || data.error) {
            testo = "ERRORE\n" + (data.error || 'Errore sconosciuto');
        } else {
            testo = data.markdown || '';
        }

        appendMessage(testo, 'ai');

    } catch (err) {
        appendMessage("Errore di connessione al server", 'ai');
        console.error(err);
    } finally {
        status.textContent = '';
    }
}