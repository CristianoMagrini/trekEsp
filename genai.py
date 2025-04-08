from google import genai

with open("transcription/transcription.txt", "r", encoding="utf-8") as f:
    prompt = f.read() + " in formato testo lat, lon con solo i dati"

client = genai.Client(api_key="AIzaSyAyMXVtP5Rg4ibMnZuLeWOvwFGXzxamEO4")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
)

try:
    print(response.candidates[0].content.parts[0].text)
except Exception as e:
    print("Errore nella lettura della risposta:", e)