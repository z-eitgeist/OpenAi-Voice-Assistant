import time
import openai
import pyttsx3
import speech_recognition as sr

# OpenAi API key
openai.api_key = "Enter your OpenAi API key"

# Initialize text-to-speech
engine = pyttsx3.init()

# Transcribe voice to text using speech recognition library
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    # Open the audio file
    with sr.AudioFile(audio_file) as audio_source:
        # Record the audio using record method
        audio = recognizer.record(audio_source)
    try:
        # Transcribe recorded audio to text
        return recognizer.recognize_google(audio)
    except:
        print("Unknown error... skipping.")

# Generate responses from OpenAI 
def ask_openai(question):
    # Pass the arguments to specify parameters of the response
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = question, 
        temperature = 0.5,
        max_tokens = 2000,
        n = 1,
        stop = None
    )
    return response["choices"][0]["text"]

# Define function that takes text argument and converts it to speech
def speak_to_text(text):
    engine.say(text)
    engine.runAndWait()

# Define how you want Python to run the script
def main():
    while True:
        # Wait for the user to say "Albert"
        print("Say \"Albert\" to start recording the question or say \"Exit\" to exit the program.")
        with sr.Microphone() as audio_source:
            recognizer = sr.Recognizer()
            # Record the audio
            audio = recognizer.listen(audio_source)
            try: 
                # Transcribe audio to text using recognize google method
                transcript = recognizer.recognize_google(audio)
                # Chek if transcribed text is Albert 
                if transcript.lower() == "albert":
                    # Record the rest of audio
                    filename = "audio_input.wav"
                    print("Yes? I am listening...")
                    # If transcribed text is Albert, record more audio and save it as audio_input.wav
                    with sr.Microphone() as source:
                        recognizer=sr.Recognizer()
                        source.pause_threshold=1
                        audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())
                    
                    # Transcribe recorded audio to text
                    text = audio_to_text(filename)
                    if text:
                        print(f"Your question: {text}")

                        # Generate responce usin openAI GTP-3
                        response = ask_openai(text)
                        print(f"My answer: {response}")

                        # Read the response 
                        speak_to_text(response)
                elif transcript.lower() == "exit":
                    break
            # Handle errors
            except Exception as e:
                print("Error occured {}".format(e))

# Run the main function
if __name__ == "__main__":
    main()