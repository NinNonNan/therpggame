"""
🐱 CAT SYSTEM — NARRATIVE INTERFERENCE ENGINE

──────────────────────────────────────────────

📌 COSA FA QUESTO SCRIPT

Questo script genera SEMPRE un post Hugo.

Il contenuto del post è deterministico e deciso dall’utente
(tramite parametro di sezione).

Il "Gatto" NON influenza la creazione del post:
influenza solo il contenuto in modo opzionale.

──────────────────────────────────────────────

📌 FLUSSO DI ESECUZIONE

INPUT:
    python cat.py <sezione>

Esempio:
    python cat.py ilgdr

OUTPUT:
    - un file Markdown Hugo creato su disco
    - opzionalmente una sezione di interferenza del gatto

──────────────────────────────────────────────

📌 COMPORTAMENTO DEL GATTO

Il Gatto è un sistema narrativo persistente che:

- legge memoria da cat_state.json
- usa bias per sezione
- accumula comportamento nel tempo
- decide se interferire nel post

Non è obbligatorio:
può non apparire (silenzio narrativo).

──────────────────────────────────────────────

📌 COSA NON FA

✖ Non decide se il post esiste
✖ Non sceglie la sezione
✖ Non genera contenuti autonomamente
✖ Non modifica la struttura del sito

──────────────────────────────────────────────

📌 INTEGRAZIONE CON HUGO

Lo script genera direttamente file compatibili con Hugo:

    +++
    front matter
    +++

    contenuto del post

    + eventuale interferenza del gatto

──────────────────────────────────────────────

📌 OBIETTIVO DEL SISTEMA

Creare un sito in cui:

- i contenuti sono controllati dall’utente
- il gatto introduce rumore narrativo emergente
- il sistema evolve tramite memoria persistente

──────────────────────────────────────────────
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

# -----------------------------
# SETUP
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "data" / "cat_state.json"

# -----------------------------
# INPUT SEZIONE (OBBLIGATORIA)
# -----------------------------
section = sys.argv[1]

# -----------------------------
# CARICA STATO
# -----------------------------
with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

# -----------------------------
# SAFE INIT
# -----------------------------
state.setdefault("bias", {
    "ilgdr": 1.0,
    "minecraft": 1.0,
    "letters": 1.0
})

state.setdefault("memory", {
    "last_section": None,
    "repetition_streak": 0
})

state.setdefault("log", [])
state.setdefault("counter", 0)
state.setdefault("last", None)

# -----------------------------
# SCELTA EVENTO GATTO
# -----------------------------
roll = random.random()

event = None

if roll < 0.5:
    event = "trace"
elif roll < 0.8:
    event = "watch"
elif roll < 0.9:
    event = "event"

# -----------------------------
# DECISIONE INTERFERENZA
# -----------------------------
chance = random.random() * state["bias"].get(section, 1.0)
cat_intervenes = chance > 0.4

cat_payload = None

if cat_intervenes and event:
    cat_payload = {
        "event": event,
        "section": section,
        "timestamp": datetime.now().isoformat()
    }

    entry = {
        "type": event,
        "date": datetime.now().isoformat(),
        "section": section
    }

    state["log"].append(entry)
    state["counter"] += 1
    state["last"] = entry

    # memoria
    last_section = state["memory"].get("last_section")

    if section == last_section:
        state["memory"]["repetition_streak"] += 1
    else:
        state["memory"]["repetition_streak"] = 1

    state["memory"]["last_section"] = section

    # bias dinamico
    if state["memory"]["repetition_streak"] > 2:
        state["bias"][section] *= 0.6

    for k in state["bias"]:
        if k != section:
            state["bias"][k] *= 1.05

# -----------------------------
# SALVA STATO
# -----------------------------
with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

# -----------------------------
# GENERAZIONE POST (SEMPRE)
# -----------------------------
timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
post_file_name = f"gatto-{section}-{timestamp}.md"

post = f"""+++
title = "Evento del Gatto"
date = "{datetime.now().isoformat()}"
draft = false
tags = ["gatto"]
section = "{section}"
+++

# 🐱 Post della sezione {section}

Contenuto del post generato.

"""

# -----------------------------
# AGGIUNTA INTERFERENZA (OPZIONALE)
# -----------------------------
labels = {
    "trace": "traccia lieve",
    "watch": "osservazione silenziosa",
    "event": "interferenza"
}

if cat_payload:
    post += f"""
---

## 🐾 Interferenza del Gatto

Tipo: **{labels[event]}**

{{< cat_{event} >}}
"""

# -----------------------------
# SCRITTURA FILE HUGO
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

sections = {
    "ilgdr": "content/ilgdr",
    "minecraft": "content/minecraft-server",
    "letters": "content/lettere-dal-buio"
}

content_dir = BASE_DIR / sections[section]
content_dir.mkdir(parents=True, exist_ok=True)

file_path = content_dir / post_file_name

with open(file_path, "w", encoding="utf-8") as f:
    f.write(post)

print(f"[CAT] Post creato: {file_path}")