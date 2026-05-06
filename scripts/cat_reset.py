import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "data" / "cat_state.json"

# -----------------------------
# STATO PULITO INIZIALE
# -----------------------------
clean_state = {
    "counter": 0,
    "log": [],
    "last": None,
    "activity": 0.0,
    "bias": {
        "ilgdr": 1.0,
        "minecraft": 1.0,
        "letters": 1.0
    },
    "memory": {
        "last_section": None,
        "repetition_streak": 0
    }
}

# -----------------------------
# SALVATAGGIO RESET
# -----------------------------
with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(clean_state, f, indent=2, ensure_ascii=False)

print("[CAT] memoria resettata - stato pulito")