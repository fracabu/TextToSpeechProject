Certo! Ecco un **README** dettagliato e "figo" per il tuo progetto di **Text-to-Speech** con supporto per vari formati di file:

---

# 🎙️ Text-to-Speech Multi-Format Converter

Converti facilmente file **TXT**, **DOC**, **DOCX**, **PDF** in audio **MP3** utilizzando **Google Text-to-Speech (gTTS)**. Questo script Python ti permette di estrarre testo da file di diversi formati, di formattarlo automaticamente per una lettura più naturale, e di salvare l'output come audio in formato **MP3**. Ideale per chi vuole convertire documenti in audio!

## ✨ Funzionalità principali
- **Supporto multi-formato**: Estrai testo da **TXT**, **DOC**, **DOCX**, e **PDF**.
- **Rate Limiting**: Gestione del ritardo tra le chiamate a **gTTS** per evitare limiti di richiesta.
- **Audio in formato MP3**: Ogni blocco di testo viene convertito in MP3 e concatenato per ottenere un unico file audio.
- **Gestione file DOC su Windows**: Utilizza **Win32com** per convertire e gestire i file **.doc**.
- **Salvataggio ordinato**: Organizza e traccia tutti i file audio generati in un file JSON.
- **Riproduzione immediata**: Riproduci subito l'audio generato direttamente dallo script.

## 🚀 Come funziona

### 1. Estrazione del testo
Lo script gestisce file di diversi formati:
- **TXT**: Lettura diretta.
- **DOC/DOCX**: Gestione tramite **python-docx** e conversione da **DOC** a **DOCX** tramite **Win32com** (solo su Windows).
- **PDF**: Estrazione del testo da PDF tramite **PyPDF2**.

### 2. Conversione Text-to-Speech
Il testo viene suddiviso in blocchi di 500 caratteri (configurabile), formattato per garantire una lettura naturale, e convertito in audio MP3 tramite **gTTS**. È possibile personalizzare il **ritardo** tra le chiamate per gestire il rate limiting.

### 3. Salvataggio e gestione
- L'audio viene salvato in una cartella specificata.
- Il nome del file audio viene automaticamente generato e non sovrascrive i file esistenti.
- Ogni conversione viene registrata in un file **JSON**, che contiene i dettagli del file di input e dell'audio generato.

## 🛠️ Tecnologie utilizzate
- **Python**: Il motore principale del progetto.
- **gTTS (Google Text-to-Speech)**: Per la sintesi vocale.
- **PyPDF2**: Per l'estrazione di testo dai PDF.
- **python-docx**: Per gestire i file Word in formato **DOCX**.
- **Win32com**: Per convertire i file **DOC** in **DOCX** (necessario solo su Windows).
- **tqdm**: Per una barra di avanzamento interattiva.
- **JSON**: Per gestire i file audio e le loro informazioni.

## 📦 Installazione

1. Clona il repository:
    ```bash
    git clone https://github.com/tuo-username/tts-multi-format-converter.git
    cd tts-multi-format-converter
    ```

2. Crea un ambiente virtuale e installa le dipendenze:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Installa **FFmpeg** per gestire la conversione audio:
    - Su macOS:
      ```bash
      brew install ffmpeg
      ```
    - Su Windows, scarica da [FFmpeg ufficiale](https://ffmpeg.org/download.html) e aggiungilo al PATH.

## 🏃‍♂️ Utilizzo

1. Esegui lo script passando il percorso del file di testo che vuoi convertire:
    ```bash
    python text_to_speech.py --file_path "percorso/del/file.pdf" --delay 2
    ```

2. Lo script estrarrà il testo dal file, lo convertirà in blocchi di audio **MP3** e salverà il file audio nella cartella specificata.

## 🎯 Esempio

Se hai un file **gaito.txt** sulla tua **scrivania**, puoi eseguirlo così:

```bash
python text_to_speech.py --file_path "C:/Users/utente/Desktop/gaito.txt" --delay 2
```

Output:
- Il file audio verrà salvato in `audio_files/output_1.mp3`.
- I dettagli dell'audio generato verranno salvati in `audio_files/audio_files.json`.

## 📈 Roadmap futura
- **Interfaccia grafica**: Aggiungere un'interfaccia utente (GUI) per una gestione più semplice.
- **Supporto per lingue aggiuntive**: Aggiungere il supporto automatico per più lingue nella sintesi vocale.
- **Supporto per altri formati di file**: Aggiungere compatibilità per altri formati (ad esempio, ODT).

## 📄 Licenza
Questo progetto è distribuito sotto la licenza MIT. Sentiti libero di utilizzarlo, modificarlo e contribuire!

---
