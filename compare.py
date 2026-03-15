import os
import json
import time
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

# API-Key konfigurieren
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Fehler: GOOGLE_API_KEY nicht in der Umgebung gefunden. Bitte in einer .env-Datei setzen.")
    exit(1)

genai.configure(api_key=api_key)

MODELLE = {
    "flash": "gemini-1.5-flash",
    "pro": "gemini-1.5-pro"
}

def hole_antwort(modell_name, prompt):
    modell = genai.GenerativeModel(modell_name)
    startzeit = time.time()
    try:
        antwort = modell.generate_content(prompt)
        endzeit = time.time()
        return {
            "text": antwort.text,
            "dauer": endzeit - startzeit,
            "status": "erfolg"
        }
    except Exception as e:
        return {
            "text": str(e),
            "dauer": 0,
            "status": "fehler"
        }

def main():
    prompt_verzeichnis = "prompts"
    ergebnis_verzeichnis = "results"
    
    if not os.path.exists(ergebnis_verzeichnis):
        os.makedirs(ergebnis_verzeichnis)

    prompts = []
    if not os.path.exists(prompt_verzeichnis):
        print(f"Fehler: Verzeichnis '{prompt_verzeichnis}' nicht gefunden.")
        return

    for dateiname in os.listdir(prompt_verzeichnis):
        if dateiname.endswith(".txt"):
            with open(os.path.join(prompt_verzeichnis, dateiname), "r", encoding="utf-8") as f:
                prompts.append({
                    "name": dateiname,
                    "inhalt": f.read().strip()
                })

    if not prompts:
        print(f"Keine Prompts im Verzeichnis '{prompt_verzeichnis}' gefunden.")
        return

    alle_ergebnisse = []

    for prompt_info in prompts:
        print(f"Teste Prompt: {prompt_info['name']}")
        ergebnis = {
            "prompt_name": prompt_info["name"],
            "prompt_inhalt": prompt_info["inhalt"],
            "zeitstempel": datetime.now().isoformat(),
            "antworten": {}
        }

        for kuerzel, modell_id in MODELLE.items():
            print(f"  Rufe Modell auf: {modell_id}...")
            antwort_daten = hole_antwort(modell_id, prompt_info["inhalt"])
            ergebnis["antworten"][kuerzel] = antwort_daten
        
        alle_ergebnisse.append(ergebnis)

    # Ergebnisse speichern
    zeitstempel_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    ausgabedatei = os.path.join(ergebnis_verzeichnis, f"vergleich_{zeitstempel_str}.json")
    
    with open(ausgabedatei, "w", encoding="utf-8") as f:
        json.dump(alle_ergebnisse, f, indent=4, ensure_ascii=False)
    
    print(f"\nFertig! Ergebnisse gespeichert in {ausgabedatei}")

if __name__ == "__main__":
    main()
