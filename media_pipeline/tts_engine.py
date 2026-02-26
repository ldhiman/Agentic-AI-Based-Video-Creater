import pyttsx3

def generate_tts(text, output_path):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()


if __name__ == "__main__":
    generate_tts("Cat with hat", r"D:\Autonomus Youtube Channel\sample.wav")