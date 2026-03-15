# Testvergleich Gemini Flash vs Pro

Dieses Projekt dient dem Vergleich der Kapazitäten und Antwortqualitäten der Gemini-Modelle **Flash** und **Pro**.

## Struktur
- `compare.py`: Das Ausführungsskript (Python).
- `prompts/`: Verzeichnis für Eingabe-Prompts (`.txt`-Dateien).
- `results/`: Verzeichnis für die Ergebnisse im JSON-Format.
- `.env`: Enthält den `GOOGLE_API_KEY` (nicht im Repository).

## Einrichtung
1. Installiere die Abhängigkeiten: `pip install -r requirements.txt`
2. Erstelle eine `.env` Datei basierend auf `.env.example` und füge deinen API-Key hinzu.
3. Lege deine Test-Prompts als Textdateien in den `prompts/` Ordner.

## Ausführung
Starte den Vergleich mit:
```bash
python compare.py
```
Die Ergebnisse werden mit Zeitstempel im `results/` Ordner gespeichert.
