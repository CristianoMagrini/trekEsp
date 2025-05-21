import os
import whisper
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import numpy as np
import subprocess
import asyncio
import websockets

os.environ["PATH"] += os.pathsep + r"ffmpeg\bin"
model = whisper.load_model("medium")
outputDir = "audio"
filename = os.path.join(outputDir, "recordedAudio.wav")
recording = False
frequency = 44100

root = tk.Tk()
root.title("TREKESP")
root.geometry("250x200+100+50")

def audioRecording():
    global recording
    audioResult = []
    try:
        os.makedirs(outputDir, exist_ok=True)
        print("Registrazione in corso...")

        def callback(indata, frames, time, status):
            if recording:
                audioResult.append(indata.copy())

        with sd.InputStream(samplerate=frequency, channels=1, callback=callback):
            while recording:
                sd.sleep(100)

        audioResult = np.concatenate(audioResult, axis=0)
        write(filename, frequency, audioResult)

        transcribeAudio()

    except Exception as e:
        print(f"Errore nella registrazione: {e}")

def transcribeAudio():
    try:
        print("Trascrizione in corso...")
        result = model.transcribe(filename, fp16=False, language="it")
        transcription = result["text"]
        print(f"Trascrizione completata: {transcription}")

        outputTranscription = "transcription"
        os.makedirs(outputTranscription, exist_ok=True)
        with open(os.path.join(outputTranscription, "transcription.txt"), "w", encoding="utf-8") as f:
            f.write(transcription)

        result = subprocess.run(["python", "genai_street.py"], capture_output=True, text=True)
        answer = result.stdout
        print("Risposta: " + answer)

        asyncio.run(sendToWebsocket(answer))

    except Exception as e:
        print(f"Errore nella trascrizione: {e}")

async def sendToWebsocket(message):
    uri = "wss://wsir.sitai2.duckdns.org"
    s = message.replace("'", '\\"')
    s = '''{"message": "trekesp#.#''' + s.strip() + '''"}'''
    s = s.replace("\n", "")
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(s)
            print("Messaggio inviato tramite WebSocket")
    except Exception as e:
        print(f"Errore nell'invio tramite WebSocket: {e}")

def startRecording():
    global recording
    recording = True
    threading.Thread(target=audioRecording).start()

def stopRecording():
    global recording
    recording = False
    messagebox.showinfo("Registrazione interrotta", "La registrazione è stata interrotta")

btnStart = tk.Button(root, text="Inizia registrazione", command=startRecording, width=20)
btnStart.pack(pady=10)

btnStop = tk.Button(root, text="Interrompi registrazione", command=stopRecording, width=20)
btnStop.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()