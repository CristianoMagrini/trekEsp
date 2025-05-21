import re
from google import genai

with open("transcription/transcription.txt", "r", encoding="utf-8") as f:
    prompt = '''Rispondi solo con un oggetto JSON. Non aggiungere testo prima o dopo. Solo una risposta come questa (con singoli apici ', e niente altro, la descrizione non deve avere apostrofi e deve contenere il name e il country del luogo): {'name':'','category':'','lat':,'lng':,'country':'','description':''} in italiano di questo luogo: ''' + f.read()

with open("key/gemini_key.txt", "r", encoding="utf-8") as f:
  client = genai.Client(api_key = f.read())

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
)

try:
    text = response.candidates[0].content.parts[0].text

    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        json_only = match.group(0)
        print(json_only)
    else:
        print("Nessun JSON trovato:", text)

except Exception as e:
    print("Errore:", e)