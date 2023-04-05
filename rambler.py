# Importing libraries
import streamlit as st # For the web part
import speech_recognition as sr # For the stt
import sounddevice as sd # For recording
import wavio # For saving and playing the audio

# Set up the app layout
st.title("The Rambler")
transcription_text = st.empty()
duration = st.slider("Recording duration (seconds)", 
                     min_value=1, 
                     max_value=10, 
                     value=5, 
                     step=1
                     )
# Define the audio recording callback function
def record_audio():
    # Creating the recognizer object
    r = sr.Recognizer()
    fs = 44100  # Sample rate
    # Recording
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    st.info("Recording...")
    sd.wait()  # Wait until recording is finished
    st.success("Recording finished.")
    
    # Save the audio file locally to be played latter
    file_name = "recording.wav"
    wavio.write(file_name, myrecording, fs, sampwidth=2)
    
    # Transcribe the audio using SpeechRecognition library
    with sr.AudioFile(file_name) as source:
        audio_data = r.record(source)
        try:
            audio_text = r.recognize_google(audio_data)
            transcription_text.text(audio_text)
        except sr.UnknownValueError:
            st.error("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Speech Recognition service; {e}")
            
# Create the record and stop buttons
record_button = st.button("Record")
stop_button = st.button("Stop")
play_button = st.button("Play")

# When the record button is clicked, start recording audio
if record_button:
    record_audio()

# When the stop button is clicked, stop recording audio
if stop_button:
    st.warning("Recording stopped.")

# When the play button is clicked, play the recording
if play_button:
    file_name = "recording.wav"
    with open(file_name, "rb") as f:
        bytes_data = f.read()
    st.audio(bytes_data, format="audio/wav")
