import os
import json
import time  # Aggiungiamo questo modulo per gestire il rate limiting
from gtts import gTTS
from tqdm import tqdm
from docx import Document  # Per file Word (docx)
import PyPDF2  # Per file PDF
import win32com.client as win32  # Per gestire i file .doc su Windows

def convert_doc_to_docx(doc_path):
    """
    Converte un file .doc in .docx utilizzando Microsoft Word.
    """
    word = win32.Dispatch("Word.Application")
    doc = word.Documents.Open(doc_path)
    docx_path = doc_path.replace(".doc", ".docx")
    doc.SaveAs(docx_path, FileFormat=16)  # 16 è il formato per .docx
    doc.Close()
    word.Quit()
    return docx_path

def extract_text_from_file(file_path):
    """
    Estrae il testo da file PDF, DOCX o TXT e restituisce il contenuto come stringa.
    Se il file è .doc, lo converte prima in .docx.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.txt':
        # Lettura di file di testo (TXT)
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    elif file_extension == '.docx':
        # Lettura di file Word (DOCX)
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    
    elif file_extension == '.pdf':
        # Lettura di file PDF (usando PyPDF2)
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            full_text = []
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                full_text.append(page.extract_text())
            return '\n'.join(full_text)
    
    elif file_extension == '.doc':
        # Converte il file .doc in .docx e poi lo legge
        docx_path = convert_doc_to_docx(file_path)
        return extract_text_from_file(docx_path)
    
    else:
        raise ValueError(f"Formato di file {file_extension} non supportato. Usa TXT, PDF o DOCX.")

def clean_text(text):
    """
    Rimuove o sostituisce caratteri indesiderati come trattini bassi e trattini.
    """
    cleaned_text = text.replace('_', ' ').replace('-', ' ')  # Sostituisci trattini con spazi o rimuovi
    return cleaned_text

def format_text_for_speech(text):
    """
    Formatta automaticamente il testo aggiungendo pause appropriate per il Text-to-Speech.
    Aggiunge punti, virgole e separa paragrafi per una lettura più naturale.
    """
    formatted_text = text.replace("\n", " ").replace(":", ".").replace(";", ".")
    formatted_text = formatted_text.replace(". ", ".\n").replace(", ", ",\n")
    formatted_text = formatted_text.replace(".", ".\n\n").replace("1.", "\n1.")
    formatted_text = formatted_text.replace("2.", "\n2.").replace("3.", "\n3.")
    
    return formatted_text

def text_to_speech(input_text=None, file_path=None, language='it', output_dir='audio_files', base_filename='output', chunk_size=500, delay=1):
    """
    Converte testo in audio. Può accettare un testo direttamente o un file da cui estrarre il testo.
    
    input_text: Testo diretto da convertire (stringa)
    file_path: Percorso del file da cui estrarre il testo (stringa)
    delay: Ritardo in secondi tra ogni chiamata per evitare problemi di rate-limiting.
    """
    # Creare la directory per i file audio se non esiste
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if input_text:
        # Usa il testo passato direttamente
        text = input_text
    elif file_path:
        # Estrazione del testo dal file
        text = extract_text_from_file(file_path)
    else:
        raise ValueError("Devi fornire un testo diretto o un percorso del file.")
    
    # Pulire e formattare il testo
    cleaned_text = clean_text(text)
    formatted_text = format_text_for_speech(cleaned_text)
    
    # Generare un nome univoco per il file audio
    counter = 1
    output_file = os.path.join(output_dir, f"{base_filename}_{counter}.mp3")
    while os.path.exists(output_file):
        counter += 1
        output_file = os.path.join(output_dir, f"{base_filename}_{counter}.mp3")
    
    # Suddividere il testo formattato in blocchi di lunghezza fissa (es. 500 caratteri)
    text_chunks = [formatted_text[i:i+chunk_size] for i in range(0, len(formatted_text), chunk_size)]
    
    # Convertire ogni blocco di testo in audio e concatenarlo
    for i, chunk in enumerate(tqdm(text_chunks, desc="Conversione testo in audio")):
        tts = gTTS(text=chunk, lang=language, slow=False)
        temp_output = f"temp_{i}.mp3"
        tts.save(temp_output)

        # Appendere ogni blocco audio nel file finale
        if i == 0:
            os.rename(temp_output, output_file)
        else:
            with open(output_file, 'ab') as f_out, open(temp_output, 'rb') as f_temp:
                f_out.write(f_temp.read())
            os.remove(temp_output)

        # Aggiungi un ritardo tra le chiamate
        time.sleep(delay)  # Questo aggiunge un ritardo di 'delay' secondi tra ogni chiamata

    print(f'File audio salvato come: {output_file}')
    
    # Aggiornare il file JSON con i dettagli del nuovo file audio
    json_file = os.path.join(output_dir, "audio_files.json")
    audio_data = {"file": output_file, "input": input_text if input_text else file_path, "language": language}
    
    if os.path.exists(json_file):
        # Leggere il file JSON esistente
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Creare un nuovo dizionario se il file non esiste
        data = []
    
    # Aggiungere i dati del nuovo file audio
    data.append(audio_data)
    
    # Salvare l'aggiornamento nel file JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return output_file

def play_audio(output_file):
    import platform
    if platform.system() == 'Windows':
        os.system(f'start {output_file}')
    elif platform.system() == 'Darwin':  # macOS
        os.system(f'open {output_file}')
    else:  # Linux
        os.system(f'xdg-open {output_file}')

# Esempio di utilizzo con file
file_path = r"C:\Users\utente\Desktop\gaito.txt"

# Passare il file_path e aggiungere un ritardo di 2 secondi tra le chiamate
text_to_speech(file_path=file_path, delay=2)
