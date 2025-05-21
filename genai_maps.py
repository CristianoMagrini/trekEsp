import webbrowser
from google import genai

with open("transcription/transcription.txt", "r", encoding="utf-8") as f:
    prompt = "Dammi le coordinate di " + f.read() + " in formato testo lat, lon con solo i dati"

client = genai.Client(api_key="AIzaSyAyMXVtP5Rg4ibMnZuLeWOvwFGXzxamEO4")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
)

try:
    print(response.candidates[0].content.parts[0].text)

    coordinates = response.text.strip()
    lat, lon = coordinates.split(",")
    street_view_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"

    webbrowser.open(street_view_url)
except Exception as e:
    print("Errore nel calcolo delle coordinate", e)