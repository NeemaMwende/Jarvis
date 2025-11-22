import time
from Backend.agent import build_agent
from Backend.stt.whisper_stt import transcribe_whisper
from Backend.tts.pyttsx3_tts import speak_text
from Backend.config import WAKE_WORD

agent = build_agent()

def jarvis_loop():
    print("[Jarvis] System Active... Say 'Jarvis' to wake me.")

    while True:
        text = transcribe_whisper()

        if text and WAKE_WORD in text.lower():
            print("[Jarvis] At your service.")
            speak_text("Yes maam?")
            time.sleep(0.3)

            while True:
                command = transcribe_whisper()
                if not command:
                    continue

                if "stop" in command:
                    speak_text("Going silent.")
                    break

                print("You:", command)
                response = agent.invoke({"input": command})
                answer = response["output"]
                print("Jarvis:", answer)
                speak_text(answer)

if __name__ == "__main__":
    jarvis_loop()
